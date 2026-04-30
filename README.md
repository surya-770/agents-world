# Agents World Simulation

A fully autonomous multi-agent simulation model designed strictly around an LLM-driven backend via Ollama, following object-oriented architectures and cleanly separated logic states.

## Overview

- **Core Loop**: Every agent observes via a perception module, decides on an action via memory, and logs votes.
- **Rules Processing**: Impostors naturally inherit deception biases using normalized Dirichlet personality mappings.
- **LLM Integration**: Re-try backed HTTP wrapper communicating with standard local Mistral/Llama3 servers.

## Running

1. Make sure you have [Ollama](https://ollama.com/) running locally with your desired model:
   ```bash
   ollama run mistral
   ```
2. Install Python requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the simulation core:
   ```bash
   python agents_world/main.py --agents 8 --impostors 2 --rounds 5
   ```
4. Run testing:
   ```bash
   pytest agents_world/tests/
   ```

*Note: This architecture is fully built in Python natively and meant to be executed over a standard Python 3.11+ environment.*
