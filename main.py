from database import init_db, save_expense_to_db
from parse_expense import parse_expense
from query_agent import ask_agent
from analytics import show_expense_summary
def main():
    init_db()
    print("++++++++++++++++++AI Expense Tracker+++++++++++++++++++++++")

    while True :
        print("\n" + "-"*30)
        print("What would you like to do?")
        print("1. Register a new expense")
        print("2. Ask a question about my expenses")
        print("3. Exit")
        print("-" * 30)

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            user_input = input("\nEnter expense details (e.g., 'Paid $20 for a taxi'): ")
            if not user_input.strip(): continue

            print("AI: Parsing and saving expense...")

            try:
                record = parse_expense(user_input)
                save_expense_to_db(record)
                print(f"AI: Success! ${record.amount} saved under '{record.category}'.")
            except Exception as e:
                print(f"AI: Error saving expense - {str(e)}")

        elif choice == '2':
            user_input = input("\nAsk your question (e.g., 'How much did I spend on food?'): ")
            if not user_input.strip(): continue
            print("AI: Querying the database...")

            try:
                answer = ask_agent(user_input)
                print(f"\nAI Answer: {answer}")
                
            except Exception as e:
                print(f"AI: Error reading database - {str(e)}")
        elif choice == '3':
                    print("\nAI: Analytics report generate kar raha hoon...")
                    show_expense_summary()
            
        elif choice == '4':
            print("\nAI: Goodbye!")
            break

        else:
            print("\nAI: Invalid choice. Please type 1, 2, or 3.")
if __name__ == "__main__":
    main()