# AI Video Production System

Professional AI-powered video production pipeline using Google Gemini and Vertex AI.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 3. Run pipeline
python run_e2e_sequential.py "Your research topic"
```

## Architecture

Built with enterprise-grade layered architecture:

- **🏗️ Core Layer**: Configuration, logging, utilities
- **🤖 Agent Layer**: Modular AI agents (research + production)
- **🎯 Orchestration Layer**: Workflow management with ADK Sequential Agents
- **📊 Observability**: Comprehensive metrics, logging, error tracking

## Features

✅ **Professional Structure** - SOLID principles, clean architecture  
✅ **Full Observability** - Structured logging, metrics, error tracking  
✅ **Vertex AI Ready** - Production deployment on GCP  
✅ **Quality Validation** - Automated output quality checks  
✅ **Session Management** - Complete workflow state tracking  

## Documentation

- [Developer Guide](docs/DEVELOPER_GUIDE.md) - Complete development guide
- [Deployment Guide](docs/DEPLOYMENT.md) - Vertex AI deployment
- [API Reference](docs/API.md) - Code API documentation

## Project Structure

```
AI Video/
├── backend/
│   ├── core/           # Configuration & utilities
│   ├── agents/         # AI agents (12 total)
│   └── orchestration/  # Workflow management
├── production_references/ # Persona documents
├── docs/              # Documentation
├── outputs/           # Generated content
└── run_e2e_sequential.py # Main entry point
```

## Requirements

- Python 3.10+
- Google Cloud Platform account
- Vertex AI API enabled
- Service account with appropriate permissions

## Configuration

Create `.env`:

```bash
# Vertex AI
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GOOGLE_GENAI_USE_VERTEXAI=true

# Model
DEFAULT_MODEL=gemini-2.0-flash
MODEL_TEMPERATURE=0.7

# Logging
LOG_LEVEL=INFO
```

## Output

Research reports: `outputs/research_reports/`  
Production scripts: `outputs/production_scripts/`  
Metrics: `logs/metrics/`

## Deployment

### Staging (Cloud Run)

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-video-production
gcloud run deploy --image gcr.io/PROJECT_ID/ai-video-production
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for complete guide.

## License

Proprietary

## Support

For questions or issues, contact the development team.
