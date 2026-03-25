use assert_cmd::Command;
use predicates::prelude::*;
use std::time::Duration;

#[test]
fn test_missing_api_key_exits_with_error() {
    let mut cmd = Command::cargo_bin("mcp-semantic-scholar").unwrap();
    cmd.env_clear()
        .assert()
        .failure()
        .code(1)
        .stderr(predicate::str::contains("S2_API_KEY"))
        .stderr(predicate::str::contains(
            "https://www.semanticscholar.org/product/api#api-key-form",
        ))
        .stdout(predicate::str::is_empty());
}

#[test]
fn test_empty_api_key_exits_with_error() {
    let mut cmd = Command::cargo_bin("mcp-semantic-scholar").unwrap();
    cmd.env_clear()
        .env("S2_API_KEY", "")
        .assert()
        .failure()
        .code(1)
        .stderr(predicate::str::contains("S2_API_KEY"))
        .stderr(predicate::str::contains(
            "https://www.semanticscholar.org/product/api#api-key-form",
        ))
        .stdout(predicate::str::is_empty());
}

#[test]
fn test_valid_key_does_not_exit_immediately() {
    // After the API key check passes, the server blocks on stdin.
    // Write empty stdin (EOF) to cause the rmcp transport to return.
    // The transport may return an error (ConnectionClosed), but the API
    // key error path must NOT be triggered — verified by absence of the
    // S2_API_KEY error message in stderr.
    let mut cmd = Command::cargo_bin("mcp-semantic-scholar").unwrap();
    cmd.env_clear()
        .env("S2_API_KEY", "test-key-for-testing")
        .timeout(Duration::from_secs(3))
        .write_stdin(b"".as_ref())
        .assert()
        .stderr(predicate::str::contains("S2_API_KEY is not set").not())
        .stdout(predicate::str::is_empty());
}
