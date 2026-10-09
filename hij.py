import hashlib
import os
import json
import getpass

DATA_FILE = "passwords.json"
MASTER_FILE = "master.hash"

# --- Utility Functions ---
def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- Master Password Setup ---
def setup_master():
    if not os.path.exists(MASTER_FILE):
        print("No master password set. Please create one.")
        master = getpass.getpass("Set master password: ")
        confirm = getpass.getpass("Confirm master password: ")
        if master == confirm:
            with open(MASTER_FILE, "w") as f:
                f.write(hash_text(master))
            print("Master password set successfully!")
        else:
            print("Passwords do not match. Try again.")
            setup_master()

def verify_master():
    with open(MASTER_FILE, "r") as f:
        stored_hash = f.read().strip()
    master = getpass.getpass("Enter master password: ")
    return hash_text(master) == stored_hash

# --- Password Manager Functions ---
def add_password(data):
    site = input("Enter site/ID: ")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    hashed_pw = hash_text(password)
    data[site] = {"username": username, "password_hash": hashed_pw}
    save_data(data)
    print(f"Password for {site} saved successfully!")

def retrieve_password(data):
    site = input("Enter site/ID to search: ")
    if site in data:
        print(f"Site: {site}")
        print(f"Username: {data[site]['username']}")
        print(f"Password Hash: {data[site]['password_hash']}")
        print("⚠️ Note: Passwords are stored as hashes for security.")
    else:
        print("No entry found for that site.")

# --- Main Program ---
def main():
    setup_master()
    if not verify_master():
        print("❌ Incorrect master password. Access denied.")
        return

    data = load_data()

    while True:
        print("\n--- Password Manager ---")
        print("1. Add new password")
        print("2. Retrieve password")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_password(data)
        elif choice == "2":
            retrieve_password(data)
        elif choice == "3":
            print("Exiting Password Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
