# Smart Log Analyzer

A Python-based log analyzer that uses local LLM (Llama 3.2) to explain the errors in simple language and summarise them (again, in simple language)

## Features
- Totally local, no API, no cloud
- CLI operation (with TUI support planned)
- Detects ERROR, FATAL, Exception, and CRITICAL keywords
- Individual error analysis
- Overall summary of all errors


## Requirements
- Python 3.8 or above
- Ollama and Llama 3.2 (or 2.5)

## Installation

1. Clone this repository:
```bash
   git clone <your-repo-url>
   cd smart-log-analyzer
```

2. Install Ollama (if not already installed):
```bash
   # Visit https://ollama.ai for installation instructions
```

3. Pull the Llama model:
```bash
   ollama pull llama3.2
```

4. No Python dependencies needed - uses only standard library!


## Usage
python3 analyser.py test.log

## Example
[screenshot](screenshot.png)