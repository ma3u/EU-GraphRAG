# EU-GraphRAG Project Structure

## Directory Tree

```
EU-GraphRAG/
│
├── README.md                           # Project overview, quick start
├── LICENSE                             # MIT License
├── .gitignore                          # Git ignore patterns
├── .env.example                        # Environment variables template
├── requirements.txt                    # Python dependencies
├── docker-compose.yml                  # Docker stack (Neo4j + App)
├── pyproject.toml                      # Poetry/uv configuration (to be added)
│
├── docs/                               # Documentation
│   ├── GraphRAG-Concept.md            # ✅ Comprehensive technical spec
│   ├── Ontology-Specification.md      # TODO: Detailed ontology docs
│   ├── API-Documentation.md           # TODO: REST API reference
│   ├── User-Guide.md                  # TODO: End-user guide
│   └── Contributing.md                # TODO: Developer guidelines
│
├── ontologies/                         # Ontology specifications
│   ├── eli-core.yaml                  # ✅ ELI ontology
│   ├── ecli-core.yaml                 # ✅ ECLI ontology
│   ├── eurovoc-core.yaml              # ✅ EuroVoc thesaurus
│   ├── sgb-extension.yaml             # ✅ SGB domain model
│   └── graph-schema.cypher            # ✅ Neo4j schema + sample data
│
├── src/                                # Source code
│   ├── __init__.py
│   │
│   ├── ingestion/                     # Data ingestion
│   │   ├── __init__.py
│   │   ├── scrapers/                  # Web scrapers
│   │   │   ├── __init__.py
│   │   │   ├── gesetze_im_internet.py # TODO: German laws scraper
│   │   │   ├── eurlex_api.py          # TODO: EUR-Lex API client
│   │   │   └── court_decisions.py     # TODO: ECLI case law
│   │   ├── parsers/                   # Document parsers
│   │   │   ├── __init__.py
│   │   │   ├── xml_parser.py          # TODO: XML/RDF parsing
│   │   │   ├── html_parser.py         # TODO: HTML extraction
│   │   │   └── pdf_extractor.py       # TODO: PDF text extraction
│   │   └── etl_pipeline.py            # TODO: ETL orchestration
│   │
│   ├── graph/                          # Graph operations
│   │   ├── __init__.py
│   │   ├── neo4j_client.py            # TODO: Neo4j connection
│   │   ├── schema_manager.py          # TODO: Schema management
│   │   ├── node_creator.py            # TODO: Node creation logic
│   │   └── relationship_builder.py    # TODO: Relationship builder
│   │
│   ├── llm/                            # LLM integration
│   │   ├── __init__.py
│   │   ├── entity_extractor.py        # TODO: Entity extraction
│   │   ├── relationship_identifier.py # TODO: Relationship extraction
│   │   ├── embedding_generator.py     # TODO: Vector embeddings
│   │   └── prompt_templates.py        # TODO: LLM prompts
│   │
│   ├── retrieval/                      # GraphRAG retrieval
│   │   ├── __init__.py
│   │   ├── vector_search.py           # TODO: Semantic search
│   │   ├── graph_traversal.py         # TODO: Graph queries
│   │   ├── hybrid_retriever.py        # TODO: Hybrid retrieval
│   │   └── community_summarizer.py    # TODO: Community detection
│   │
│   ├── api/                            # REST API
│   │   ├── __init__.py
│   │   ├── app.py                     # TODO: FastAPI application
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── query.py               # TODO: Query endpoints
│   │   │   ├── documents.py           # TODO: Document endpoints
│   │   │   └── analytics.py           # TODO: Analytics endpoints
│   │   └── models.py                  # TODO: Pydantic schemas
│   │
│   └── ui/                             # User interface
│       ├── __init__.py
│       └── streamlit_app.py           # TODO: Streamlit demo
│
├── tests/                              # Tests
│   ├── __init__.py
│   ├── unit/                          # Unit tests
│   │   ├── __init__.py
│   │   ├── test_scrapers.py           # TODO
│   │   ├── test_parsers.py            # TODO
│   │   ├── test_graph_ops.py          # TODO
│   │   └── test_retrieval.py          # TODO
│   ├── integration/                   # Integration tests
│   │   ├── __init__.py
│   │   ├── test_etl_pipeline.py       # TODO
│   │   └── test_graphrag_e2e.py       # TODO
│   └── fixtures/                      # Test data
│       ├── sample_laws.json           # TODO
│       └── test_queries.yaml          # TODO
│
├── config/                             # Configuration
│   ├── neo4j.yaml                     # TODO: Database config
│   ├── llm.yaml                       # TODO: LLM settings
│   ├── scrapers.yaml                  # TODO: Scraping config
│   └── logging.yaml                   # TODO: Logging config
│
├── data/                               # Data storage
│   ├── raw/                           # Downloaded files
│   │   └── .gitkeep
│   ├── processed/                     # Parsed data
│   │   └── .gitkeep
│   └── embeddings/                    # Precomputed vectors
│       └── .gitkeep
│
├── notebooks/                          # Jupyter notebooks
│   ├── 01-data-exploration.ipynb      # TODO
│   ├── 02-ontology-design.ipynb       # TODO
│   ├── 03-graph-analysis.ipynb        # TODO
│   └── 04-retrieval-experiments.ipynb # TODO
│
└── scripts/                            # Utility scripts
    ├── init_database.sh               # TODO: Neo4j setup
    ├── ingest_sgb.py                  # TODO: SGB ingestion
    ├── update_eurlex.py               # TODO: EUR-Lex updates
    └── generate_embeddings.py         # TODO: Batch embeddings
```

## Completed Files (✅)

### Documentation
- **GraphRAG-Concept.md** (57 KB): Comprehensive technical specification
- **README.md**: Project overview with quick start guide

### Ontologies
- **eli-core.yaml**: ELI ontology specification
- **ecli-core.yaml**: ECLI ontology specification
- **eurovoc-core.yaml**: EuroVoc thesaurus structure
- **sgb-extension.yaml**: SGB domain model
- **graph-schema.cypher**: Neo4j schema with constraints, indexes, sample data

### Configuration
- **requirements.txt**: Python dependencies
- **.env.example**: Environment variables template
- **.gitignore**: Git ignore patterns
- **LICENSE**: MIT License

## Next Steps

### Week 1: GitHub & Database Setup
1. **Initialize Git repository**
   ```bash
   cd /home/mbuchhorn/projects/EU_GraphRAG
   git init
   git add .
   git commit -m "Initial commit: EU GraphRAG project structure"
   ```

2. **Create GitHub repository**
   - Repository name: `EU-GraphRAG`
   - Description: "GraphRAG system for EU regulations and German legal documents"
   - Visibility: Public
   - License: MIT

3. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/sopra-steria-cassa/EU-GraphRAG.git
   git branch -M main
   git push -u origin main
   ```

4. **Set up Neo4j database**
   ```bash
   # Start Neo4j with Docker
   docker-compose up -d neo4j
   
   # Initialize schema
   cat ontologies/graph-schema.cypher | docker exec -i eu-graphrag-neo4j cypher-shell -u neo4j -p password
   ```

### Week 2: Initial Implementation
1. Create Python package structure (src/__init__.py files)
2. Implement Neo4j client (src/graph/neo4j_client.py)
3. Build Gesetze im Internet scraper (src/ingestion/scrapers/gesetze_im_internet.py)
4. Create basic ingestion pipeline

### Week 3: First Data Ingestion
1. Scrape SGB I-III from Gesetze im Internet
2. Parse HTML to extract articles
3. Create Neo4j nodes (LegalDocument, Article)
4. Validate: 500+ articles ingested

### Week 4: Basic Retrieval
1. Implement Cypher query templates
2. Add vector search capabilities
3. Create simple Streamlit UI for law lookup
4. Validate: <2s query latency

## File Sizes

```
GraphRAG-Concept.md:    ~57 KB (comprehensive spec)
graph-schema.cypher:    ~15 KB (schema + sample data)
README.md:              ~12 KB (quick start guide)
eli-core.yaml:          ~5 KB (ELI ontology)
ecli-core.yaml:         ~4 KB (ECLI ontology)
eurovoc-core.yaml:      ~6 KB (EuroVoc structure)
sgb-extension.yaml:     ~8 KB (SGB domain model)
requirements.txt:       ~2 KB (dependencies)
```

## Technology Stack

| Layer | Technology | Status |
|-------|-----------|--------|
| **Graph Database** | Neo4j 5.15.0 | ✅ Schema ready |
| **Vector Search** | Neo4j Vector Index | ✅ Schema ready |
| **LLM** | OpenAI GPT-4 | ⏳ To configure |
| **Embeddings** | E5-multilingual | ⏳ To configure |
| **API** | FastAPI | ⏳ To implement |
| **UI** | Streamlit | ⏳ To implement |
| **ETL** | Apache Airflow | ⏳ To configure |
| **Testing** | Pytest | ⏳ To implement |

## Contact

- **Project**: EU-GraphRAG
- **Organization**: Sopra Steria - Cassa (Law2Logic)
- **Repository**: https://github.com/sopra-steria-cassa/EU-GraphRAG
- **Date Created**: November 9, 2025
