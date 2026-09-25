from datetime import date
from ExpenseRecord import ExpenseRecord, client
from database import save_expense_to_db, init_db

def parse_expense(user_input: str) -> ExpenseRecord:
    today_date = date.today().isoformat()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"You are a strict data extractor. You must output ONLY a valid raw JSON object. Do not use markdown, code blocks, or bullet points. Exact JSON schema required: {{\"amount\": float, \"category\": str, \"description\": str, \"date\": str}}. Today is {today_date}."
            },
            {
                "role": "user", 
                "content": user_input
            }
        ],
        response_format={"type": "json_object"},
        name="expense_parsing"
    )
    raw_json = response.choices[0].message.content
    return ExpenseRecord.model_validate_json(raw_json)

if __name__ == "__main__":
    init_db() # Ensure database is ready
    
    test_sentence = "I grabbed a $12 sandwich for lunch yesterday."
    print(f"Analyzing: '{test_sentence}'...\n")
    
    result = parse_expense(test_sentence)
    save_expense_to_db(result) # Save to database
    
    print("Saved to DB! Parsed Result:")
    print(result.model_dump_json(indent=2))