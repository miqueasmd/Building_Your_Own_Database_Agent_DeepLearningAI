# AI-Powered COVID-19 Data Analysis Platform

## Overview
This project creates an AI-powered platform for analyzing COVID-19 data using Azure OpenAI services and various database integrations. It demonstrates different approaches to data analysis, from simple CSV processing to complex SQL database interactions.

## Features

### 1. Data Processing & Storage
- CSV data loading and transformation
- SQLite database integration
- Automated data cleaning and standardization

### 2. AI Integration
- Azure OpenAI API integration
- Function calling capabilities
- Code interpreter implementation
- SQL query generation and execution

### 3. Analysis Capabilities
- State-by-state COVID statistics
- Historical data analysis
- Custom query support
- Multiple visualization options

## Project Structure

```
project/
├── code/
│   ├── L1_Your_First_AI_Agent.ipynb               # Create the first AI Agent
│   ├── L2_Interacting_with_CSV_Data.ipynb         # CSV data processing
│   ├── L3_Connecting_to_SQL_Database.ipynb        # SQL database setup
│   ├── L4_Azure_OpenAI_Function_Calling.ipynb     # Azure OpenAI integration
│   ├── L5_Leveraging_Assistants_API.ipynb         # AI Assistant implementation
│   └── Helper.py                                  # Utility functions
├── data/
│   └── all-states-history.csv                     # COVID-19 dataset
└── .env                                           # Environment variables
```

## Setup

1. **Environment Configuration**
```bash
pip install -r requirements.txt
```

2. **Environment Variables**
```properties
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_key
DATA_PATH=path_to_data_directory
```

3. **Azure Configuration**
```markdown
a. Create an Azure Account
- Visit portal.azure.com and sign up for an account
- If you're new to Azure, you may be eligible for free credits

b. Create an Azure OpenAI Resource
- In Azure portal, search for "Azure OpenAI"
- Click "Create" and follow setup wizard
```

## Usage Examples

### 1. Basic CSV Analysis
```python
# Load and analyze CSV data
import pandas as pd
df = pd.read_csv("data/all-states-history.csv")
```

### 2. SQL Query Generation
```python
# Generate and execute SQL queries
agent_executor_SQL.invoke("How many patients were hospitalized in Alaska?")
```

### 3. AI Assistant Integration
```python
# Create and use AI assistant
assistant = client.beta.assistants.create(
    model="gpt-35-turbo",
    instructions="Analyze COVID-19 data",
    tools=[{"type": "code_interpreter"}]
)
```

## Documentation
- Azure OpenAI Setup
- Database Schema
- API Reference

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ☕ Support Me

If you like my work, consider supporting my studies!

Your contributions will help cover fees and materials for my **Computer Science and Engineering studies at the UOC** starting in September 2025.

Every little bit helps—you can donate from as little as $1.

<a href="https://ko-fi.com/miqueasmd"><img src="https://ko-fi.com/img/githubbutton_sm.svg" /></a>

## Acknowledgements

This project is inspired by the DeepLearning.AI courses. Please visit [DeepLearning.AI](https://www.deeplearning.ai/) for more information and resources.
