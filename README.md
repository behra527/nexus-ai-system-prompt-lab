# System Prompt Engineering Lab

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-red?logo=streamlit)
![OpenRouter](https://img.shields.io/badge/API-OpenRouter-purple)
![Grok](https://img.shields.io/badge/LLM-Grok%204.3-black)
![Pydantic](https://img.shields.io/badge/Validation-Pydantic-e92063?logo=pydantic)
![Status](https://img.shields.io/badge/Status-Completed-success)

An interactive Streamlit application for designing, testing, and validating **LLM system prompts** using Grok 4.3 through OpenRouter.

## Overview

This project demonstrates how system prompts can control an LLM's:

* Role
* Tone
* Response style
* Accuracy requirements
* Output format
* Safety boundaries

The application dynamically builds system prompts and evaluates the generated responses for structure, compliance, and basic security issues.

## Key Features

* Dynamic system prompt builder
* Configurable roles, tones, and response styles
* Strict JSON output mode
* Pydantic response validation
* Prompt compliance evaluation
* Prompt-injection testing
* Basic secret detection
* Token usage tracking
* Experiment history
* Streamlit-based interface

## Architecture

```text
User Configuration
       ↓
System Prompt Builder
       ↓
System Prompt + User Prompt
       ↓
OpenRouter
       ↓
Grok 4.3
       ↓
Response Validation
       ↓
Compliance & Security Evaluation
       ↓
Experiment Metrics
```

## Project Structure

```text
system-prompt-engineering-lab/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── src/
│   ├── grok_client.py
│   ├── prompt_builder.py
│   ├── prompts.py
│   ├── schemas.py
│   ├── validator.py
│   ├── evaluator.py
│   └── security.py
│
└── tests/
    ├── test_validator.py
    └── test_prompt_builder.py
```

## Tech Stack

* **Python**
* **Streamlit**
* **Grok 4.3**
* **OpenRouter**
* **OpenAI Python SDK**
* **Pydantic**
* **Pandas**

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/system-prompt-engineering-lab.git
cd system-prompt-engineering-lab
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Never commit your API key to the repository.

### 4. Run the Application

```bash
streamlit run app.py
```

## Example

**System Configuration**

```text
Role: Senior AI Engineer
Tone: Professional
Response Style: Step-by-step
Output Format: Strict JSON
Safety Level: Strict
Accuracy Level: Very High
```

**User Prompt**

```text
Design a production architecture for a RAG application.
```

The application generates the response and then validates and evaluates it.

## Security Testing

The application includes basic tests for:

* System prompt extraction
* Secret extraction
* Instruction override
* Role override

These checks are designed for experimentation and are not intended to replace a complete production LLM security framework.

## Testing

Run the test suite with:

```bash
pytest
```

## License

This project is intended for educational and AI engineering experimentation.
