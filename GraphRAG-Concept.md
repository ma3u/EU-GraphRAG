# EU GraphRAG - Detailed Concept Document

## Executive Summary

The EU GraphRAG (Graph Retrieval-Augmented Generation) system is a comprehensive knowledge graph solution designed to structure, interconnect, and provide intelligent access to European Union regulations, German legal documents (especially SGB), and cross-border legal information. Building upon the foundation of the SGB RAG and Gesetze im Internet projects, this system leverages Neo4j graph database technology combined with advanced AI/LLM capabilities to enable precise legal research, regulatory compliance, and transposition analysis.

## 1. Project Overview

### 1.1 Vision
Create the first production-ready GraphRAG system for EU regulatory compliance that:
- Natively integrates ELI (European Legislation Identifier) and ECLI (European Case Law Identifier) standards
- Supports multi-jurisdictional legal knowledge representation
- Enables automated EU-to-national law transposition analysis
- Provides temporal tracking of legal amendments and their impacts

### 1.2 Core Objectives
1. **Unified Legal Knowledge Graph**: Integrate EU law, German federal law (SGB, BGB, StGB, etc.), and case law into a single queryable graph
2. **Semantic Interoperability**: Implement ELI, ECLI, and EuroVoc ontologies for cross-border compatibility
3. **Intelligent Retrieval**: Enable GraphRAG-based question answering with source-grounded responses
4. **Transposition Tracking**: Automated analysis of how EU directives/regulations map to national implementation
5. **Temporal Intelligence**: Track legal amendments over time with SUPERSEDED_BY relationships

### 1.3 Target Users
- Government agencies (BA, DRV, federal/state ministries)
- Legal professionals in public sector
- Policy analysts and legislators
- Compliance officers in regulated industries
- Legal tech companies and researchers

## 2. Technical Architecture

### 2.1 Core Technology Stack

#### Graph Database
- **Neo4j 5.x** (Community Edition for development, Enterprise for production)
- **APOC Library**: Graph algorithms and advanced procedures
- **Graph Data Science Library**: Community detection, embeddings
- **Native Vector Search**: For hybrid semantic-graph retrieval

#### LLM Integration
- **OpenAI GPT-4** or **Azure OpenAI**: Entity extraction, relationship identification
- **Local LLMs (optional)**: Llama 3, Mistral for sensitive data
- **Embedding Models**: text-embedding-3-large or multilingual-e5-large

#### Application Framework
- **Python 3.11+**: Primary development language
- **LangChain/LlamaIndex**: LLM orchestration and GraphRAG patterns
- **FastAPI**: REST API for query interface
- **Streamlit**: Interactive UI for demonstration

#### Data Processing
- **Apache Airflow**: ETL orchestration
- **Beautiful Soup/Scrapy**: Web scraping for Gesetze im Internet
- **EUR-Lex API**: EU legislation retrieval
- **XML/RDF parsing**: ELI/ECLI metadata extraction

### 2.2 Graph Data Model

#### Core Node Types

**1. LegalDocument**
- Properties: eli_uri, title, document_type (directive/regulation/law), effective_date, publication_date, status
- Subtypes: EUDirective, EURegulation, GermanLaw, CourtDecision

**2. Article/Section**
- Properties: article_number, title, text_content, eli_uri (with fragment)
- Hierarchical structure: Chapter → Section → Paragraph

**3. LegalConcept**
- Properties: concept_id, preferred_label, alt_labels, eurovoc_id, domain
- Based on EuroVoc thesaurus descriptors

**4. Organization**
- Properties: name, org_type (ministry/agency/court), country_code, eli_court_code

**5. TemporalVersion**
- Properties: version_date, consolidation_status, change_description
- Represents specific versions of articles/laws

**6. Amendment**
- Properties: amendment_date, amendment_type, description
- Links versions of legal texts

#### Core Relationship Types

**1. IMPLEMENTS** (EUDirective → GermanLaw)
- Properties: transposition_deadline, implementation_status, mapping_confidence

**2. REFERENCES** (Article → Article)
- Properties: reference_type (cites/amends/repeals), context

**3. SUPERSEDES** (TemporalVersion → TemporalVersion)
- Properties: change_date, change_reason

**4. BELONGS_TO** (Article → LegalDocument)
- Properties: hierarchical_position

**5. CONCERNS** (LegalDocument → LegalConcept)
- Properties: relevance_score, eurovoc_descriptor

**6. DECIDED_BY** (CourtDecision → Organization)
- Properties: ecli_uri, decision_date

**7. IMPACTS** (Amendment → BusinessProcess)
- Properties: impact_type, affected_entities

### 2.3 Ontology Integration

#### ELI (European Legislation Identifier)
- **Pillar I**: Web identifiers (URIs) for legal resources
- **Pillar II**: Metadata ontology (Work, Expression, Manifestation, Item)
- Implementation: Each legal document has canonical ELI URI
- Example: `http://data.europa.eu/eli/dir/2016/680/oj`

#### ECLI (European Case Law Identifier)
- Format: `ECLI:{country}:{court}:{year}:{identifier}`
- Metadata: Dublin Core elements (title, creator, date, subject, type)
- Integration: CourtDecision nodes have ECLI as primary identifier

#### EuroVoc Thesaurus
- 21 domains, 127 microthesauri, ~7,000 concepts
- Multilingual (24 EU languages)
- Implementation: LegalConcept nodes mapped to EuroVoc descriptors
- Enables multilingual search and cross-border legal discovery

#### SGB-Specific Ontology
- Social law domain model
- Books (SGB I-XII): Different social benefit areas
- Benefit types: Health insurance, pension, unemployment, nursing care
- Process mapping: Administrative procedures, entitlements, appeals

### 2.4 GraphRAG Architecture

#### Indexing Pipeline

**1. Document Ingestion**
- Scrape/API retrieve: Gesetze im Internet, EUR-Lex, court databases
- Parse: XML, HTML, PDF extraction
- Normalize: UTF-8, clean formatting

**2. Entity Extraction (LLM-based)**
- Extract: Organizations, legal concepts, dates, references
- Classify: Document type, subject matter
- Validation: Human-in-the-loop for critical entities

**3. Graph Construction**
- Create nodes: Documents, articles, concepts
- Establish relationships: References, implementations, amendments
- Link to ontologies: ELI URIs, EuroVoc descriptors

**4. Embedding Generation**
- Article-level embeddings: Dense vector representations
- Concept embeddings: Semantic similarity search
- Community summaries: Hierarchical GraphRAG approach

**5. Quality Assurance**
- Verify ELI/ECLI compliance
- Check relationship consistency
- Validate temporal chains (SUPERSEDES)

#### Query Pipeline (Hybrid GraphRAG)

**1. Query Understanding**
- Parse user question
- Identify: Entities, time constraints, jurisdictions
- Classify: Query type (factual/analytical/comparative)

**2. Hybrid Retrieval**
- **Vector Search**: Semantic similarity on article embeddings
- **Graph Traversal**: Relationship-based context expansion
  - REFERENCES relationships → cited articles
  - IMPLEMENTS relationships → related EU/national laws
  - SUPERSEDES relationships → historical versions
- **Community-based**: Leiden algorithm clusters for global queries

**3. Context Assembly**
- Rank retrieved articles/concepts
- Assemble: Primary sources + related context
- Limit: Token budget for LLM (e.g., 8k context window)

**4. Answer Generation**
- LLM generates response with context
- Cite sources: ELI/ECLI URIs, article numbers
- Hallucination prevention: Grounded in graph data

**5. Validation & Enrichment**
- Cross-check citations against graph
- Add metadata: Effective dates, amendment status
- Format: User-friendly with legal references

## 3. Data Sources

### 3.1 EU Sources
- **EUR-Lex**: Official EU legal database (SPARQL endpoint, REST API)
- **CELLAR**: Publications Office repository (ELI/ECLI metadata)
- **EUR-Lex N-Lex**: Gateway to national legislation
- **Court of Justice (CJEU)**: Case law with ECLI

### 3.2 German Sources
- **Gesetze im Internet**: ~5,000 federal laws (HTML/XML scraping)
- **Bundesgesetzblatt**: Official law gazette (BGBl I & II)
- **Bundesrat/Bundestag**: Legislative materials (DIP system)
- **Federal Courts**: Bundesverfassungsgericht, BGH, BVerwG (ECLI compliant)

### 3.3 SGB-Specific
- SGB I-XII: Complete books with amendments
- BA regulations: Employment services, SGB II/III
- DRV regulations: Pension insurance, SGB VI
- Commentaries: Cross-references to case law

## 4. Key Features & Differentiation

### 4.1 Unique Capabilities

**Amendment Tracking**
- Temporal SUPERSEDES chains track every version of legal text
- Query historical state: "What did SGB VI § 43 say in 2020?"
- Impact analysis: "Which provisions were affected by BGBl 2023 I Nr. 123?"

**EU Transposition Automation**
- IMPLEMENTS relationships link EU directives to national laws
- Gap analysis: Identify unimplemented EU requirements
- Deadline tracking: Monitor transposition obligations

**Process Impact Visualization**
- IMPACTS relationships connect legal changes to operational procedures
- Business process nodes represent BA/DRV workflows
- Cost estimation: Predict administrative burden of amendments

**Multilingual Support**
- EuroVoc-based concept mapping across 24 EU languages
- Parallel text storage (DE/EN/FR for major directives)
- Cross-language search: Query in English, retrieve German law

### 4.2 GraphRAG Advantages over Traditional RAG

| Aspect | Traditional RAG | GraphRAG (This System) |
|--------|----------------|------------------------|
| **Retrieval** | Vector similarity on chunks | Hybrid: vectors + graph traversal |
| **Relationships** | Implicit (in embeddings) | Explicit (REFERENCES, IMPLEMENTS) |
| **Temporal** | Latest version only | Full amendment history (SUPERSEDES) |
| **Citations** | Page numbers, chunks | ELI/ECLI URIs, precise articles |
| **Multi-hop** | Limited (context window) | Unlimited (graph paths) |
| **Structured queries** | Not supported | Cypher + natural language |

## 5. Implementation Roadmap

### Phase 1: Foundation (Months 1-3)
**Goals**: Working prototype with SGB core

- Set up Neo4j database (local + AuraDB cloud)
- Create GitHub repository (public, MIT license)
- Implement ELI ontology schema (Cypher CREATE statements)
- Build web scraper for Gesetze im Internet
- Ingest SGB I-III (~500 articles)
- Basic retrieval: Cypher queries for law lookup
- **Milestone**: Demo Q&A on SGB provisions

### Phase 2: GraphRAG Core (Months 4-6)
**Goals**: LLM-powered intelligent retrieval

- LLM entity extraction pipeline (GPT-4 + validation)
- Relationship identification (REFERENCES, cites)
- Generate embeddings for all articles
- Hybrid retrieval implementation (vector + graph)
- Streamlit Q&A interface
- 100% test coverage for core modules
- **Milestone**: >85% answer accuracy on test set

### Phase 3: EU Integration (Months 7-9)
**Goals**: Cross-border legal knowledge graph

- EUR-Lex API integration
- EuroVoc concept mapping (7,000+ descriptors)
- ECLI case law ingestion (German supreme courts)
- EU-to-German transposition tracking (pilot: 10 directives)
- Multilingual support (DE/EN/FR)
- **Milestone**: Live demo at EU Digital Assembly

### Phase 4: Production (Months 10-12)
**Goals**: Production-ready system for BA/DRV

- FastAPI REST service with authentication
- Performance optimization (caching, indexing)
- BA/DRV pilot deployment (2 agencies)
- User training and documentation
- Open-source community building
- **Milestone**: €500K+ EU funding secured

## 6. Use Cases

### 6.1 Regulatory Compliance Assistant
**User**: BA compliance officer
**Query**: "What changed in SGB II § 7 since January 2023?"

**GraphRAG Process**:
1. Identify node: SGB II § 7
2. Traverse SUPERSEDES relationships (filter: date >= 2023-01-01)
3. Retrieve: Amendment nodes, new/old TemporalVersions
4. LLM generates summary with BGBl citations

**Output**:
> "SGB II § 7 was amended twice since January 2023:
> 1. **BGBl I 2023 Nr. 45 (effective 2023-03-01)**: Extended eligibility criteria for single parents...
> 2. **BGBl I 2023 Nr. 234 (effective 2023-10-01)**: Adjusted income thresholds to €1,200/month...
> 
> ELI: http://data.europa.eu/eli/de/sgb/2/7/2023-10-01"

### 6.2 EU Transposition Analysis
**User**: Ministry of Labor policy analyst
**Query**: "Which German laws implement the EU Data Act (2023/2854)?"

**GraphRAG Process**:
1. Find EURegulation node (eli:reg/2023/2854)
2. Traverse all IMPLEMENTS relationships
3. Retrieve: Connected GermanLaw nodes
4. Analyze: Implementation status, gaps

**Output**:
> "The EU Data Act (Regulation 2023/2854) is partially implemented in Germany through:
> 
> **Fully implemented**:
> - Datengesetz (Data Act Implementation Law, BGBl I 2024 Nr. 78)
>   - Articles 4-7 → § 3-12 DatenG
> 
> **Partially implemented**:
> - Telekommunikationsgesetz (TKG) § 98a (data portability)
>   - Covers Articles 8-9 only
> 
> **Not yet implemented** (Deadline: 2025-09-12):
> - Articles 12-14 (data altruism)
> - Requires new legislation or amendment to existing laws
> 
> ELI: http://data.europa.eu/eli/reg/2023/2854/oj"

### 6.3 Cross-Border Social Security
**User**: Legal researcher
**Query**: "How does SGB VI (German pension law) interact with EU Regulation 883/2004 on social security coordination?"

**GraphRAG Process**:
1. Find nodes: SGB VI, EU Reg 883/2004
2. Traverse REFERENCES relationships (bidirectional)
3. Identify: Relevant articles in both
4. Extract: Coordination rules, conflicts

**Output**:
> "SGB VI coordinates with EU Regulation 883/2004 in the following areas:
> 
> **Applicable Legislation (Art. 11-16)**:
> - SGB VI § 3 defines German pension insurance coverage
> - Defers to EU Reg 883/2004 Art. 11(3)(a) for cross-border workers
> 
> **Aggregation of Periods (Art. 6)**:
> - SGB VI § 55 allows counting foreign insurance periods
> - References EU Reg 883/2004 Art. 6 and Annex VI
> 
> **Calculation of Benefits (Art. 52)**:
> - SGB VI § 63 implements pro-rata calculation
> - Follows EU Reg 883/2004 Art. 52(1)(b) formula
> 
> ELI URIs:
> - http://data.europa.eu/eli/reg/2004/883/oj
> - http://data.europa.eu/eli/de/sgb/6/oj"

### 6.4 Impact Analysis
**User**: DRV operations manager
**Query**: "Which processes would be affected if SGB VI § 43 (disability pension) changes its income threshold?"

**GraphRAG Process**:
1. Identify node: SGB VI § 43
2. Traverse IMPACTS relationships
3. Retrieve: BusinessProcess nodes
4. LLM enriches with operational context

**Output**:
> "Changing the income threshold in SGB VI § 43 would impact the following DRV processes:
> 
> **Process 1: Disability Pension Application (DRV-P-001)**
> - Affected step: Income verification (Step 4)
> - Estimated case volume: ~45,000 applications/year
> - IT change required: Update income calculation module
> 
> **Process 2: Ongoing Entitlement Review (DRV-P-012)**
> - Affected step: Annual income check (Step 2)
> - Estimated case volume: ~320,000 reviews/year
> - IT change required: Modify automated income comparison
> 
> **Process 3: Appeals Handling (DRV-P-033)**
> - Affected step: Eligibility reassessment (Step 3)
> - Estimated case volume: ~8,000 appeals/year
> - Training required: New guidelines for caseworkers
> 
> **Estimated implementation cost**: €1.2M (IT) + €300K (training)
> **Timeline**: 9-12 months for full rollout"

## 7. Ontology Structure

### 7.1 ELI Ontology Implementation

```cypher
// ELI Work (abstract legal act)
CREATE (work:ELIWork {
  eli_uri: 'http://data.europa.eu/eli/dir/2016/680',
  type: 'directive',
  date_document: date('2016-04-27'),
  title_de: 'Richtlinie über den Schutz natürlicher Personen...',
  title_en: 'Directive on the protection of natural persons...'
})

// ELI Expression (language version)
CREATE (expr:ELIExpression {
  eli_uri: 'http://data.europa.eu/eli/dir/2016/680/oj',
  language: 'deu',
  date_publication: date('2016-05-04')
})-[:REALIZES]->(work)

// ELI Manifestation (format)
CREATE (manif:ELIManifes tation {
  eli_uri: 'http://data.europa.eu/eli/dir/2016/680/oj/deu/html',
  format: 'text/html',
  access_url: 'https://eur-lex.europa.eu/...'
})-[:EMBODIES]->(expr)

// Articles (fragments)
CREATE (art5:Article {
  eli_uri: 'http://data.europa.eu/eli/dir/2016/680/oj#art_5',
  article_number: '5',
  title: 'Rechtmäßigkeit der Verarbeitung',
  text_content: '...'
})-[:PART_OF]->(expr)
```

### 7.2 ECLI Ontology Implementation

```cypher
// Court Decision with ECLI
CREATE (decision:CourtDecision {
  ecli: 'ECLI:DE:BGH:2023:120723U2STR456.22.0',
  title: 'BGH Urteil vom 12.07.2023 - 2 StR 456/22',
  decision_date: date('2023-07-12'),
  decision_type: 'Urteil',
  language: 'deu'
})

// Court
CREATE (court:Court {
  name: 'Bundesgerichtshof',
  court_code: 'BGH',
  country: 'DE',
  jurisdiction: 'federal'
})<-[:DECIDED_BY]-(decision)

// Subject matter (EuroVoc)
CREATE (concept:LegalConcept {
  eurovoc_id: '3815',
  pref_label_de: 'Strafverfahren',
  pref_label_en: 'criminal procedure'
})<-[:CONCERNS]-(decision)

// References to legal provisions
CREATE (decision)-[:CITES {
  reference_type: 'applies',
  article: '§ 261 StPO'
}]->(stpo_article:Article {
  eli_uri: 'http://data.europa.eu/eli/de/stpo/261/oj'
})
```

### 7.3 EuroVoc Integration

```cypher
// EuroVoc Domain
CREATE (domain:EuroVocDomain {
  code: '12',
  label_de: 'Recht',
  label_en: 'law'
})

// EuroVoc Microthesaurus
CREATE (mt:EuroVocMicrothesaurus {
  code: '1206',
  label_de: 'Arbeitsrecht',
  label_en: 'labour law'
})-[:BELONGS_TO]->(domain)

// EuroVoc Descriptor
CREATE (desc:LegalConcept {
  eurovoc_id: '3141',
  pref_label_de: 'Arbeitsvertrag',
  pref_label_en: 'employment contract',
  pref_label_fr: 'contrat de travail',
  alt_labels_de: ['Dienstvertrag', 'Anstellungsvertrag']
})-[:IN_MICROTHESAURUS]->(mt)

// Broader/Narrower relationships
CREATE (desc)-[:BROADER_THAN]->(desc2:LegalConcept {
  eurovoc_id: '3140',
  pref_label_de: 'Arbeitsbeziehungen'
})

// Link legal documents to concepts
CREATE (sgb_article:Article {
  eli_uri: 'http://data.europa.eu/eli/de/sgb/3/611/oj',
  article_number: '611',
  title: 'Arbeitsvertrag'
})-[:CONCERNS {
  relevance_score: 0.95
}]->(desc)
```

### 7.4 SGB-Specific Extension

```cypher
// SGB Book
CREATE (sgb6:SocialLawBook {
  eli_uri: 'http://data.europa.eu/eli/de/sgb/6/oj',
  book_number: 'VI',
  title: 'Gesetzliche Rentenversicherung',
  title_en: 'Statutory Pension Insurance',
  effective_date: date('1992-01-01')
})

// Benefit Type
CREATE (benefit:BenefitType {
  id: 'disability_pension',
  label_de: 'Erwerbsminderungsrente',
  label_en: 'Disability Pension',
  sgb_book: 'VI'
})<-[:REGULATES]-(sgb6)

// Administrative Process
CREATE (process:BusinessProcess {
  process_id: 'DRV-P-001',
  name: 'Antrag auf Erwerbsminderungsrente',
  name_en: 'Disability Pension Application',
  authority: 'Deutsche Rentenversicherung',
  avg_duration_days: 90,
  annual_volume: 45000
})

// Link process to legal provisions
CREATE (process)-[:BASED_ON]->(art43:Article {
  eli_uri: 'http://data.europa.eu/eli/de/sgb/6/43/oj',
  article_number: '43',
  title: 'Anspruch auf Rente wegen Erwerbsminderung'
})

// Impact relationship
CREATE (art43)-[:IMPACTS {
  impact_type: 'eligibility_criteria',
  affected_population: 320000,
  change_probability: 'medium'
}]->(process)
```

### 7.5 Temporal Versioning

```cypher
// Original version of an article
CREATE (v1:TemporalVersion {
  eli_uri: 'http://data.europa.eu/eli/de/sgb/2/7/2020-01-01',
  version_date: date('2020-01-01'),
  article_number: '7',
  title: 'Leistungsberechtigte',
  text_content: '...original text...',
  consolidation_status: 'official',
  bgbl_reference: 'BGBl. I 2019 Nr. 45 S. 2345'
})

// Amendment
CREATE (amendment:Amendment {
  amendment_date: date('2023-03-01'),
  amendment_type: 'text_change',
  description: 'Erweiterung Anspruchsberechtigter',
  bgbl_reference: 'BGBl. I 2023 Nr. 45 S. 1234',
  effective_date: date('2023-03-01')
})

// New version
CREATE (v2:TemporalVersion {
  eli_uri: 'http://data.europa.eu/eli/de/sgb/2/7/2023-03-01',
  version_date: date('2023-03-01'),
  article_number: '7',
  title: 'Leistungsberechtigte',
  text_content: '...amended text...',
  consolidation_status: 'official',
  bgbl_reference: 'BGBl. I 2023 Nr. 45 S. 1234'
})

// Temporal chain
CREATE (v2)-[:SUPERSEDES {
  change_date: date('2023-03-01'),
  change_reason: 'Gesetzesänderung'
}]->(v1)

CREATE (v2)<-[:CREATES]-(amendment)
CREATE (amendment)-[:AMENDS]->(v1)

// Current version pointer
CREATE (article:Article {
  eli_uri: 'http://data.europa.eu/eli/de/sgb/2/7/oj',
  article_number: '7'
})-[:CURRENT_VERSION]->(v2)
CREATE (article)-[:HAS_VERSION]->(v1)
CREATE (article)-[:HAS_VERSION]->(v2)
```

## 8. Query Examples (Cypher)

### 8.1 Find all laws implementing an EU directive

```cypher
MATCH (directive:EUDirective {eli_uri: 'http://data.europa.eu/eli/dir/2016/680/oj'})
      -[:IMPLEMENTED_BY]->(law:GermanLaw)
OPTIONAL MATCH (law)-[:HAS_ARTICLE]->(article:Article)
RETURN directive.title, law.title, collect(article.article_number) as articles
```

### 8.2 Track amendment history

```cypher
MATCH path = (latest:TemporalVersion {
  eli_uri: 'http://data.europa.eu/eli/de/sgb/2/7/oj'
})-[:SUPERSEDES*]->(historical:TemporalVersion)
RETURN path, 
       [v IN nodes(path) | v.version_date] as dates,
       [v IN nodes(path) | v.text_content] as versions
ORDER BY latest.version_date DESC
```

### 8.3 Find related legal concepts (EuroVoc)

```cypher
MATCH (article:Article {eli_uri: 'http://data.europa.eu/eli/de/sgb/6/43/oj'})
      -[:CONCERNS]->(concept:LegalConcept)
      -[:BROADER_THAN|NARROWER_THAN|RELATED_TO*1..2]->(related:LegalConcept)
RETURN concept.pref_label_de, collect(DISTINCT related.pref_label_de) as related_concepts
```

### 8.4 Impact analysis for legal changes

```cypher
MATCH (article:Article {article_number: '43'})
      <-[:BELONGS_TO]-(law {title: 'SGB VI'})
MATCH (article)-[:IMPACTS]->(process:BusinessProcess)
OPTIONAL MATCH (process)-[:REQUIRES_SYSTEM]->(system:ITSystem)
RETURN article.title,
       collect(DISTINCT {
         process: process.name,
         volume: process.annual_volume,
         systems: collect(system.name)
       }) as impacted_processes
```

### 8.5 Hybrid search (vector + graph)

```cypher
// Step 1: Vector search for semantic similarity
CALL db.index.vector.queryNodes('article_embeddings', 10, $query_embedding)
YIELD node as article, score

// Step 2: Graph expansion for context
MATCH (article)-[:REFERENCES]->(cited:Article)
MATCH (article)<-[:BELONGS_TO]-(law:LegalDocument)
MATCH (article)-[:CONCERNS]->(concept:LegalConcept)

RETURN article.eli_uri,
       article.title,
       article.text_content,
       score,
       collect(DISTINCT cited.article_number) as cited_articles,
       law.title,
       collect(DISTINCT concept.pref_label_de) as concepts
ORDER BY score DESC
LIMIT 5
```

## 9. GitHub Repository Structure

```
EU-GraphRAG/
├── README.md                    # Project overview, quick start
├── LICENSE                      # MIT License
├── .gitignore                   # Python, Neo4j, IDE files
├── requirements.txt             # Python dependencies
├── docker-compose.yml           # Neo4j + app stack
├── pyproject.toml              # Poetry/uv configuration
│
├── docs/
│   ├── GraphRAG-Concept.md     # This document
│   ├── Ontology-Specification.md
│   ├── API-Documentation.md
│   ├── User-Guide.md
│   └── Contributing.md
│
├── ontologies/
│   ├── eli-ontology.ttl        # ELI RDF/OWL
│   ├── ecli-ontology.ttl       # ECLI RDF/OWL
│   ├── eurovoc-core.ttl        # EuroVoc subset
│   ├── sgb-extension.ttl       # SGB-specific ontology
│   └── graph-schema.cypher     # Neo4j schema definition
│
├── src/
│   ├── __init__.py
│   ├── ingestion/
│   │   ├── scrapers/
│   │   │   ├── gesetze_im_internet.py
│   │   │   ├── eurlex_api.py
│   │   │   └── court_decisions.py
│   │   ├── parsers/
│   │   │   ├── xml_parser.py
│   │   │   ├── html_parser.py
│   │   │   └── pdf_extractor.py
│   │   └── etl_pipeline.py
│   │
│   ├── graph/
│   │   ├── neo4j_client.py
│   │   ├── schema_manager.py
│   │   ├── node_creator.py
│   │   └── relationship_builder.py
│   │
│   ├── llm/
│   │   ├── entity_extractor.py
│   │   ├── relationship_identifier.py
│   │   ├── embedding_generator.py
│   │   └── prompt_templates.py
│   │
│   ├── retrieval/
│   │   ├── vector_search.py
│   │   ├── graph_traversal.py
│   │   ├── hybrid_retriever.py
│   │   └── community_summarizer.py
│   │
│   ├── api/
│   │   ├── app.py              # FastAPI application
│   │   ├── routers/
│   │   │   ├── query.py
│   │   │   ├── documents.py
│   │   │   └── analytics.py
│   │   └── models.py           # Pydantic schemas
│   │
│   └── ui/
│       └── streamlit_app.py    # Demo interface
│
├── tests/
│   ├── unit/
│   │   ├── test_scrapers.py
│   │   ├── test_parsers.py
│   │   ├── test_graph_ops.py
│   │   └── test_retrieval.py
│   ├── integration/
│   │   ├── test_etl_pipeline.py
│   │   └── test_graphrag_e2e.py
│   └── fixtures/
│       ├── sample_laws.json
│       └── test_queries.yaml
│
├── config/
│   ├── neo4j.yaml              # Database configuration
│   ├── llm.yaml                # LLM settings (API keys, models)
│   ├── scrapers.yaml           # Scraping targets, schedules
│   └── logging.yaml            # Logging configuration
│
├── data/
│   ├── raw/                    # Downloaded XML/HTML/PDF
│   ├── processed/              # Parsed, structured data
│   └── embeddings/             # Precomputed vectors
│
├── notebooks/
│   ├── 01-data-exploration.ipynb
│   ├── 02-ontology-design.ipynb
│   ├── 03-graph-analysis.ipynb
│   └── 04-retrieval-experiments.ipynb
│
└── scripts/
    ├── init_database.sh        # Neo4j setup, schema creation
    ├── ingest_sgb.py           # One-off SGB ingestion
    ├── update_eurlex.py        # Incremental EU law updates
    └── generate_embeddings.py  # Batch embedding generation
```

## 10. Next Steps

### Week 1: Project Setup
- [x] Create GitHub repository: `https://github.com/sopra-steria-cassa/EU-GraphRAG`
- [ ] Initialize Neo4j database (Docker + AuraDB)
- [ ] Set up development environment (Python 3.11, Poetry)
- [ ] Create ontology documentation (Cypher schema)
- [ ] Write README with quick start guide

### Week 2-3: Data Ingestion Prototype
- [ ] Implement Gesetze im Internet scraper (SGB I-III)
- [ ] Parse HTML to extract articles, paragraphs
- [ ] Create Neo4j nodes/relationships
- [ ] Validate: 500+ articles ingested, ELI URIs correct

### Week 4: Basic Retrieval
- [ ] Implement Cypher queries (find by ELI, search by title)
- [ ] Add vector search (embeddings for articles)
- [ ] Streamlit UI for law lookup
- [ ] Validate: <2s query latency

### Month 2: LLM Integration
- [ ] Entity extraction with GPT-4 (organizations, dates, concepts)
- [ ] Relationship identification (REFERENCES citations)
- [ ] Human validation loop (sample 100 extractions, >95% accuracy)
- [ ] Update graph with extracted relationships

### Month 3: GraphRAG Prototype
- [ ] Hybrid retrieval (vector + graph traversal)
- [ ] LLM answer generation with sources
- [ ] Test set: 50 legal questions, >85% accuracy
- [ ] Demo video and blog post

### Month 4-6: EU Integration
- [ ] EUR-Lex API integration
- [ ] EuroVoc mapping (LLM-assisted)
- [ ] ECLI case law ingestion
- [ ] Transposition tracking (10 pilot directives)

### Month 7-12: Production & Scaling
- [ ] FastAPI REST service
- [ ] BA/DRV pilot (2 agencies, 50 users)
- [ ] Performance optimization (100K+ nodes, <10s queries)
- [ ] EU funding proposal (SIMPL, GovTech4All)
- [ ] Open-source release, community building

---

## Appendix A: Technology Comparison

| Component | Option 1 | Option 2 | **Selected** | Rationale |
|-----------|----------|----------|--------------|-----------|
| **Graph DB** | Neo4j | Stardog | **Neo4j** | Largest ecosystem, best GraphRAG support, AuraDB cloud |
| **LLM** | OpenAI GPT-4 | Llama 3 (local) | **GPT-4** | Superior accuracy, API stability (local for sensitive data) |
| **Embeddings** | OpenAI ada-002 | E5-multilingual | **E5-multilingual** | Free, multilingual, good performance |
| **API Framework** | FastAPI | Flask | **FastAPI** | Async, auto docs, Pydantic validation |
| **ETL** | Airflow | Prefect | **Airflow** | Industry standard, mature, BA/DRV familiarity |
| **UI** | Streamlit | Gradio | **Streamlit** | Rich components, easy deployment |
| **Testing** | Pytest | Unittest | **Pytest** | Better fixtures, plugins, readability |

## Appendix B: Competitive Landscape

| Competitor | Strength | Weakness | Cassa Advantage |
|------------|----------|----------|-----------------|
| **Neo4j Platform** | Graph database leader | No legal ontology | Pre-built ELI/ECLI/SGB schema |
| **Stardog** | Semantic graph, RDF | Smaller ecosystem | Larger community, better docs |
| **LexisNexis** | Comprehensive legal data | Expensive, law firms | Free/open-source, public sector |
| **Ontotext GraphDB** | EU compliance focus | Limited GraphRAG | Advanced LLM integration |
| **Microsoft GraphRAG** | Generic framework | No legal domain | Legal-specific, standards-native |

## Appendix C: EU Funding Opportunities

| Programme | Call | Deadline | Budget | Fit |
|-----------|------|----------|--------|-----|
| **SIMPL Programme** | Legal Interoperability | Q1 2026 | €2-10M | ★★★★★ (perfect fit) |
| **GovTech4All 2.0** | Municipal Legal Compliance | Q2 2026 | €500K-2M | ★★★★☆ |
| **Digital Europe** | AI for Public Good | Rolling | €1-5M | ★★★★☆ |
| **Interoperable Europe** | Best Practices | Q3 2026 | €200K-1M | ★★★☆☆ |

## Appendix D: Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Neo4j scalability limits | Medium | High | Sharding, read replicas, caching |
| LLM hallucinations | High | High | Graph grounding, citation validation |
| Slow government procurement | High | Medium | Parallel private sector sales |
| Copyright issues | Low | High | Use only official government publications |
| Budget constraints | Medium | High | Open-source model, EU grants |
| Technical staff shortage | Medium | Medium | External contractors, university partnerships |

---

**Document Version**: 1.0
**Last Updated**: November 9, 2025
**Next Review**: December 9, 2025
**Owner**: Cassa (Law2Logic) Product Team
**Status**: Active Development
