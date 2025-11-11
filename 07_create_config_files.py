
# Create requirements.txt
requirements = """# EU GraphRAG - Python Dependencies
# Last updated: November 9, 2025

# ============================================================================
# Core Dependencies
# ============================================================================
python>=3.11

# Graph Database
neo4j==5.15.0
py2neo==2021.2.3

# LLM & AI
openai==1.6.1
langchain==0.1.0
langchain-community==0.0.13
langchain-openai==0.0.2
llama-index==0.9.40
llama-index-graph-stores-neo4j==0.1.0

# Embeddings
sentence-transformers==2.2.2
transformers==4.36.0
torch==2.1.2

# Web Framework
fastapi==0.108.0
uvicorn[standard]==0.25.0
streamlit==1.29.0
pydantic==2.5.3

# Data Processing
pandas==2.1.4
numpy==1.26.2
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.4
xmltodict==0.13.0

# Web Scraping
scrapy==2.11.0
selenium==4.16.0

# ETL & Workflow
apache-airflow==2.8.0
prefect==2.14.13

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
pytest-mock==3.12.0

# Code Quality
black==23.12.1
isort==5.13.2
flake8==7.0.0
mypy==1.7.1
pre-commit==3.6.0

# Documentation
mkdocs==1.5.3
mkdocs-material==9.5.3

# Utilities
python-dotenv==1.0.0
pyyaml==6.0.1
click==8.1.7
tqdm==4.66.1
loguru==0.7.2
tenacity==8.2.3

# RDF & Ontology
rdflib==7.0.0
owlready2==0.45

# Datetime
python-dateutil==2.8.2
pytz==2023.3
"""

with open("/home/mbuchhorn/projects/EU_GraphRAG/requirements.txt", 'w') as f:
    f.write(requirements)

print("✓ Created requirements.txt")

# Create .env.example
env_example = """# EU GraphRAG Environment Variables
# Copy this file to .env and fill in your actual values

# Neo4j Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here
NEO4J_DATABASE=neo4j

# Neo4j AuraDB (Production)
# NEO4J_AURA_URI=neo4j+s://xxxxx.databases.neo4j.io
# NEO4J_AURA_USER=neo4j
# NEO4J_AURA_PASSWORD=your_aura_password

# OpenAI API
OPENAI_API_KEY=sk-your_openai_key_here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_EMBEDDING_MODEL=text-embedding-3-large

# Azure OpenAI (Optional)
# AZURE_OPENAI_API_KEY=your_azure_key
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_DEPLOYMENT=your_deployment_name
# AZURE_OPENAI_API_VERSION=2023-12-01-preview

# Local LLM (Optional)
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=llama3

# EUR-Lex API
EURLEX_API_BASE_URL=https://eur-lex.europa.eu/legal-content/EN/ALL/
EURLEX_SPARQL_ENDPOINT=http://publications.europa.eu/webapi/rdf/sparql

# Gesetze im Internet
GESETZE_BASE_URL=https://www.gesetze-im-internet.de

# Application Settings
APP_ENV=development
LOG_LEVEL=INFO
DEBUG_MODE=true

# API Keys for other services
# Add any additional API keys needed for your deployment
"""

with open("/home/mbuchhorn/projects/EU_GraphRAG/.env.example", 'w') as f:
    f.write(env_example)

print("✓ Created .env.example")

# Create .gitignore
gitignore = """# EU GraphRAG - Git Ignore File

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environments
venv/
env/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment variables
.env
.env.local
.env.*.local

# Testing
.pytest_cache/
.coverage
htmlcov/
*.cover
.hypothesis/
.tox/

# Jupyter Notebooks
.ipynb_checkpoints
*.ipynb

# Neo4j
neo4j/
*.db
*.log

# Data files (exclude large data)
data/raw/*
!data/raw/.gitkeep
data/processed/*
!data/processed/.gitkeep
data/embeddings/*
!data/embeddings/.gitkeep

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db

# Airflow
airflow/logs/
airflow.db
airflow-webserver.pid

# Temporary files
*.tmp
*.temp
.cache/

# Documentation build
site/
docs/_build/

# Secrets
secrets/
*.pem
*.key
*.crt
"""

with open("/home/mbuchhorn/projects/EU_GraphRAG/.gitignore", 'w') as f:
    f.write(gitignore)

print("✓ Created .gitignore")

# Create docker-compose.yml
docker_compose = '''version: "3.8"

services:
  # Neo4j Graph Database
  neo4j:
    image: neo4j:5.15.0-enterprise
    container_name: eu-graphrag-neo4j
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    environment:
      - NEO4J_AUTH=neo4j/password
      - NEO4J_ACCEPT_LICENSE_AGREEMENT=yes
      - NEO4J_PLUGINS=["apoc", "graph-data-science"]
      - NEO4J_dbms_security_procedures_unrestricted=apoc.*,gds.*
      - NEO4J_dbms_memory_heap_initial__size=2G
      - NEO4J_dbms_memory_heap_max__size=4G
      - NEO4J_dbms_memory_pagecache_size=2G
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
      - neo4j_import:/var/lib/neo4j/import
      - ./ontologies/graph-schema.cypher:/var/lib/neo4j/import/schema.cypher
    networks:
      - graphrag-network

  # FastAPI Application
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: eu-graphrag-api
    ports:
      - "8000:8000"
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=password
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./src:/app/src
      - ./config:/app/config
    depends_on:
      - neo4j
    networks:
      - graphrag-network
    command: uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload

  # Streamlit UI
  ui:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: eu-graphrag-ui
    ports:
      - "8501:8501"
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=password
      - API_BASE_URL=http://api:8000
    volumes:
      - ./src:/app/src
    depends_on:
      - neo4j
      - api
    networks:
      - graphrag-network
    command: streamlit run src/ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0

volumes:
  neo4j_data:
  neo4j_logs:
  neo4j_import:

networks:
  graphrag-network:
    driver: bridge
'''

with open("/home/mbuchhorn/projects/EU_GraphRAG/docker-compose.yml", 'w') as f:
    f.write(docker_compose)

print("✓ Created docker-compose.yml")

print("\n" + "="*60)
print("✅ Project setup complete!")
print("="*60)
print("\nCreated files:")
print("  - requirements.txt (Python dependencies)")
print("  - .env.example (Environment variables template)")
print("  - .gitignore (Git ignore patterns)")
print("  - docker-compose.yml (Docker stack)")
