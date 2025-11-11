#!/bin/bash
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
