import os
import base64
import json
from groq import Groq
from parse_expense import ExpenseRecord
from dotenv import load_dotenv


load_dotenv()

class VisionAgent:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        # Groq ka vision model
        self.model = "llama-3.2-90b-vision-preview"

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def process_image(self, image_path: str) -> ExpenseRecord:
        base64_image = self.encode_image(image_path)
        
        # Proper Tool Definition (Function Calling)
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "save_receipt_expense",
                    "description": "Extracts bill details from the receipt and saves them.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "amount": {
                                "type": "number", 
                                "description": "The total final bill amount on the receipt."
                            },
                            "category": {
                                "type": "string", 
                                "description": "The guessed category of the expense (e.g., Groceries, Dining, Utilities)."
                            },
                            "description": {
                                "type": "string", 
                                "description": "A very short description of the purchased items."
                            }
                        },
                        "required": ["amount", "category", "description"]
                    }
                }
            }
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    'role': 'system', 
                    'content': 'You are a Vision AI Agent. Analyze the image and use the provided tool to extract data.'
                },
                {
                    'role': 'user', 
                    'content': [
                        {"type": "text", "text": "Read this receipt and call the tool to save the details."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            tools=tools,
            # Force the model to use our specific tool
            tool_choice={"type": "function", "function": {"name": "save_receipt_expense"}},
            temperature=0.1
        )
        
        # Tool call ke arguments extract karna
        tool_call = response.choices[0].message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        
        # Pydantic model mein pass karke return karna
        return ExpenseRecord(**arguments)