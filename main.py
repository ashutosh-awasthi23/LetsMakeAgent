from database import init_db, save_expense_to_db
from parse_expense import parse_expense
from query_agent import ask_agent
from analytics import show_expense_summary
# 1. Naya Groq Vision Agent import karein
from vision_agent import VisionAgent 

def main():
    init_db()
    # 2. Agent ko initialize karein
    vision_agent = VisionAgent() 
    print("=== AI Expense Tracker ===")

    while True:
        print("\n" + "-"*30)
        print("What would you like to do?")
        print("1. Register a text expense")
        print("2. Ask a question about my expenses")
        print("3. View Expense Summary (Pandas)")
        print("4. Upload a Receipt Image (Groq Vision Agent)")
        print("5. Exit")
        print("-" * 30)
        
        choice = input("Enter your choice (1/2/3/4/5): ").strip()
        
        if choice == '1':
            user_input = input("\nEnter expense details: ")
            if not user_input.strip(): continue
            print("AI: Parsing and saving expense...")
            try:
                record = parse_expense(user_input)
                save_expense_to_db(record)
                print(f"AI: Success! ${record.amount} saved under '{record.category}'.")
            except Exception as e:
                print(f"AI: Error saving expense - {str(e)}")
                
        elif choice == '2':
            user_input = input("\nAsk your question: ")
            if not user_input.strip(): continue
            print("AI: Querying the database...")
            try:
                answer = ask_agent(user_input)
                print(f"\nAI Answer: {answer}")
            except Exception as e:
                print(f"AI: Error reading database - {str(e)}")
                
        elif choice == '3':
            print("\nAI: Generating Analytics report...")
            show_expense_summary()
            
        elif choice == '4':
            # 3. Groq tool-calling ko execute karein
            image_path = input("\nEnter the file path of your receipt image (e.g., test_bill.jpg): ").strip()
            if not image_path: continue
                
            print("Vision Agent: Sending receipt to Groq (LPU) for lightning-fast analysis...")
            try:
                record = vision_agent.process_image(image_path)
                save_expense_to_db(record)
                print(f"Vision Agent: Success! Extracted ${record.amount} for '{record.category}'. Saved to database!")
            except FileNotFoundError:
                print("Vision Agent: Error - Could not find the image file.")
            except Exception as e:
                print(f"Vision Agent: Error parsing receipt - {str(e)}")
            
        elif choice == '5':
            print("\nAI: Goodbye!")
            break
            
        else:
            print("\nAI: Invalid choice. Please type 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()