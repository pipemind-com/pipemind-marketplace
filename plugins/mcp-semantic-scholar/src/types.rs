use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct Author {
    #[serde(rename = "authorId")]
    pub author_id: Option<String>,
    pub name: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct OpenAccessPdf {
    pub url: Option<String>,
    pub status: Option<String>,
    pub license: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct ExternalIds {
    #[serde(rename = "DOI")]
    pub doi: Option<String>,
    #[serde(rename = "ArXiv")]
    pub arxiv: Option<String>,
    #[serde(rename = "CorpusId")]
    pub corpus_id: Option<u64>,
    #[serde(rename = "PubMed")]
    pub pubmed: Option<String>,
}

#[derive(Debug, Deserialize)]
pub struct Paper {
    #[serde(rename = "paperId")]
    pub paper_id: Option<String>,
    pub title: Option<String>,
    #[serde(rename = "abstract")]
    pub abstract_text: Option<String>,
    pub year: Option<u32>,
    pub authors: Option<Vec<Author>>,
    #[serde(rename = "citationCount")]
    pub citation_count: Option<u32>,
    #[serde(rename = "influentialCitationCount")]
    pub influential_citation_count: Option<u32>,
    #[serde(rename = "isOpenAccess")]
    pub is_open_access: Option<bool>,
    #[serde(rename = "openAccessPdf")]
    pub open_access_pdf: Option<OpenAccessPdf>,
    #[serde(rename = "externalIds")]
    pub external_ids: Option<ExternalIds>,
    pub url: Option<String>,
    #[serde(rename = "publicationTypes")]
    pub publication_types: Option<Vec<String>>,
    #[serde(rename = "fieldsOfStudy")]
    pub fields_of_study: Option<Vec<String>>,
}

#[derive(Debug, Deserialize)]
pub struct SearchResponse {
    pub total: Option<u64>,
    pub offset: Option<u32>,
    pub next: Option<u32>,
    pub data: Vec<Paper>,
}

#[derive(Debug, Deserialize)]
pub struct CitationWrapper {
    #[serde(rename = "citingPaper")]
    pub citing_paper: Paper,
}

#[derive(Debug, Deserialize)]
pub struct ReferenceWrapper {
    #[serde(rename = "citedPaper")]
    pub cited_paper: Paper,
}

#[derive(Debug, Deserialize)]
pub struct PaginatedCitations {
    pub offset: Option<u32>,
    pub next: Option<u32>,
    pub data: Vec<CitationWrapper>,
}

#[derive(Debug, Deserialize)]
pub struct PaginatedReferences {
    pub offset: Option<u32>,
    pub next: Option<u32>,
    pub data: Vec<ReferenceWrapper>,
}
