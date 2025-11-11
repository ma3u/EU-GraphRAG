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

1. **LegalDocument**
   - Properties: eli_uri, title, document_type (directive/regulation/law), effective_date, publication_date, status
   - Subtypes: EUDirective, EURegulation, GermanLaw, CourtDecision

2. **Article/Section**
   - Properties: article_number, title, text_content, eli_uri (with fragment)
   - Hierarchical structure: Chapter → Section → Paragraph

3. **LegalConcept**
   - Properties: concept_id, preferred_label, alt_labels, eurovoc_id, domain
   - Based on EuroVoc thesaurus descriptors

4. **Organization**
   - Properties: name, org_type (ministry/agency/court), country_code, eli_court_code

5. **TemporalVersion**
   - Properties: version_date, consolidation_status, change_description
   - Represents specific versions of articles/laws

6. **Amendment**
   - Properties: amendment_date, amendment_type, description
   - Links versions of legal texts

#### Core Relationship Types

1. **IMPLEMENTS** (EUDirective → GermanLaw)
   - Properties: transposition_deadline, implementation_status, mapping_confidence

2. **REFERENCES** (Article → Article)
   - Properties: reference_type (cites/amends/repeals), context

3. **SUPERSEDES** (TemporalVersion → TemporalVersion)
   - Properties: change_date, change_reason

4. **BELONGS_TO** (Article → LegalDocument)
   - Properties: hierarchical_position

5. **CONCERNS** (LegalDocument → LegalConcept)
   - Properties: relevance_score, eurovoc_descriptor

6. **DECIDED_BY** (CourtDecision → Organization)
   - Properties: ecli_uri, decision_date

7. **IMPACTS** (Amendment → BusinessProcess)
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

1. **Document Ingestion**
   - Scrape/API retrieve: Gesetze im Internet, EUR-Lex, court databases
   - Parse: XML, HTML, PDF extraction
   - Normalize: UTF-8, clean formatting

2. **Entity Extraction (LLM-based)**
   - Extract: Organizations, legal concepts, dates, references
   - Classify: Document type, subject matter
   - Validation: Human-in-the-loop for critical entities

3. **Graph Construction**
   - Create nodes: Documents, articles, concepts
   - Establish relationships: References, implementations, amendments
   - Link to ontologies: ELI URIs, EuroVoc descriptors

4. **Embedding Generation**
   - Article-level embeddings: Dense vector representations
   - Concept embeddings: Semantic similarity search
   - Community summaries: Hierarchical GraphRAG approach

5. **Quality Assurance**
   - Verify ELI/ECLI compliance
   - Check relationship consistency
   - Validate temporal chains (SUPERSEDES)

#### Query Pipeline (Hybrid GraphRAG)

1. **Query Understanding**
   - Parse user question
   - Identify: Entities, time constraints, jurisdictions
   - Classify: Query type (factual/analytical/comparative)

2. **Hybrid Retrieval**
   - **Vector Search**: Semantic similarity on article embeddings
   - **Graph Traversal**: Relationship-based context expansion
     - REFERENCES relationships → cited articles
     - IMPLEMENTS relationships → related EU/national laws
     - SUPERSEDES relationships → historical versions
   - **Community-based**: Leiden algorithm clusters for global queries

3. **Context Assembly**
   - Rank retrieved articles/concepts
   - Assemble: Primary sources + related context
   - Limit: Token budget for LLM (e.g., 8k context window)

4. **Answer Generation**
   - LLM generates response with context
   - Cite sources: ELI/ECLI URIs, article numbers
   - Hallucination prevention: Grounded in graph data

5. **Validation & Enrichment**
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

## 4. Implementation Roadmap

### Phase 1: Foundation (Months 1-3)
- [ ] Set up Neo4j database (local + cloud)
- [ ] Create GitHub repository (public, MIT license)
- [ ] Implement ELI ontology schema
- [ ] Build web scrapers (Gesetze im Internet pilot)
- [ ] Ingest SGB I-III as proof of concept
- [ ] Basic Cypher queries for retrieval

### Phase 2: GraphRAG Core (Months 4-6)
- [ ] LLM entity extraction pipeline
- [ ] Relationship identification (REFERENCES, IMPLEMENTS)
- [ ] Embedding generation for articles
- [ ] Hybrid retrieval implementation
- [ ] Q&A interface (Streamlit demo)
- [ ] 100% test coverage for core modules

### Phase 3: EU Integration (Months 7-9)
- [ ] EUR-Lex API integration
- [ ] EuroVoc concept mapping
- [ ] ECLI case law ingestion
- [ ] EU-to-German transposition tracking
- [ ] Multilingual support (DE/EN/FR)

### Phase 4: Production (Months 10-12)
- [ ] FastAPI REST service
- [ ] Authentication & authorization
- [ ] Performance optimization (indexing, caching)
- [ ] BA/DRV pilot deployment
- [ ] Documentation & user training
- [ ] Open-source release (GitHub, Docker)

## 5. Use Cases

### 5.1 Regulatory Compliance Assistant
**Scenario**: BA compliance officer needs to check SGB II updates
**Query**: "What changed in SGB II § 7 since January 2023?"
**GraphRAG Response**:
1. Traverse SUPERSEDES chain for SGB II § 7
2. Retrieve amendments from 2023-01-01 onwards
3. Return: Amendment texts, effective dates, BGBl references

### 5.2 EU Transposition Analysis
**Scenario**: Ministry of Labor needs to verify Data Act implementation
**Query**: "Which German laws implement EU Data Act (2023/2854)?"
**GraphRAG Response**:
1. Find EURegulation node (eli:reg/2023/2854)
2. Traverse IMPLEMENTS relationships
3. Return: List of German laws, implementation status, gaps

### 5.3 Cross-Border Social Security
**Scenario**: Legal researcher studying pension coordination
**Query**: "How does SGB VI interact with EU Regulation 883/2004?"
**GraphRAG Response**:
1. Graph traversal: SGB VI → REFERENCES → EU Reg 883/2004
2. Identify relevant articles in both
3. Return: Coordination rules, conflict resolution

### 5.4 Impact Analysis
**Scenario**: Policy analyst assessing proposed SGB amendment
**Query**: "Which DRV processes would be affected by changing SGB VI § 43?"
**GraphRAG Response**:
1. Traverse IMPACTS relationships
2. Retrieve linked BusinessProcess nodes
3. Return: Process IDs, affected populations, cost estimates

## 6. Differentiation from Competitors

### vs. Neo4j/Stardog (Graph Platforms)
- **Cassa Advantage**: Pre-built legal ontology, ready-to-use
- **Competitors**: Require 12-18 months custom development

### vs. LexisNexis/Westlaw (Legal Research)
- **Cassa Advantage**: Public sector focus, EU integration, open-source
- **Competitors**: Expensive, law firm-centric, proprietary

### vs. Microsoft GraphRAG (General Purpose)
- **Cassa Advantage**: Legal-specific, ELI/ECLI native, temporal tracking
- **Competitors**: Generic, requires domain adaptation

### Unique Features
1. **Amendment Chains**: Temporal SUPERSEDES graphs
2. **Transposition Tracking**: Automated EU-to-national mapping
3. **Process Impact**: Legal changes → operational effects
4. **Standards-First**: ELI Task Force collaboration
5. **Open Source**: Community-driven, government-friendly

## 7. Quality Metrics

### Data Quality
- ELI conformance: 100% for EU documents
- Relationship accuracy: >95% (human-validated sample)
- Temporal chain completeness: >90%
- EuroVoc mapping coverage: >80%

### System Performance
- Query latency: <2s for simple, <10s for complex
- Graph size: 100K+ nodes, 500K+ relationships (Phase 3)
- Uptime: 99.5% (production)
- Embedding refresh: Weekly

### User Metrics
- Answer accuracy: >90% (expert evaluation)
- Citation correctness: 100% (ELI/ECLI validation)
- User satisfaction: >4.0/5.0

## 8. Risk Mitigation

### Technical Risks
- **Neo4j scalability**: Use sharding, read replicas
- **LLM hallucinations**: Graph grounding, citation verification
- **Data drift**: Automated monitoring, daily updates

### Legal Risks
- **Copyright**: Limit to official government publications
- **Data protection**: Anonymize personal data in case law
- **Liability**: Disclaimers (no legal advice, for research only)

### Organizational Risks
- **Slow procurement**: Parallel private sector pilots (DAX companies)
- **Budget constraints**: Open-source model, EU grant applications
- **Adoption resistance**: User training, stakeholder engagement

## 9. Success Criteria

### Short-term (6 months)
- [ ] 5,000+ legal documents ingested (SGB + pilot EU directives)
- [ ] GraphRAG Q&A demo with >85% accuracy
- [ ] GitHub repo with 100+ stars
- [ ] 1-2 pilot projects signed (BA/DRV)

### Medium-term (12 months)
- [ ] 50,000+ documents (full SGB, major EU regulations)
- [ ] Production deployment at 2+ government agencies
- [ ] EU funding secured (€500K+ SIMPL/GovTech)
- [ ] Academic publication (legal informatics conference)

### Long-term (24 months)
- [ ] 10+ EU member states using system
- [ ] €5M+ annual revenue (subscriptions + support)
- [ ] Integration with eur-lex.europa.eu
- [ ] ELI Task Force reference implementation

## 10. Next Steps

### Immediate Actions (This Week)
1. Create GitHub repo: `EU-GraphRAG` (MIT license)
2. Initialize Neo4j database (Neo4j AuraDB free tier + local)
3. Document ontology schema (Cypher CREATE statements)
4. Set up development environment (Docker Compose)

### Month 1 Deliverables
1. Complete ontology documentation (ELI, ECLI, SGB)
2. Scraper for Gesetze im Internet (SGB I-III)
3. Basic graph ingestion (1,000 articles)
4. First Cypher queries (find law by ELI, traverse REFERENCES)
5. Project README and contribution guidelines

---

**Version**: 1.0
**Date**: November 9, 2025
**Authors**: Cassa (Law2Logic) Product Team
**Status**: Active Development
