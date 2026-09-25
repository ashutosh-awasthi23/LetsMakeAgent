import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langfuse.openai import OpenAI



load_dotenv()

client = OpenAI()

class ExpenseRecord(BaseModel):
    amount: float
    category : str
    description : str
    date : str

print("Foundation set! LLMOps and LLM client initialized.")