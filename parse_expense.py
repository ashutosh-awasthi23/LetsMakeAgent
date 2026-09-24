
from datetime import date
from ExpenseRecord import ExpenseRecord,client
def parse_expense(user_input:str)->ExpenseRecord:
    today_date = date.today().isoformat()
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {
                "role" : "system",
                "content" : f"You are a strict data extractor. You must output ONLY a valid raw JSON object. Do not use markdown, code blocks, or bullet points. Exact JSON schema required: {{\"amount\": float, \"category\": str, \"description\": str, \"date\": str}}. Today is {today_date}."
            },
            {
                "role": "user", 
                "content": user_input
            }
        ]
    )
    raw_json =  response.choices[0].message.content
    return ExpenseRecord.model_validate_json(raw_json)
if __name__== "__main__":
    test_sentence = "I grabbed a $12 sandwich for lunch yesterday."
    result = parse_expense(test_sentence)
    print(result.model_dump_json(indent=2))
