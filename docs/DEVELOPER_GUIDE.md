# AI Video Production System - Developer Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Architecture Overview](#architecture-overview)
3. [Project Structure](#project-structure)
4. [Configuration](#configuration)
5. [Running the System](#running-the-system)
6. [Development Workflow](#development-workflow)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites
- Python 3.10+
- Google Cloud Platform account (for Vertex AI)
- GCP service account with Vertex AI permissions

### Installation

```bash
# 1. Clone repository
git clone <repo-url>
cd AI\ Video

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### Configuration

Create `.env` file:
```bash
# Vertex AI Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GOOGLE_GENAI_USE_VERTEXAI=true

# Model Configuration
DEFAULT_MODEL=gemini-2.0-flash
MODEL_TEMPERATURE=0.7
MAX_RETRIES=3
TIMEOUT=60

# Logging
LOG_LEVEL=INFO
DEBUG=false
```

### Run Your First Pipeline

```bash
python run_e2e_sequential.py "Your research topic here"
```

---

## Architecture Overview

### Layered Architecture

```
┌─────────────────────────────────────────┐
│         Application Layer               │
│  (run_e2e_sequential.py)                │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│       Orchestration Layer               │
│  - research_pipeline.py                 │
│  - production_pipeline.py               │
│  - session_manager.py                   │
│  - quality_evaluator.py                 │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│          Agent Layer                    │
│  - research_agents/                     │
│  - production_agents/                   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│          Core Layer                     │
│  - config/                              │
│  - logging/                             │
│  - utils/                               │
└─────────────────────────────────────────┘
```

### Key Patterns

**ADK SequentialAgent Pattern:**
- Deterministic workflow execution
- State management via `output_key`
- No reliance on function calling

**Observability First:**
- Structured logging
- Performance metrics
- Error tracking
- Execution reports

---

## Project Structure

```
AI Video/
├── backend/
│   ├── core/
│   │   ├── config/          # Settings & configuration
│   │   ├── logging/         # Observability
│   │   └── utils/           # Helper functions
│   ├── agents/
│   │   ├── research_agents/ # 6 research agents
│   │   └── production_agents/ # 6 production agents
│   └── orchestration/
│       ├── research_pipeline.py
│       ├── production_pipeline.py
│       ├── session_manager.py
│       └── quality_evaluator.py
├── outputs/
│   ├── research_reports/
│   ├── production_scripts/
│   └── sessions/
├── logs/
│   └── metrics/
├── production_references/  # Persona documents
├── run_e2e_sequential.py   # Main entry point
├── requirements.txt
├── .env                    # Configuration
└── gcp-credentials.json    # GCP service account
```

---

## Configuration

### Settings Hierarchy

1. **Environment Variables** (`.env`)
2. **`backend/core/config/settings.py`** (defaults)
3. **Runtime overrides**

### Key Configuration Classes

**APIConfig:**
- Vertex AI vs API key mode
- GCP project & location
- Model selection

**ModelConfig:**
- Research vs production models
- Temperature & parameters

**PathConfig:**
- Output directories
- Persona file locations
- Log directories

---

## Running the System

### E2E Pipeline

```bash
python run_e2e_sequential.py "Your Topic"
```

**Output:**
- Research report: `outputs/research_reports/`
- Production script: `outputs/production_scripts/`
- Session data: `outputs/sessions/`
- Metrics: `logs/metrics/`

### Individual Components

```python
from backend.orchestration.research_pipeline import research_pipeline_agent
from google.adk.runners import Runner

# Create runner
runner = Runner(agent=research_pipeline_agent, ...)

# Execute
async for event in runner.run_async(...):
    process_event(event)
```

---

## Development Workflow

### Adding a New Agent

1. Create directory structure:
```bash
mkdir -p backend/agents/research_agents/new_agent
```

2. Create required files:
```
new_agent/
├── __init__.py
├── manifest.py    # Metadata
├── prompts.py     # Instructions
└── agent.py       # LlmAgent instance
```

3. Update `__init__.py` in parent directory

4. Add to pipeline in `research_pipeline.py`

### Modifying a Pipeline

Edit `backend/orchestration/research_pipeline.py`:

```python
# Add new agent to sequence
new_agent = LlmAgent(
    name="new_agent",
    model=model,
    instruction="...",
    output_key="new_output",
    include_contents='none'
)

# Add to SequentialAgent
sub_agents=[..., new_agent]
```

---

## Testing

### Manual Testing

```bash
# Test research pipeline
python run_e2e_sequential.py "Test Topic"

# Check outputs
cat outputs/research_reports/Test_Topic_research.md
```

### Logs Analysis

```bash
# View recent logs
tail -f logs/ai_video.log

# Check metrics
cat logs/metrics/e2e_metrics_*.json | jq
```

---

## Deployment

### Staging (Vertex AI)

1. **Configure GCP:**
```bash
gcloud config set project YOUR_PROJECT_ID
gcloud services enable aiplatform.googleapis.com
```

2. **Update `.env`:**
```bash
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-project-id
```

3. **Test:**
```bash
python run_e2e_sequential.py "Staging Test"
```

### Production

1. **Container build:**
```bash
docker build -t ai-video-production .
```

2. **Deploy to Cloud Run / GKE**

3. **Set up monitoring:**
- Cloud Logging
- Error Reporting
- Cloud Monitoring

---

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure in virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Vertex AI Authentication:**
```bash
# Check service account
gcloud auth application-default login

# Verify permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID
```

**Empty Output:**
- Known ADK limitation with current model
- Use fallback mechanisms
- Consider alternative frameworks

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
export DEBUG=true

python run_e2e_sequential.py "Debug Test"
```

---

## API Reference

### Core Classes

**`Settings`**
- Global configuration management
- Environment variable loading

**`SequentialAgent`**
- ADK workflow agent
- Deterministic execution

**`Runner`**
- Execute agent workflows
- Event stream processing

### Key Methods

```python
# Create pipeline
pipeline = create_research_pipeline()

# Execute
runner = Runner(agent=pipeline, ...)
async for event in runner.run_async(...):
    handle_event(event)
```

---

## Contributing

### Code Style
- Follow PEP 8
- Type hints required
- Docstrings for all public methods

### Pull Request Process
1. Create feature branch
2. Implement changes
3. Test thoroughly
4. Update documentation
5. Submit PR

---

## Support

**Documentation:** See `/docs` directory  
**Issues:** GitHub Issues  
**Questions:** Team Slack / Email
