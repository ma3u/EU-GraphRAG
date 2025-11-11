# EU-GraphRAG Quick Start Guide

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
# venv\Scripts\activate

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
