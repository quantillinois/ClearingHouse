import zmq
import sqlite3
from typing import Dict
import hashlib

def hash_password(password: str) -> str:
    """
    Hashes a password using SHA-256 and returns the hexadecimal representation.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def populate_accounts(db_path) -> Dict[str, str]:
    accounts = {}
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
                    SELECT mpid, password
                    FROM accounts
                    ''')

    rows = cursor.fetchall()

    for row in rows:
        mpid, password = row
        accounts[mpid] = password

    conn.close()
    return accounts

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    accounts = populate_accounts("accounts.db")

    while True:
        # Wait for the next request from a client
        message = socket.recv_json()
        mpid = message.get("mpid")
        password = message.get("password")
        hashed_password = hash_password(password)
        # Check credentials
        if mpid in accounts and accounts[mpid] == hashed_password:
            response = "Success"
        else:
            response = "Failure"

        socket.send_string(response)

if __name__ == "__main__":
    main()