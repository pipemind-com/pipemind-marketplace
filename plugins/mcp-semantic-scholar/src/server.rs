use rmcp::handler::server::router::tool::ToolRouter;
use rmcp::handler::server::wrapper::Parameters;
use rmcp::model::*;
use rmcp::schemars::JsonSchema;
use rmcp::tool;
use rmcp::ServerHandler;
use serde::Deserialize;

use crate::api::{ApiError, S2Client};
use crate::format;

const ATTRIBUTION: &str = "\n---\n*Data provided by Semantic Scholar*";

fn map_api_err(e: ApiError) -> Result<String, String> {
    match e {
        ApiError::UserFacing(msg) => Ok(msg),
        ApiError::Internal(msg) => Err(msg),
    }
}

#[derive(Clone)]
pub struct SemanticScholarServer {
    client: S2Client,
    tool_router: ToolRouter<Self>,
}

impl SemanticScholarServer {
    pub fn new(client: S2Client) -> Self {
        let tool_router = Self::tool_router();
        Self {
            client,
            tool_router,
        }
    }
}

#[derive(Debug, Deserialize, JsonSchema)]
pub struct SearchPapersParams {
    /// Natural language search query (e.g., "transformer attention mechanism")
    pub query: String,
    /// Maximum number of results to return (1-100, default 10)
    pub limit: Option<u32>,
    /// Pagination offset (default 0). Use the `next` value from a previous search to get more results.
    pub offset: Option<u32>,
}

#[derive(Debug, Deserialize, JsonSchema)]
pub struct GetPaperParams {
    /// Paper identifier. Accepts: Semantic Scholar ID, DOI:10.xxx/xxx, ArXiv:2301.xxxxx, or CorpusId:12345
    pub paper_id: String,
}

#[derive(Debug, Deserialize, JsonSchema)]
pub struct GetReferencesParams {
    /// Paper identifier (same formats as get_paper)
    pub paper_id: String,
    /// Maximum references to return (1-1000, default 20)
    pub limit: Option<u32>,
}

#[derive(Debug, Deserialize, JsonSchema)]
pub struct GetCitationsParams {
    /// Paper identifier (same formats as get_paper)
    pub paper_id: String,
    /// Maximum citations to return (1-1000, default 20)
    pub limit: Option<u32>,
}

#[rmcp::tool_router]
impl SemanticScholarServer {
    #[tool(
        name = "search_papers",
        description = "Search for academic papers by keyword or natural language query. Returns papers with titles, authors, citation counts, and open access PDF links."
    )]
    async fn search_papers(
        &self,
        Parameters(params): Parameters<SearchPapersParams>,
    ) -> Result<String, String> {
        if params.query.trim().is_empty() {
            return Ok(format!("Search query cannot be empty{ATTRIBUTION}"));
        }
        let limit = params.limit.unwrap_or(10).min(100);
        let offset = params.offset.unwrap_or(0);
        self.client
            .search_papers(&params.query, limit, offset)
            .await
            .map(|resp| format::format_search_results(&resp))
            .or_else(|e| map_api_err(e))
    }

    #[tool(
        name = "get_paper",
        description = "Get detailed information about a specific paper by its identifier. Accepts Semantic Scholar ID, DOI (e.g. DOI:10.xxx), ArXiv ID (e.g. ArXiv:2301.xxxxx), or Corpus ID."
    )]
    async fn get_paper(
        &self,
        Parameters(params): Parameters<GetPaperParams>,
    ) -> Result<String, String> {
        self.client
            .get_paper(&params.paper_id)
            .await
            .map(|paper| format::format_paper_detail(&paper))
            .or_else(|e| map_api_err(e))
    }

    #[tool(
        name = "get_references",
        description = "Get papers cited BY a given paper (backward citation snowball). Useful for finding foundational work a paper builds upon."
    )]
    async fn get_references(
        &self,
        Parameters(params): Parameters<GetReferencesParams>,
    ) -> Result<String, String> {
        let limit = params.limit.unwrap_or(20).min(1000);
        self.client
            .get_references(&params.paper_id, limit)
            .await
            .map(|resp| format::format_references(&params.paper_id, &resp))
            .or_else(|e| map_api_err(e))
    }

    #[tool(
        name = "get_citations",
        description = "Get papers that CITE a given paper (forward citation snowball). Useful for finding recent work building on a foundational paper."
    )]
    async fn get_citations(
        &self,
        Parameters(params): Parameters<GetCitationsParams>,
    ) -> Result<String, String> {
        let limit = params.limit.unwrap_or(20).min(1000);
        self.client
            .get_citations(&params.paper_id, limit)
            .await
            .map(|resp| format::format_citations(&params.paper_id, &resp))
            .or_else(|e| map_api_err(e))
    }
}

#[rmcp::tool_handler]
impl ServerHandler for SemanticScholarServer {
    fn get_info(&self) -> ServerInfo {
        let capabilities = ServerCapabilities::builder()
            .enable_tools()
            .build();
        InitializeResult::new(capabilities)
            .with_server_info(Implementation::new(
                "mcp-semantic-scholar",
                env!("CARGO_PKG_VERSION"),
            ))
            .with_instructions(
                "Semantic Scholar MCP server — search 200M+ academic papers, \
                 fetch citation graphs, and discover references. \
                 Data provided by Semantic Scholar.",
            )
    }
}
