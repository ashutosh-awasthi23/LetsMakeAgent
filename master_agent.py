import os
from parse_expense import parse_expense
from vision_agent import VisionAgent
from database import save_expense_to_db
from CurrentConverterSchema import convert_currency_to_inr

class MasterAgent:
    def __init__(self):
        # Vision agent ko sirf ek baar initialize karenge
        self.vision_agent = VisionAgent()

    def process(self, user_input: str):
        user_input = user_input.strip()
        
        # Check karte hain ki kya input ek image file ka path hai
        valid_extensions = ('.png', '.jpg', '.jpeg')
        
        if os.path.isfile(user_input) and user_input.lower().endswith(valid_extensions):
            print("\n🤖 Master Agent: Image file detected! Routing to Vision Agent...")
            record = self.vision_agent.process_image(user_input)
            
        else:
            print("\n🤖 Master Agent: Text detected! Routing to Text Agent...")
            # Agar image nahi hai, toh normal text parser ko bhej do
            record = parse_expense(user_input)

        if original_currency != 'INR':
            original_currency = record.currency
            original_amount = record.amount
            record.amount = convert_currency_to_inr(original_amount,original_currency)
            record.currency = "INR"
            record.description = f"{record.description} (Original: {original_amount} {original_currency})"


    
        # Dono mein se jo bhi agent data laye, use database mein save kar do
        save_expense_to_db(record)
        return record