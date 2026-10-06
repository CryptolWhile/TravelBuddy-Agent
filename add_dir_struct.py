with open('README.md', 'r') as f:
    content = f.read()

dir_structure = """## Directory Structure

```text
.
├── agent.py                 # Main entry point to run the interactive agent
├── test.py                  # Script to run adversarial test cases
├── attack_results.md        # Detailed report on adversarial attacks
├── BaoCao.html              # Final project report
├── data/                    # Data sources (flights.json, hotels.json)
├── logs/                    # Telemetry & tracking logs (JSONLines)
├── src/
│   ├── agent/               # Agent architectural implementations
│   │   ├── graph.py         # Baseline ReAct Agent
│   │   ├── plan_and_execute.py # Plan-then-Execute Architecture
│   │   └── hybrid.py        # Hybrid Architecture (Planner/Observer)
│   ├── core/                # Core application settings
│   │   ├── llm.py           # LLM client setup and parsing
│   │   └── schemas.py       # Strict Pydantic validation models
│   ├── telemetry/           # Observability
│   │   ├── logger.py        # JSON structured event logging
│   │   └── metrics.py       # Latency and token usage tracking
│   └── utils/               # Utilities
│       └── data_store.py    # Data access and input normalization
└── requirements.txt         # Project dependencies
```

"""

content = content.replace("## Setup", dir_structure + "## Setup")

with open('README.md', 'w') as f:
    f.write(content)
print("Added directory structure successfully")
