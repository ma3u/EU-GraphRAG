
# Create requirements.txt
requirements = """# EU GraphRAG - Python Dependencies
# Last updated: November 9, 2025

# Core Dependencies
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

# Create .env.example (using string properly)
env_example = """# EU GraphRAG Environment Variables
# Copy this file to .env and fill in your actual values

# Neo4j Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here
NEO4J_DATABASE=neo4j

# OpenAI API
OPENAI_API_KEY=sk-your_openai_key_here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_EMBEDDING_MODEL=text-embedding-3-large

# Application Settings
APP_ENV=development
LOG_LEVEL=INFO
DEBUG_MODE=true
"""

with open("/home/mbuchhorn/projects/EU_GraphRAG/.env.example", 'w') as f:
    f.write(env_example)

print("✓ Created .env.example")

# Create .gitignore
gitignore = """# Python
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

# Data files
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

# Create LICENSE file
license_text = """MIT License

Copyright (c) 2025 Sopra Steria - Cassa (Law2Logic)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

with open("/home/mbuchhorn/projects/EU_GraphRAG/LICENSE", 'w') as f:
    f.write(license_text)

print("✓ Created LICENSE (MIT)")

print("\n" + "="*60)
print("✅ Essential configuration files created!")
print("="*60)
