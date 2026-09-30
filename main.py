from database import init_db
from query_agent import ask_agent
from analytics import show_expense_summary
# 1. Purane agents ki jagah ab sirf MasterAgent import karenge
from master_agent import MasterAgent

def main():
    init_db()
    # 2. Master Agent ko initialize kiya
    master = MasterAgent()
    print("=== Multimodal AI Expense Tracker ===")

    while True:
        print("\n" + "-"*30)
        print("What would you like to do?")
        # 3. Menu chhota ho gaya hai (Text aur Image combine ho gaye)
        print("1. Add an Expense (Type a sentence OR enter an image path)")
        print("2. Ask a question about my expenses")
        print("3. View Expense Summary")
        print("4. Exit")
        print("-" * 30)
        
        choice = input("Enter your choice (1/2/3/4): ").strip()
        
        if choice == '1':
            user_input = input("\nEnter expense details or image path (e.g., test_bill.jpg): ")
            if not user_input.strip(): continue
            
            try:
                # Master Agent ko directly user input de diya, baaki wo khud handle karega
                record = master.process(user_input)
                print(f"✅ Success! ${record.amount} saved under '{record.category}'.")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                
        elif choice == '2':
            user_input = input("\nAsk your question: ")
            if not user_input.strip(): continue
            print("🤖 AI: Querying the database...")
            try:
                answer = ask_agent(user_input)
                print(f"\nAI Answer: {answer}")
            except Exception as e:
                print(f"❌ Error reading database: {str(e)}")
                
        elif choice == '3':
            print("\n📊 Generating Analytics report...")
            show_expense_summary()
            
        elif choice == '4':
            print("\nGoodbye! 👋")
            break
            
        else:
            print("\nInvalid choice. Please type 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()