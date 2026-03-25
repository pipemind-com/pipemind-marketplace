use reqwest::Client;
use serde::de::DeserializeOwned;
use std::fmt;
use std::sync::Arc;
use std::time::{Duration, Instant, SystemTime, UNIX_EPOCH};
use tokio::sync::Mutex;

use crate::types::*;

const BASE_URL: &str = "https://api.semanticscholar.org/graph/v1";
const DEFAULT_FIELDS: &str = "paperId,title,abstract,year,authors,citationCount,influentialCitationCount,isOpenAccess,openAccessPdf,externalIds,url,publicationTypes,fieldsOfStudy";
const MAX_RETRIES: u32 = 3;
/// Minimum interval between requests (S2 allows 1 req/sec with a key)
const MIN_REQUEST_INTERVAL: Duration = Duration::from_millis(1050);
const ATTRIBUTION: &str = "\n---\n*Data provided by Semantic Scholar*";

#[derive(Debug)]
pub enum ApiError {
    UserFacing(String),
    Internal(String),
}

impl fmt::Display for ApiError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ApiError::UserFacing(msg) => write!(f, "{msg}"),
            ApiError::Internal(msg) => write!(f, "{msg}"),
        }
    }
}

#[derive(Clone)]
pub struct S2Client {
    http: Client,
    api_key: String,
    last_request: Arc<Mutex<Instant>>,
    base_url: String,
    max_retries: u32,
    retry_base_ms: u64,
    throttle_disabled: bool,
}

impl S2Client {
    pub fn new(api_key: String) -> Self {
        let http = Client::builder()
            .user_agent("mcp-semantic-scholar/0.1.0")
            .timeout(Duration::from_secs(30))
            .build()
            .expect("failed to build HTTP client");
        Self {
            http,
            api_key,
            last_request: Arc::new(Mutex::new(Instant::now() - MIN_REQUEST_INTERVAL)),
            base_url: BASE_URL.to_string(),
            max_retries: MAX_RETRIES,
            retry_base_ms: 1000,
            throttle_disabled: false,
        }
    }

    pub fn new_with_base_url(api_key: String, base_url: String) -> Self {
        let mut client = Self::new(api_key);
        client.base_url = base_url;
        client
    }

    pub fn with_retry_config(mut self, max_retries: u32, retry_base_ms: u64) -> Self {
        self.max_retries = max_retries;
        self.retry_base_ms = retry_base_ms;
        self.throttle_disabled = true;
        self
    }

    /// Enforce 1 req/sec rate limit proactively
    async fn throttle(&self) {
        if self.throttle_disabled {
            return;
        }
        let mut last = self.last_request.lock().await;
        let elapsed = last.elapsed();
        if elapsed < MIN_REQUEST_INTERVAL {
            tokio::time::sleep(MIN_REQUEST_INTERVAL - elapsed).await;
        }
        *last = Instant::now();
    }

    async fn get<T: DeserializeOwned>(&self, url: &str) -> Result<T, ApiError> {
        let mut last_err = String::new();

        for attempt in 0..=self.max_retries {
            if attempt > 0 {
                let base_ms = self.retry_base_ms * (1 << (attempt - 1));
                let jitter_ms = SystemTime::now()
                    .duration_since(UNIX_EPOCH)
                    .unwrap_or_default()
                    .subsec_nanos() as u64
                    % 500;
                tokio::time::sleep(Duration::from_millis(base_ms + jitter_ms)).await;
                tracing::info!(attempt, "retrying after rate limit");
            }

            self.throttle().await;

            let resp = match self
                .http
                .get(url)
                .header("x-api-key", &self.api_key)
                .send()
                .await
            {
                Ok(r) => r,
                Err(e) => {
                    last_err = format!("HTTP request failed: {e}");
                    continue;
                }
            };

            let status = resp.status();

            // 401/403 — invalid or revoked API key; no retry
            if status == reqwest::StatusCode::UNAUTHORIZED
                || status == reqwest::StatusCode::FORBIDDEN
            {
                return Err(ApiError::UserFacing(format!(
                    "Your API key appears to be invalid or revoked. \
                     Get a new key at: https://www.semanticscholar.org/product/api#api-key-form\
                     {ATTRIBUTION}"
                )));
            }

            if status == reqwest::StatusCode::TOO_MANY_REQUESTS {
                last_err = "Rate limited (429)".to_string();
                tracing::warn!(attempt, "received 429 from Semantic Scholar API");
                continue;
            }

            // 404 — resource not found
            if status == reqwest::StatusCode::NOT_FOUND {
                return Err(ApiError::UserFacing(format!(
                    "Not found: the requested resource does not exist on Semantic Scholar.\
                     {ATTRIBUTION}"
                )));
            }

            if !status.is_success() {
                let body = resp.text().await.unwrap_or_default();
                return Err(ApiError::Internal(format!(
                    "Semantic Scholar API returned {status}: {body}{ATTRIBUTION}"
                )));
            }

            return resp.json::<T>().await.map_err(|e| {
                ApiError::Internal(format!(
                    "Failed to parse API response: {e}{ATTRIBUTION}"
                ))
            });
        }

        Err(ApiError::UserFacing(format!(
            "Semantic Scholar API rate limit exceeded after {} retries. \
             Try again in a few minutes. Last error: {last_err}{ATTRIBUTION}",
            self.max_retries
        )))
    }

    pub async fn search_papers(
        &self,
        query: &str,
        limit: u32,
        offset: u32,
    ) -> Result<SearchResponse, ApiError> {
        let url = format!(
            "{}/paper/search?query={}&fields={DEFAULT_FIELDS}&limit={limit}&offset={offset}",
            self.base_url,
            urlencoded(query)
        );
        self.get(&url).await
    }

    pub async fn get_paper(&self, paper_id: &str) -> Result<Paper, ApiError> {
        let url = format!(
            "{}/paper/{}?fields={DEFAULT_FIELDS}",
            self.base_url,
            urlencoded(paper_id)
        );
        self.get(&url).await
    }

    pub async fn get_references(
        &self,
        paper_id: &str,
        limit: u32,
    ) -> Result<PaginatedReferences, ApiError> {
        let url = format!(
            "{}/paper/{}/references?fields={DEFAULT_FIELDS}&limit={limit}",
            self.base_url,
            urlencoded(paper_id)
        );
        self.get(&url).await
    }

    pub async fn get_citations(
        &self,
        paper_id: &str,
        limit: u32,
    ) -> Result<PaginatedCitations, ApiError> {
        let url = format!(
            "{}/paper/{}/citations?fields={DEFAULT_FIELDS}&limit={limit}",
            self.base_url,
            urlencoded(paper_id)
        );
        self.get(&url).await
    }
}

pub(crate) fn urlencoded(s: &str) -> String {
    s.chars()
        .map(|c| match c {
            ' ' => "+".to_string(),
            c if c.is_ascii_alphanumeric() || "-._~".contains(c) => c.to_string(),
            c => format!("%{:02X}", c as u32),
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::urlencoded;

    #[test]
    fn test_urlencoded_alphanumeric() {
        assert_eq!(urlencoded("abc123"), "abc123");
    }

    #[test]
    fn test_urlencoded_spaces() {
        assert_eq!(urlencoded("neural scaling laws"), "neural+scaling+laws");
    }

    #[test]
    fn test_urlencoded_preserved_chars() {
        assert_eq!(urlencoded("-._~"), "-._~");
    }

    #[test]
    fn test_urlencoded_colon() {
        assert_eq!(urlencoded(":"), "%3A");
    }

    #[test]
    fn test_urlencoded_slash() {
        assert_eq!(urlencoded("/"), "%2F");
    }

    #[test]
    fn test_urlencoded_doi() {
        assert_eq!(
            urlencoded("DOI:10.1145/1234.5678"),
            "DOI%3A10.1145%2F1234.5678"
        );
    }

    #[test]
    fn test_urlencoded_arxiv() {
        assert_eq!(urlencoded("ArXiv:2301.12345"), "ArXiv%3A2301.12345");
    }

    #[test]
    fn test_urlencoded_empty() {
        assert_eq!(urlencoded(""), "");
    }

    #[test]
    fn test_urlencoded_unicode() {
        // U+00E9 (é) encoded by Unicode scalar value
        assert_eq!(urlencoded("caf\u{00E9}"), "caf%E9");
    }

    #[test]
    fn test_urlencoded_mixed() {
        assert_eq!(
            urlencoded("hello world: foo/bar"),
            "hello+world%3A+foo%2Fbar"
        );
    }
}
