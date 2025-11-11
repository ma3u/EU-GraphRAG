
# Create comprehensive README for GitHub
readme_content = """# EU-GraphRAG: European Legal Knowledge Graph with GraphRAG

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![Neo4j 5.x](https://img.shields.io/badge/Neo4j-5.x-green.svg)

A production-ready **GraphRAG system** for European Union regulations, German legal documents (SGB, BGB, etc.), and cross-border legal knowledge. Built on **Neo4j** with native support for **ELI**, **ECLI**, and **EuroVoc** ontologies.

## 🎯 Project Vision

Create the first open-source GraphRAG system for EU regulatory compliance that:
- ✅ Natively integrates ELI (European Legislation Identifier) and ECLI (European Case Law Identifier)
- ✅ Enables automated EU-to-national law transposition analysis
- ✅ Provides temporal tracking of legal amendments
- ✅ Supports multilingual legal search across 24 EU languages

## 🚀 Quick Start

### Prerequisites
- **Docker** & **Docker Compose**
- **Python 3.11+**
- **Neo4j AuraDB** (free tier) or local Neo4j instance

### Installation

```bash
# Clone repository
git clone https://github.com/sopra-steria-cassa/EU-GraphRAG.git
cd EU-GraphRAG

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt

# Start Neo4j database
docker-compose up -d

# Initialize graph schema
python scripts/init_database.py

# Ingest sample data (SGB I-III)
python scripts/ingest_sgb.py
```

### Run Demo

```bash
# Start Streamlit UI
streamlit run src/ui/streamlit_app.py

# Or use REST API
uvicorn src.api.app:app --reload
```

Navigate to `http://localhost:8501` for the UI or `http://localhost:8000/docs` for API documentation.

## 📊 Architecture Overview

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
    ┌────▼────────────────────────────────┐
    │  GraphRAG Query Engine               │
    │  ┌────────────┬──────────────────┐  │
    │  │ Vector     │ Graph Traversal  │  │
    │  │ Search     │ (Cypher)         │  │
    │  └────────────┴──────────────────┘  │
    └────────┬────────────────────────────┘
             │
    ┌────────▼────────────────────────┐
    │  Neo4j Knowledge Graph          │
    │  ┌──────────┬──────────────┐    │
    │  │ ELI      │ ECLI         │    │
    │  │ Ontology │ Metadata     │    │
    │  ├──────────┼──────────────┤    │
    │  │ EuroVoc  │ SGB Domain   │    │
    │  │ Concepts │ Model        │    │
    │  └──────────┴──────────────┘    │
    └─────────────────────────────────┘
```

### Core Node Types
- **LegalDocument**: EU directives, regulations, German laws
- **Article/Section**: Individual provisions with ELI URIs
- **LegalConcept**: EuroVoc thesaurus descriptors
- **TemporalVersion**: Historical versions of legal texts
- **CourtDecision**: Case law with ECLI identifiers

### Key Relationships
- **IMPLEMENTS**: EU Directive → German Law
- **REFERENCES**: Article → Cited Article
- **SUPERSEDES**: New Version → Old Version
- **CONCERNS**: Document → Legal Concept (EuroVoc)

## 🔍 Use Cases

### 1. Regulatory Compliance
**Query**: "What changed in SGB II § 7 since January 2023?"

GraphRAG retrieves:
- Amendment history via `SUPERSEDES` relationships
- BGBl (Federal Law Gazette) references
- Effective dates and consolidation status

### 2. EU Transposition Tracking
**Query**: "Which German laws implement the EU Data Act (2023/2854)?"

GraphRAG analyzes:
- `IMPLEMENTS` relationships
- Implementation gaps and deadlines
- Cross-references to national legislation

### 3. Cross-Border Legal Research
**Query**: "How does SGB VI interact with EU Regulation 883/2004?"

GraphRAG provides:
- Coordination rules between German pension law and EU social security regulation
- Relevant articles in both legal frameworks
- Conflict resolution mechanisms

## 📚 Data Sources

### EU Sources
- **EUR-Lex**: Official EU legal database (SPARQL endpoint)
- **CELLAR**: Publications Office repository
- **CJEU**: Court of Justice case law

### German Sources
- **Gesetze im Internet**: ~5,000 federal laws
- **Bundesgesetzblatt**: Official law gazette (BGBl I & II)
- **Federal Courts**: Supreme court decisions (ECLI-compliant)

### SGB-Specific
- SGB I-XII: Complete social law books
- BA/DRV regulations: Employment and pension insurance

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Graph Database** | Neo4j 5.x | Knowledge graph storage |
| **Vector Search** | Neo4j Vector Index | Semantic article retrieval |
| **LLM** | OpenAI GPT-4 / Llama 3 | Entity extraction, Q&A |
| **Embeddings** | E5-multilingual | Multilingual embeddings |
| **API** | FastAPI | REST service |
| **UI** | Streamlit | Demo interface |
| **ETL** | Apache Airflow | Data ingestion orchestration |

## 📖 Documentation

- **[GraphRAG Concept](docs/GraphRAG-Concept.md)**: Comprehensive technical specification
- **[Ontology Specification](docs/Ontology-Specification.md)**: ELI, ECLI, EuroVoc schemas
- **[API Documentation](docs/API-Documentation.md)**: REST API reference
- **[User Guide](docs/User-Guide.md)**: End-user documentation
- **[Contributing](docs/Contributing.md)**: Development guidelines

## 🧪 Testing

```bash
# Run all tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests (requires Neo4j)
pytest tests/integration/

# Test coverage
pytest --cov=src --cov-report=html
```

Target: **100% test coverage** for core modules.

## 🗺️ Roadmap

### Phase 1: Foundation (Months 1-3) ✅
- [x] Project setup and repository
- [x] ELI ontology schema
- [x] Gesetze im Internet scraper
- [x] SGB I-III ingestion (500+ articles)
- [x] Basic Cypher queries

### Phase 2: GraphRAG Core (Months 4-6) 🔄
- [ ] LLM entity extraction pipeline
- [ ] Hybrid retrieval (vector + graph)
- [ ] Streamlit Q&A interface
- [ ] 100% test coverage

### Phase 3: EU Integration (Months 7-9)
- [ ] EUR-Lex API integration
- [ ] EuroVoc concept mapping
- [ ] ECLI case law ingestion
- [ ] Multilingual support (DE/EN/FR)

### Phase 4: Production (Months 10-12)
- [ ] FastAPI REST service with authentication
- [ ] Performance optimization (100K+ nodes)
- [ ] BA/DRV pilot deployment
- [ ] EU funding secured (SIMPL, GovTech)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/Contributing.md) for guidelines.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Pre-commit hooks
pre-commit install

# Code formatting
black src/ tests/
isort src/ tests/

# Linting
flake8 src/ tests/
mypy src/
```

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🏢 Project Team

**Cassa (Law2Logic)** - Sopra Steria Product for Regulatory Compliance

- **Product Owner**: [Your Name]
- **Tech Lead**: [Your Name]
- **Contributors**: See [CONTRIBUTORS.md](CONTRIBUTORS.md)

## 🌟 Acknowledgments

- **EU Publications Office**: ELI and ECLI standards
- **EuroVoc Team**: Multilingual thesaurus
- **Neo4j Community**: Graph database support
- **Gesetze im Internet**: German federal law portal

## 📫 Contact

- **Email**: law2logic@sopra-steria.com
- **GitHub Issues**: [Report bugs or request features](https://github.com/sopra-steria-cassa/EU-GraphRAG/issues)
- **Discussions**: [Community forum](https://github.com/sopra-steria-cassa/EU-GraphRAG/discussions)

## 🔗 Links

- **ELI Ontology**: https://op.europa.eu/en/web/eu-vocabularies/eli
- **ECLI Portal**: https://e-justice.europa.eu/ecli
- **EuroVoc Thesaurus**: https://op.europa.eu/en/web/eu-vocabularies/th-concept-scheme/-/resource/eurovoc
- **Gesetze im Internet**: https://www.gesetze-im-internet.de
- **Neo4j GraphRAG**: https://neo4j.com/labs/genai-ecosystem/

---

**⭐ Star this repository if you find it useful!**

**📢 Follow updates**: Watch this repo for the latest developments in EU legal knowledge graphs.
"""

# Save README
with open("/home/mbuchhorn/projects/EU_GraphRAG/README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("✓ Created comprehensive README.md")
print(f"  File: /home/mbuchhorn/projects/EU_GraphRAG/README.md")
