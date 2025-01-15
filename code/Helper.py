from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()
data_path = os.getenv('DATA_PATH')
csv_path = os.path.join(data_path, "all-states-history.csv")
AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-05-01-preview"
)


# Load the data and create the database 
df = pd.read_csv(os.path.join(csv_path)).fillna(value=0)
database_file_path = os.path.join(data_path, "test.db")
engine = create_engine(f'sqlite:///{database_file_path}')
df.to_sql('all_states_history', con=engine, if_exists='replace', index=False)

# Define the tools for the LLM
tools_sql = [
    {
        "type": "function",
        "function": {
            "name": "get_hospitalized_for_state_on_date",
            "description": """Retrieves the number of hospitalized people
                              for a specific state on a specific date.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "state_abbr": {
                        "type": "string",
                        "description": """The abbreviation of the state
                                          (e.g., 'NY', 'CA')."""
                    },
                    "specific_date": {
                        "type": "string",
                        "description": """The specific date for
                                          the query in 'M/D/YYYY'
                                          format."""
                    }
                },
                "required": ["state_abbr", "specific_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_positive_cases_for_state_on_date",
            "description": """Retrieves the number of positive cases
                              for a specific state on a specific date.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "state_abbr": {
                        "type": "string",
                        "description": """The abbreviation of the 
                                          state (e.g., 'NY', 'CA')."""
                    },
                    "specific_date": {
                        "type": "string",
                        "description": """The specific date for the
                                          query in 'M/D/YYYY'
                                          format."""
                    }
                },
                "required": ["state_abbr", "specific_date"]
            }
        }
    }
]

# Define the functions
def get_hospitalized_for_state_on_date(state_abbr, specific_date):
    try:
        query = f"""
        SELECT date, state, hospitalized
        FROM all_states_history
        WHERE state = '{state_abbr}' AND date = '{specific_date}';
        """
        query = text(query)

        with engine.connect() as connection:
            result = pd.read_sql_query(query, connection)
        if not result.empty:
            return result.to_dict('records')[0]
        else:
            return np.nan
    except Exception as e:
        print(e)
        return np.nan

def get_positive_cases_for_state_on_date(state_abbr, specific_date):
    try:
        query = f"""
        SELECT date, state, positive AS positive_cases
        FROM all_states_history
        WHERE state = '{state_abbr}' AND date = '{specific_date}';
        """
        with engine.connect() as connection:
            result = pd.read_sql_query(query, connection)
        if not result.empty:
            return result.to_dict('records')[0]
        else:
            return np.nan
    except Exception as e:
        print(e)
        return np.nan

if __name__ == '__main__':
    # Example usage with the LLM
    messages = [
    {"role": "user",
        "content": """ how many hospitalized people and positive cases we had in Alaska
                    the 3/7/2021?"""
    }
    ]

    response = client.chat.completions.create(
    model="gpt-35-turbo",
    messages=messages,
    tools=tools_sql,
    tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        print(tool_calls)

        available_functions = {
            "get_positive_cases_for_state_on_date": get_positive_cases_for_state_on_date,
            "get_hospitalized_increase_for_state_on_date": get_hospitalized_for_state_on_date
        }  
        messages.append(response_message)  

        results = {}

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        if function_name in available_functions:
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                state_abbr=function_args.get("state_abbr"),
                specific_date=function_args.get("specific_date"),
            )
            results[function_name] = function_response
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            ) 
        else:
            print(f"Function {function_name} is not available.")
    print(messages)

    # Combine results into a single response
    hospitalized_info = results.get("get_hospitalized_for_state_on_date", {})
    positive_cases_info = results.get("get_positive_cases_for_state_on_date", {})

    final_response_content = (
        f"On {hospitalized_info.get('date', 'the specified date')}, "
        f"there were {hospitalized_info.get('hospitalized', 'an unknown number of')} hospitalized people in {hospitalized_info.get('state', 'the specified state')}."
        f" The number of positive cases on that date was {positive_cases_info.get('positive', 'not provided')}."
    )

    messages.append(
        {
            "role": "assistant",
            "content": final_response_content,
        }
    )

    second_response = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=messages,
    )

    # Organize and print the final response
    final_message = second_response.choices[0].message.content
    print("\nFinal Response:")
    print(final_message)