
# Create project structure summary
structure_doc = """# EU-GraphRAG Project Structure

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
"""

with open("/home/mbuchhorn/projects/EU_GraphRAG/PROJECT_STRUCTURE.md", 'w', encoding='utf-8') as f:
    f.write(structure_doc)

print("✓ Created PROJECT_STRUCTURE.md")

# Create GitHub initialization script
github_script = """#!/bin/bash
# EU GraphRAG - GitHub Repository Initialization Script
# Run this script to create and push to GitHub

set -e

echo "==================================================================="
echo "EU GraphRAG - GitHub Repository Setup"
echo "==================================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: README.md not found. Please run this script from the project root."
    exit 1
fi

# Initialize Git if not already done
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already exists"
fi

# Create .gitkeep files for empty directories
echo "📁 Creating .gitkeep files for empty directories..."
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch data/embeddings/.gitkeep
echo "✓ .gitkeep files created"

# Stage all files
echo "📝 Staging files..."
git add .
echo "✓ Files staged"

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: EU GraphRAG project structure

- Comprehensive GraphRAG concept document
- ELI, ECLI, EuroVoc, SGB ontologies
- Neo4j graph schema with sample data
- Project structure and documentation
- Configuration files and dependencies"
echo "✓ Initial commit created"

# Instructions for GitHub remote
echo ""
echo "==================================================================="
echo "Next Steps:"
echo "==================================================================="
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: EU-GraphRAG"
echo "   - Description: GraphRAG system for EU regulations and German legal documents"
echo "   - Visibility: Public"
echo "   - License: MIT (already included)"
echo "   - DO NOT initialize with README, .gitignore, or license"
echo ""
echo "2. After creating the repository, run these commands:"
echo ""
echo "   git remote add origin https://github.com/YOUR-USERNAME/EU-GraphRAG.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Alternative: If you want to use GitHub CLI (gh):"
echo ""
echo "   gh repo create EU-GraphRAG --public --description 'GraphRAG system for EU regulations and German legal documents' --source=."
echo "   git push -u origin main"
echo ""
echo "==================================================================="
echo "✅ Local repository ready for GitHub push!"
echo "==================================================================="
"""

with open("/home/mbuchhorn/projects/EU_GraphRAG/scripts/init_github.sh", 'w', encoding='utf-8') as f:
    f.write(github_script)

# Make the script executable
import os
os.chmod("/home/mbuchhorn/projects/EU_GraphRAG/scripts/init_github.sh", 0o755)

print("✓ Created scripts/init_github.sh (executable)")

# Create quick start guide
quickstart = """# EU-GraphRAG Quick Start Guide

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git
- OpenAI API key (or local LLM setup)

## Installation (5 minutes)

### 1. Clone Repository

```bash
git clone https://github.com/sopra-steria-cassa/EU-GraphRAG.git
cd EU-GraphRAG
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
# venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your actual values
nano .env  # or use your favorite editor

# Required: NEO4J_URI, NEO4J_PASSWORD, OPENAI_API_KEY
```

### 4. Start Neo4j Database

```bash
# Start Neo4j with Docker Compose
docker-compose up -d neo4j

# Wait for Neo4j to be ready (~30 seconds)
docker logs eu-graphrag-neo4j --follow

# Initialize schema
cat ontologies/graph-schema.cypher | docker exec -i eu-graphrag-neo4j cypher-shell -u neo4j -p password
```

### 5. Verify Installation

```bash
# Check Neo4j is running
curl http://localhost:7474

# Check Python environment
python -c "import neo4j; print(f'Neo4j driver version: {neo4j.__version__}')"
```

## First Steps

### 1. Explore Sample Data

The graph schema includes sample data for testing:

```bash
# Open Neo4j Browser
open http://localhost:7474

# Log in: neo4j / password

# Run sample queries:
# 1. View all node types
MATCH (n) RETURN labels(n) as NodeType, count(n) as Count ORDER BY Count DESC;

# 2. View SGB VI article
MATCH (a:Article {article_number: '43'}) RETURN a;

# 3. See amendment history
MATCH path = (latest:TemporalVersion {article_number: '43'})-[:SUPERSEDES*]->(historical)
RETURN path;

# 4. Find impacted processes
MATCH (a:Article {article_number: '43'})-[:IMPACTS]->(p:BusinessProcess)
RETURN a.title, p.name, p.annual_volume;
```

### 2. Run First Ingestion (Coming Soon)

```bash
# Ingest SGB I-III from Gesetze im Internet
python scripts/ingest_sgb.py --books I II III

# This will:
# - Scrape laws from gesetze-im-internet.de
# - Parse HTML to extract articles
# - Create Neo4j nodes and relationships
# - Generate embeddings for semantic search
```

### 3. Launch UI (Coming Soon)

```bash
# Start Streamlit demo interface
streamlit run src/ui/streamlit_app.py

# Or start FastAPI service
uvicorn src.api.app:app --reload
```

## Example Queries

### GraphRAG Query (Conceptual)

```python
from src.retrieval.hybrid_retriever import HybridRetriever

retriever = HybridRetriever()

# Query with natural language
answer = retriever.query(
    question="What changed in SGB II § 7 since January 2023?",
    filters={"jurisdiction": "DE", "sgb_book": "II"}
)

print(answer.text)  # LLM-generated answer
print(answer.sources)  # ELI URIs of cited articles
print(answer.metadata)  # Amendment dates, BGBl references
```

### Cypher Queries

```cypher
// Find all SGB VI articles about disability pensions
MATCH (a:Article {sgb_book: 'VI'})
WHERE a.title CONTAINS 'Erwerbsminderung'
RETURN a.article_number, a.title;

// Track cross-border social security coordination
MATCH (sgb:SocialLawBook)-[:COORDINATES_WITH]->(eureg:EURegulation)
RETURN sgb.title_de, eureg.title_en;

// Identify processes affected by legal changes
MATCH (a:Article)-[r:IMPACTS]->(p:BusinessProcess)
RETURN a.title, p.name, r.impact_type, r.affected_population
ORDER BY r.affected_population DESC;
```

## Project Structure

```
EU-GraphRAG/
├── docs/               # Documentation
├── ontologies/         # ELI, ECLI, EuroVoc, SGB schemas
├── src/                # Source code
│   ├── ingestion/      # Data scrapers & parsers
│   ├── graph/          # Neo4j operations
│   ├── llm/            # LLM integration
│   ├── retrieval/      # GraphRAG retrieval
│   ├── api/            # REST API
│   └── ui/             # Streamlit UI
├── tests/              # Unit & integration tests
├── config/             # Configuration files
├── data/               # Raw & processed data
└── scripts/            # Utility scripts
```

## Troubleshooting

### Neo4j Connection Issues

```bash
# Check Neo4j is running
docker ps | grep neo4j

# View logs
docker logs eu-graphrag-neo4j

# Restart Neo4j
docker-compose restart neo4j
```

### Python Import Errors

```bash
# Ensure virtual environment is activated
which python  # Should point to venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database Schema Issues

```bash
# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d neo4j

# Re-initialize schema
cat ontologies/graph-schema.cypher | docker exec -i eu-graphrag-neo4j cypher-shell -u neo4j -p password
```

## Next Steps

1. **Read Documentation**: See `docs/GraphRAG-Concept.md` for technical details
2. **Explore Ontologies**: Review `ontologies/*.yaml` for data model
3. **Run Tests**: `pytest tests/` (when implemented)
4. **Contribute**: See `docs/Contributing.md` for guidelines
5. **Join Community**: GitHub Discussions for Q&A

## Resources

- **Documentation**: `docs/`
- **GitHub**: https://github.com/sopra-steria-cassa/EU-GraphRAG
- **ELI Ontology**: https://op.europa.eu/en/web/eu-vocabularies/eli
- **ECLI Portal**: https://e-justice.europa.eu/ecli
- **Neo4j Docs**: https://neo4j.com/docs/

## Support

- **Issues**: https://github.com/sopra-steria-cassa/EU-GraphRAG/issues
- **Discussions**: https://github.com/sopra-steria-cassa/EU-GraphRAG/discussions
- **Email**: law2logic@sopra-steria.com

---

**Happy GraphRAG-ing! 🚀**
"""

with open("/home/mbuchhorn/projects/EU_GraphRAG/QUICKSTART.md", 'w', encoding='utf-8') as f:
    f.write(quickstart)

print("✓ Created QUICKSTART.md")

print("\n" + "="*70)
print("✅ All project files created successfully!")
print("="*70)
print("\nProject ready at: /home/mbuchhorn/projects/EU_GraphRAG")
print("\nNext step: Run scripts/init_github.sh to push to GitHub")
