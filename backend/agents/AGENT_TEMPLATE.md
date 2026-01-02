# Agent Module Template

Each agent should follow this structure for consistency and maintainability.

## Structure

```
agent_name/
├── __init__.py       # Exports agent instance and metadata
├── manifest.py       # Agent metadata and configuration
├── agent.py          # Core agent logic
├── config.py         # Agent-specific configuration
└── prompts.py        # Prompt construction and loading
```

## Files

### manifest.py
Defines agent metadata including:
- Name and description
- Version
- Capabilities
- Required sub-agents (if any)
- Model preferences

### agent.py
Contains the agent instance creation and configuration:
- Agent initialization
- Persona loading
- Tool/sub-agent registration

### config.py
Agent-specific configuration:
- Persona file path
- Guide file path
- Model overrides
- Any agent-specific parameters

### prompts.py
Prompt construction logic:
- Load persona and guides
- Construct system instructions
- Handle templating

## Usage Example

```python
from backend.agents.research_agents.data_miner import data_miner_agent, MANIFEST

# Access agent
agent = data_miner_agent

# Access metadata
print(MANIFEST.name)
print(MANIFEST.description)
print(MANIFEST.version)
```
