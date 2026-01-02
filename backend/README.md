# AI Video Production System

## Overview
Professional multi-agent system for AI-powered video content generation with layered architecture.

## Architecture

```
backend/
├── core/                   # Shared infrastructure
│   ├── config/            # Configuration management
│   ├── logging/           # Observability infrastructure
│   └── utils/             # Shared utilities
├── orchestration/         # Orchestration layer
│   ├── research_orchestrator.py
│   ├── production_orchestrator.py
│   ├── session_manager.py
│   └── quality_evaluator.py
└── agents/                # Agent layer
    ├── research_agents/
    └── production_agents/
```

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run E2E Pipeline**
   ```bash
   python run_e2e.py "Your topic here"
   ```

## Development

- **Add New Agent**: See `backend/agents/README.md`
- **Configure Logging**: See `backend/core/logging/README.md`
- **Orchestration**: See `backend/orchestration/README.md`

## Migration from Legacy

The legacy `research_agency/` and `production_agency/` folders are being phased out in favor of the new `backend/` structure.
