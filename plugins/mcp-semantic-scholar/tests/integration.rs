#![allow(unused_imports)]

use mcp_semantic_scholar::api::{S2Client, ApiError};
use wiremock::{MockServer, Mock, ResponseTemplate};
use wiremock::matchers::{method, path, path_regex};
use serde_json::json;

fn make_paper_json(paper_id: &str, title: &str) -> serde_json::Value {
    json!({
        "paperId": paper_id,
        "title": title,
        "abstract": null,
        "year": 2024,
        "authors": [{"authorId": "1", "name": "Test Author"}],
        "citationCount": 5,
        "influentialCitationCount": 1,
        "isOpenAccess": false,
        "openAccessPdf": null,
        "externalIds": {"DOI": null, "ArXiv": null, "CorpusId": null, "PubMed": null},
        "url": "https://semanticscholar.org/paper/test",
        "publicationTypes": null,
        "fieldsOfStudy": null
    })
}

fn client_for(server: &MockServer) -> S2Client {
    S2Client::new_with_base_url("test-key".into(), format!("{}/graph/v1", server.uri()))
}

fn fast_client(server: &MockServer) -> S2Client {
    S2Client::new_with_base_url("test-key".into(), format!("{}/graph/v1", server.uri()))
        .with_retry_config(3, 0)
}

#[tokio::test]
async fn f02_1_search_returns_markdown() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/graph/v1/paper/search"))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({
            "total": 1, "offset": 0, "next": null,
            "data": [make_paper_json("abc123", "Attention Is All You Need")]
        })))
        .mount(&server).await;

    let client = client_for(&server);
    let result = client.search_papers("attention", 10, 0).await;
    assert!(result.is_ok());
    // The client returns SearchResponse, not formatted string
    let resp = result.unwrap();
    assert_eq!(resp.data.len(), 1);
    assert_eq!(resp.data[0].title.as_deref(), Some("Attention Is All You Need"));
}

#[tokio::test]
async fn f02_3_search_no_results() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/graph/v1/paper/search"))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({
            "total": 0, "offset": 0, "next": null, "data": []
        })))
        .mount(&server).await;

    let client = client_for(&server);
    let result = client.search_papers("xyzzy", 10, 0).await;
    assert!(result.is_ok());
    assert_eq!(result.unwrap().data.len(), 0);
}

#[tokio::test]
async fn f03_1_lookup_by_s2_id() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/graph/v1/paper/abc123"))
        .respond_with(ResponseTemplate::new(200).set_body_json(make_paper_json("abc123", "BERT")))
        .mount(&server).await;

    let client = client_for(&server);
    let result = client.get_paper("abc123").await;
    assert!(result.is_ok());
    assert_eq!(result.unwrap().title.as_deref(), Some("BERT"));
}

#[tokio::test]
async fn f03_4_nonexistent_paper_returns_not_found() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/graph/v1/paper/does-not-exist"))
        .respond_with(ResponseTemplate::new(404))
        .mount(&server).await;

    let client = client_for(&server);
    let result = client.get_paper("does-not-exist").await;
    assert!(result.is_err());
    let err = result.unwrap_err();
    match err {
        ApiError::UserFacing(msg) => {
            assert!(msg.contains("Not found"), "expected 'Not found' in: {msg}");
        }
        other => panic!("expected UserFacing, got: {other}"),
    }
}

#[tokio::test]
async fn f04_1_get_references() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/graph/v1/paper/abc123/references"))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({
            "offset": 0, "next": null,
            "data": [{"citedPaper": make_paper_json("ref1", "Reference Paper")}]
        })))
        .mount(&server).await;

    let client = client_for(&server);
    let result = client.get_references("abc123", 20).await;
    assert!(result.is_ok());
    let resp = result.unwrap();
    assert_eq!(resp.data.len(), 1);
    assert_eq!(resp.data[0].cited_paper.title.as_deref(), Some("Reference Paper"));
}

#[tokio::test]
async fn f05_1_get_citations() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/graph/v1/paper/abc123/citations"))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({
            "offset": 0, "next": null,
            "data": [{"citingPaper": make_paper_json("cit1", "Citing Paper")}]
        })))
        .mount(&server).await;

    let client = client_for(&server);
    let result = client.get_citations("abc123", 20).await;
    assert!(result.is_ok());
    let resp = result.unwrap();
    assert_eq!(resp.data.len(), 1);
    assert_eq!(resp.data[0].citing_paper.title.as_deref(), Some("Citing Paper"));
}

#[tokio::test]
async fn f07_1_single_429_retried_transparently() {
    let server = MockServer::start().await;
    // First request returns 429, second returns 200
    Mock::given(method("GET"))
        .and(path("/graph/v1/paper/search"))
        .respond_with(ResponseTemplate::new(429))
        .up_to_n_times(1)
        .expect(1)
        .mount(&server).await;
    Mock::given(method("GET"))
        .and(path("/graph/v1/paper/search"))
        .respond_with(ResponseTemplate::new(200).set_body_json(json!({
            "total": 1, "offset": 0, "next": null,
            "data": [make_paper_json("abc", "Test")]
        })))
        .expect(1)
        .mount(&server).await;

    let client = fast_client(&server);
    let result = client.search_papers("test", 10, 0).await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn f07_2_all_retries_exhausted() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/graph/v1/paper/search"))
        .respond_with(ResponseTemplate::new(429))
        .expect(4)  // 1 initial + 3 retries
        .mount(&server).await;

    let client = fast_client(&server);
    let result = client.search_papers("test", 10, 0).await;
    assert!(result.is_err());
    match result.unwrap_err() {
        ApiError::UserFacing(msg) => {
            assert!(msg.to_lowercase().contains("rate limit"), "expected rate limit message in: {msg}");
        }
        other => panic!("expected UserFacing, got: {other}"),
    }
}

#[tokio::test]
async fn f07_3_network_failure_retried() {
    // Point client at a port where nothing is listening
    let listener = std::net::TcpListener::bind("127.0.0.1:0").unwrap();
    let port = listener.local_addr().unwrap().port();
    drop(listener);

    let client = S2Client::new_with_base_url(
        "test-key".into(),
        format!("http://127.0.0.1:{port}/graph/v1"),
    ).with_retry_config(1, 0);  // 1 retry only to keep test fast

    let result = client.search_papers("test", 10, 0).await;
    assert!(result.is_err());
    // After retries exhausted, returns UserFacing error
    match result.unwrap_err() {
        ApiError::UserFacing(msg) => {
            assert!(msg.to_lowercase().contains("rate limit") || msg.contains("retries"),
                "expected retry exhaustion message in: {msg}");
        }
        other => panic!("expected UserFacing after network failures, got: {other}"),
    }
}

#[tokio::test]
async fn f12_1_401_returns_actionable_error() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/graph/v1/paper/search"))
        .respond_with(ResponseTemplate::new(401))
        .mount(&server).await;

    let client = fast_client(&server);
    let result = client.search_papers("test", 10, 0).await;
    assert!(result.is_err());
    match result.unwrap_err() {
        ApiError::UserFacing(msg) => {
            assert!(msg.contains("semanticscholar.org"), "expected URL in: {msg}");
            assert!(msg.to_lowercase().contains("api key") || msg.to_lowercase().contains("invalid"),
                "expected key message in: {msg}");
        }
        other => panic!("expected UserFacing, got: {other}"),
    }
}

#[tokio::test]
async fn f12_2_401_not_retried() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/graph/v1/paper/search"))
        .respond_with(ResponseTemplate::new(401))
        .expect(1)  // exactly 1 request — no retry
        .mount(&server).await;

    let client = fast_client(&server);
    let _ = client.search_papers("test", 10, 0).await;
    // Verification happens via expect(1) — wiremock panics if more than 1 request received
}

#[tokio::test]
async fn f12_2b_403_not_retried() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/graph/v1/paper/search"))
        .respond_with(ResponseTemplate::new(403))
        .expect(1)
        .mount(&server).await;

    let client = fast_client(&server);
    let _ = client.search_papers("test", 10, 0).await;
}
