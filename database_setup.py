import sqlite3

def initialize_db(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the accounts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        mpid TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        balance INTEGER NOT NULL
    );
    ''')
    
    # Create the past_trades table (fill in trade details)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS past_trades (
        trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
        mpid TEXT NOT NULL,
        trade_details TEXT NOT NULL,
        FOREIGN KEY (mpid) REFERENCES accounts(mpid)
    );
    ''')
    
    # Create the positions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS positions (
        position_id INTEGER PRIMARY KEY AUTOINCREMENT,
        mpid TEXT NOT NULL,
        ticker TEXT NOT NULL,
        volume INTEGER NOT NULL,
        FOREIGN KEY (mpid) REFERENCES accounts(mpid)
    );
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_path = 'accounts.db'
    initialize_db(db_path)