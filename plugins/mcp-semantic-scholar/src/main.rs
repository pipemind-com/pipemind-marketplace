use mcp_semantic_scholar::api;
use mcp_semantic_scholar::server::SemanticScholarServer;

use rmcp::ServiceExt;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt()
        .with_writer(std::io::stderr)
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "warn".into()),
        )
        .init();

    let api_key = match std::env::var("S2_API_KEY") {
        Ok(key) if !key.is_empty() => key,
        _ => {
            eprintln!("error: S2_API_KEY is not set or is empty.");
            eprintln!();
            eprintln!("The Semantic Scholar MCP server requires an API key to operate.");
            eprintln!("Get a free key at: https://www.semanticscholar.org/product/api#api-key-form");
            eprintln!();
            eprintln!("Then add it to your Claude settings (~/.claude/settings.json):");
            eprintln!(r#"  "mcpServers": {{ "mcp-semantic-scholar": {{ "env": {{ "S2_API_KEY": "YOUR_KEY" }} }} }}"#);
            std::process::exit(1);
        }
    };

    tracing::info!("S2_API_KEY present, starting with authenticated access");

    let client = api::S2Client::new(api_key);
    let server = SemanticScholarServer::new(client);

    let service = server.serve(rmcp::transport::io::stdio()).await?;
    service.waiting().await?;

    Ok(())
}
