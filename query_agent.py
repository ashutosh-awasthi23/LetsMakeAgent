import sqlite3
import json
from ExpenseRecord import client

def run_sql_query(query:str):
    print(f"--->[AI is executing SQL : {query}]")
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return str(results)
    
    except Exception as e:
        conn.close()
        return f"Error: {str(e)}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "run_sql_query",
            "description": "Run a SQLite query on the 'expenses' table to answer user questions. Schema: expenses(id INTEGER, amount REAL, category TEXT, description TEXT, date TEXT)",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQLite query to run."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def ask_agent(user_question: str):
    messages = [
        {
            "role":"system",
            "content" : "You are a helpful expense assistant. Always use the run_sql_query tool to fetch data from the database before answering financial questions."
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    # <-- "completions" FIXED HERE
    response = client.chat.completions.create( 
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        name="expense_query"
    )
    response_message = response.choices[0].message

    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.function.name=="run_sql_query":
                function_args = json.loads(tool_call.function.arguments)
                query_result = run_sql_query(function_args.get("query"))
                
                messages.append(response_message)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": "run_sql_query",
                    "content": query_result
                })

                # <-- "completions" FIXED HERE
                final_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                return final_response.choices[0].message.content
    else: # <-- INDENTATION FIXED HERE
        return response_message.content

if __name__ == "__main__":
    question = "How much money have I spent on Food?"
    print(f"Question: {question}\n") 
    answer = ask_agent(question) 
    print(f"\nAnswer: {answer}")