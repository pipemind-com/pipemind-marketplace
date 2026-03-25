use crate::types::*;

const ATTRIBUTION: &str = "\n---\n*Data provided by Semantic Scholar*";

pub fn format_search_results(resp: &SearchResponse) -> String {
    let total = resp.total.unwrap_or(0);
    let offset = resp.offset.unwrap_or(0);
    let count = resp.data.len();

    if count == 0 {
        let mut out = String::from("## Search Results\n\n0 results found\n");
        out.push_str(ATTRIBUTION);
        return out;
    }

    let mut out = format!(
        "## Search Results\n\nShowing {}-{} of {} results\n",
        offset + 1,
        offset as usize + count,
        total
    );

    for (i, paper) in resp.data.iter().enumerate() {
        out.push_str(&format!("\n### {}. ", offset as usize + i + 1));
        out.push_str(&format_paper_inline(paper));
    }

    if let Some(next) = resp.next {
        out.push_str(&format!(
            "\n*Next page: offset={next} (pass as `offset` to get more results)*\n"
        ));
    }

    out.push_str(ATTRIBUTION);
    out
}

pub fn format_paper_detail(paper: &Paper) -> String {
    let mut out = String::from("## Paper Details\n\n");
    out.push_str(&format_paper_inline(paper));

    if let Some(ref abstract_text) = paper.abstract_text {
        if !abstract_text.is_empty() {
            out.push_str(&format!("\n**Abstract:**\n> {}\n", abstract_text));
        }
    }

    out.push_str(ATTRIBUTION);
    out
}

pub fn format_references(paper_id: &str, resp: &PaginatedReferences) -> String {
    let papers: Vec<&Paper> = resp.data.iter().map(|w| &w.cited_paper).collect();
    let mut out = format!(
        "## References of {}\n\nPapers cited by this paper ({} shown):\n",
        paper_id,
        papers.len()
    );
    for (i, paper) in papers.iter().enumerate() {
        out.push_str(&format!("\n### {}. ", i + 1));
        out.push_str(&format_paper_inline(paper));
    }
    out.push_str(ATTRIBUTION);
    out
}

pub fn format_citations(paper_id: &str, resp: &PaginatedCitations) -> String {
    let papers: Vec<&Paper> = resp.data.iter().map(|w| &w.citing_paper).collect();
    let mut out = format!(
        "## Citations of {}\n\nPapers that cite this paper ({} shown):\n",
        paper_id,
        papers.len()
    );
    for (i, paper) in papers.iter().enumerate() {
        out.push_str(&format!("\n### {}. ", i + 1));
        out.push_str(&format_paper_inline(paper));
    }
    out.push_str(ATTRIBUTION);
    out
}

fn format_paper_inline(paper: &Paper) -> String {
    let title = paper.title.as_deref().unwrap_or("Untitled");
    let year = paper
        .year
        .map(|y| format!(" ({y})"))
        .unwrap_or_default();
    let mut out = format!("{title}{year}\n");

    if let Some(ref authors) = paper.authors {
        let names: Vec<&str> = authors
            .iter()
            .filter_map(|a| a.name.as_deref())
            .collect();
        if !names.is_empty() {
            out.push_str(&format!("**Authors:** {}\n", names.join(", ")));
        }
    }

    let citations = paper.citation_count.unwrap_or(0);
    let influential = paper.influential_citation_count.unwrap_or(0);
    out.push_str(&format!(
        "**Citations:** {citations} ({influential} influential)\n"
    ));

    if let Some(ref ids) = paper.external_ids {
        let mut id_parts = Vec::new();
        if let Some(ref doi) = ids.doi {
            id_parts.push(format!("DOI: {doi}"));
        }
        if let Some(ref arxiv) = ids.arxiv {
            id_parts.push(format!("ArXiv: {arxiv}"));
        }
        if let Some(ref pubmed) = ids.pubmed {
            id_parts.push(format!("PubMed: {pubmed}"));
        }
        if !id_parts.is_empty() {
            out.push_str(&format!("**IDs:** {}\n", id_parts.join(" | ")));
        }
    }

    if let Some(true) = paper.is_open_access {
        let mut oa_line = String::from("**Open Access:** Yes");
        if let Some(ref pdf) = paper.open_access_pdf {
            if let Some(ref status) = pdf.status {
                if !status.is_empty() && status != "CLOSED" {
                    oa_line.push_str(&format!(" ({status})"));
                }
            }
            if let Some(ref license) = pdf.license {
                if !license.is_empty() {
                    oa_line.push_str(&format!(" — License: {license}"));
                }
            }
            if let Some(ref url) = pdf.url {
                if !url.is_empty() {
                    oa_line.push_str(&format!(" — [PDF]({url})"));
                }
            }
        }
        out.push_str(&oa_line);
        out.push('\n');
    }

    if let Some(ref types) = paper.publication_types {
        if !types.is_empty() {
            out.push_str(&format!("**Type:** {}\n", types.join(", ")));
        }
    }

    if let Some(ref fields) = paper.fields_of_study {
        if !fields.is_empty() {
            out.push_str(&format!("**Fields:** {}\n", fields.join(", ")));
        }
    }

    if let Some(ref url) = paper.url {
        out.push_str(&format!("**URL:** {url}\n"));
    }

    if let Some(ref id) = paper.paper_id {
        out.push_str(&format!("**S2 ID:** {id}\n"));
    }

    out
}

#[cfg(test)]
mod tests {
    use super::*;

    fn minimal_paper() -> Paper {
        Paper {
            paper_id: None,
            title: Some("Test Paper".to_string()),
            abstract_text: None,
            year: None,
            authors: None,
            citation_count: None,
            influential_citation_count: None,
            is_open_access: None,
            open_access_pdf: None,
            external_ids: None,
            url: None,
            publication_types: None,
            fields_of_study: None,
        }
    }

    // ── format_search_results ────────────────────────────────────────────────

    #[test]
    fn test_format_search_empty_results() {
        let resp = SearchResponse {
            total: Some(0),
            offset: None,
            next: None,
            data: vec![],
        };
        let out = format_search_results(&resp);
        assert!(out.contains("0 results found"), "expected '0 results found'");
        assert!(out.ends_with(ATTRIBUTION), "expected ATTRIBUTION footer");
        assert!(!out.contains("Showing"), "should not contain 'Showing'");
    }

    #[test]
    fn test_format_search_single_result() {
        let resp = SearchResponse {
            total: Some(1),
            offset: None,
            next: None,
            data: vec![minimal_paper()],
        };
        let out = format_search_results(&resp);
        assert!(out.contains("Showing 1-1 of 1"), "expected 'Showing 1-1 of 1'");
        assert!(out.contains("### 1."), "expected '### 1.'");
        assert!(!out.contains("Next page"), "should not contain 'Next page'");
    }

    #[test]
    fn test_format_search_pagination_next_line() {
        let resp = SearchResponse {
            total: Some(100),
            offset: None,
            next: Some(10),
            data: vec![minimal_paper()],
        };
        let out = format_search_results(&resp);
        assert!(
            out.contains("Next page: offset=10"),
            "expected 'Next page: offset=10'"
        );
    }

    #[test]
    fn test_format_search_offset_numbering() {
        let resp = SearchResponse {
            total: Some(30),
            offset: Some(10),
            next: None,
            data: vec![minimal_paper(), minimal_paper()],
        };
        let out = format_search_results(&resp);
        assert!(out.contains("Showing 11-12 of 30"), "expected 'Showing 11-12 of 30'");
        assert!(out.contains("### 11."), "expected '### 11.'");
        assert!(out.contains("### 12."), "expected '### 12.'");
    }

    // ── format_paper_inline (via format_paper_detail) ───────────────────────

    #[test]
    fn test_f08_1_null_fields_omitted() {
        let paper = Paper {
            title: Some("Minimal".to_string()),
            ..minimal_paper()
        };
        let out = format_paper_detail(&paper);
        assert!(!out.contains("null"), "should not contain 'null'");
        assert!(!out.contains("N/A"), "should not contain 'N/A'");
        assert!(!out.contains("Unknown"), "should not contain 'Unknown'");
        assert!(!out.contains("Abstract"), "should not contain 'Abstract'");
        assert!(!out.contains("Fields"), "should not contain 'Fields'");
        assert!(!out.contains("**IDs:**"), "should not contain '**IDs:**'");
    }

    #[test]
    fn test_f08_2_open_access_full() {
        let paper = Paper {
            is_open_access: Some(true),
            open_access_pdf: Some(OpenAccessPdf {
                url: Some("https://example.com/paper.pdf".to_string()),
                status: Some("GREEN".to_string()),
                license: Some("CC-BY".to_string()),
            }),
            ..minimal_paper()
        };
        let out = format_paper_detail(&paper);
        assert!(out.contains("**Open Access:** Yes"), "expected '**Open Access:** Yes'");
        assert!(out.contains("(GREEN)"), "expected '(GREEN)'");
        assert!(out.contains("License: CC-BY"), "expected 'License: CC-BY'");
        assert!(
            out.contains("[PDF](https://example.com/paper.pdf)"),
            "expected PDF link"
        );
    }

    #[test]
    fn test_f08_2_open_access_no_pdf_url() {
        let paper = Paper {
            is_open_access: Some(true),
            open_access_pdf: None,
            ..minimal_paper()
        };
        let out = format_paper_detail(&paper);
        assert!(out.contains("**Open Access:** Yes"), "expected '**Open Access:** Yes'");
        assert!(!out.contains("[PDF]"), "should not contain '[PDF]'");
        assert!(!out.contains("License"), "should not contain 'License'");
    }

    #[test]
    fn test_f08_2_open_access_closed_status_suppressed() {
        let paper = Paper {
            is_open_access: Some(true),
            open_access_pdf: Some(OpenAccessPdf {
                url: None,
                status: Some("CLOSED".to_string()),
                license: None,
            }),
            ..minimal_paper()
        };
        let out = format_paper_detail(&paper);
        assert!(out.contains("**Open Access:** Yes"), "expected '**Open Access:** Yes'");
        assert!(!out.contains("CLOSED"), "should not contain 'CLOSED'");
    }

    #[test]
    fn test_f08_3_external_ids_all_three() {
        let paper = Paper {
            external_ids: Some(ExternalIds {
                doi: Some("10.1234/test".to_string()),
                arxiv: Some("2301.00001".to_string()),
                pubmed: Some("12345678".to_string()),
                corpus_id: None,
            }),
            ..minimal_paper()
        };
        let out = format_paper_detail(&paper);
        assert!(out.contains("DOI: 10.1234/test"), "expected DOI");
        assert!(out.contains("ArXiv: 2301.00001"), "expected ArXiv");
        assert!(out.contains("PubMed: 12345678"), "expected PubMed");
        assert!(out.contains(" | "), "expected pipe separator");
    }

    #[test]
    fn test_f08_3_external_ids_partial() {
        let paper = Paper {
            external_ids: Some(ExternalIds {
                doi: Some("10.9999/only".to_string()),
                arxiv: None,
                pubmed: None,
                corpus_id: None,
            }),
            ..minimal_paper()
        };
        let out = format_paper_detail(&paper);
        assert!(out.contains("DOI: 10.9999/only"), "expected DOI");
        assert!(!out.contains("ArXiv"), "should not contain 'ArXiv'");
        assert!(!out.contains("PubMed"), "should not contain 'PubMed'");
        assert!(!out.contains(" | "), "should not contain pipe with single ID");
    }

    #[test]
    fn test_f08_4_citation_counts_always_present() {
        let paper = Paper {
            citation_count: Some(0),
            influential_citation_count: Some(0),
            ..minimal_paper()
        };
        let out = format_paper_detail(&paper);
        assert!(
            out.contains("**Citations:** 0 (0 influential)"),
            "expected citation line"
        );
    }

    #[test]
    fn test_f08_4_citation_counts_none_defaults_zero() {
        let paper = minimal_paper(); // both counts are None
        let out = format_paper_detail(&paper);
        assert!(
            out.contains("**Citations:** 0 (0 influential)"),
            "expected default zero citation line"
        );
    }

    // ── ATTRIBUTION footer ───────────────────────────────────────────────────

    #[test]
    fn test_f08_5_attribution_footer_search() {
        let resp = SearchResponse {
            total: Some(1),
            offset: None,
            next: None,
            data: vec![minimal_paper()],
        };
        assert!(format_search_results(&resp).ends_with(ATTRIBUTION));
    }

    #[test]
    fn test_f08_5_attribution_footer_detail() {
        assert!(format_paper_detail(&minimal_paper()).ends_with(ATTRIBUTION));
    }

    #[test]
    fn test_f08_5_attribution_footer_references() {
        let resp = PaginatedReferences {
            offset: None,
            next: None,
            data: vec![],
        };
        assert!(format_references("x", &resp).ends_with(ATTRIBUTION));
    }

    #[test]
    fn test_f08_5_attribution_footer_citations() {
        let resp = PaginatedCitations {
            offset: None,
            next: None,
            data: vec![],
        };
        assert!(format_citations("x", &resp).ends_with(ATTRIBUTION));
    }

    // ── format_references ───────────────────────────────────────────────────

    #[test]
    fn test_format_references_header_and_numbering() {
        fn paper_with_title(t: &str) -> Paper {
            Paper {
                title: Some(t.to_string()),
                ..minimal_paper()
            }
        }
        let resp = PaginatedReferences {
            offset: None,
            next: None,
            data: vec![
                ReferenceWrapper { cited_paper: paper_with_title("Paper A") },
                ReferenceWrapper { cited_paper: paper_with_title("Paper B") },
            ],
        };
        let out = format_references("paper-123", &resp);
        assert!(out.contains("## References of paper-123"), "expected header");
        assert!(out.contains("2 shown"), "expected '2 shown'");
        assert!(out.contains("### 1."), "expected '### 1.'");
        assert!(out.contains("### 2."), "expected '### 2.'");
    }

    // ── format_citations ────────────────────────────────────────────────────

    #[test]
    fn test_format_citations_header_and_numbering() {
        fn paper_with_title(t: &str) -> Paper {
            Paper {
                title: Some(t.to_string()),
                ..minimal_paper()
            }
        }
        let resp = PaginatedCitations {
            offset: None,
            next: None,
            data: vec![
                CitationWrapper { citing_paper: paper_with_title("Citing A") },
                CitationWrapper { citing_paper: paper_with_title("Citing B") },
            ],
        };
        let out = format_citations("paper-456", &resp);
        assert!(out.contains("## Citations of paper-456"), "expected header");
        assert!(out.contains("2 shown"), "expected '2 shown'");
        assert!(out.contains("### 1."), "expected '### 1.'");
        assert!(out.contains("### 2."), "expected '### 2.'");
    }

    // ── author filtering ─────────────────────────────────────────────────────

    #[test]
    fn test_format_paper_inline_authors() {
        let paper = Paper {
            authors: Some(vec![
                Author { author_id: None, name: Some("Alice Smith".to_string()) },
                Author { author_id: None, name: Some("Bob Jones".to_string()) },
                Author { author_id: None, name: None },
            ]),
            ..minimal_paper()
        };
        let out = format_paper_detail(&paper);
        assert!(
            out.contains("**Authors:** Alice Smith, Bob Jones"),
            "expected two named authors, None filtered out"
        );
    }
}
