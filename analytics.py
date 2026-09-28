import sqlite3
import pandas as pd

def show_expense_summary():
    try:
        # SQLite database se connect karein
        conn = sqlite3.connect("expenses.db")
        
        # SQL query jo category ke hisaab se total calculate karegi
        query = """
        SELECT category as Category, SUM(amount) as Total_Spent 
        FROM expenses 
        GROUP BY category
        ORDER BY Total_Spent DESC
        """
        
        # Data ko seedha Pandas DataFrame mein load karein
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            print("\nAI: Abhi tak koi expenses save nahi hue hain.")
        else:
            print("\n=== Category-wise Expense Summary ===")
            # index=False karne se table clean dikhti hai
            print(df.to_string(index=False)) 
            print("=====================================\n")
            
    except Exception as e:
        print(f"\nAI: Summary generate karne mein error aayi - {str(e)}\n")