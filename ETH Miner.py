import random
import string
import sys
import sqlite3
import requests
from colorama import init, Fore
import tkinter as tk
from tkinter import messagebox

init()

# CoinGecko API URL
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

def print_eth_miner_banner():
    banner = r"""
  _____ _____ _   _   __  __ _                  __     ___ 
 | ____|_   _| | | | |  \/  (_)_ __   ___ _ __  \ \   / / |
 |  _|   | | | |_| | | |\/| | | '_ \ / _ \ '__|  \ \ / /| |
 | |___  | | |  _  | | |  | | | | | |  __/ |      \ V / | |
 |_____| |_| |_| |_| |_|  |_|_|_| |_|\___|_|       \_/  |_|
                                                              
===========================================================================
                                 ETH Miner v1
===========================================================================
"""

    print(banner)


def get_ethereum_price():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return data.get("ethereum", {}).get("usd")
    else:
        return None


def mine_ethereum(difficulty):
    target = "0" * difficulty
    attempts = 0
    eth_found = 0
    total_money = 0

    while True:
        attempts += 1
        hash_attempt = ''.join(random.choice(string.hexdigits) for _ in range(64))

        if hash_attempt.startswith(target):
            eth_amount = random.uniform(0.1, 0.5)  # Adjust the range to your desired maximum value
            eth_found += eth_amount

            eth_price = get_ethereum_price()
            if eth_price is not None:
                eth_value = eth_amount * eth_price
                total_money += eth_value

                print(f"[ {Fore.GREEN}FOUND{Fore.WHITE} ] {Fore.GREEN}{eth_amount:.4f} ETH! Total Money: {total_money:.2f} USD{Fore.RESET}")
                break  # Exit the loop if a valid hash is found
            else:
                print(f"[ {Fore.GREEN}FOUND{Fore.WHITE} ] {Fore.GREEN}{eth_amount:.4f} ETH! Total Money: {total_money:.2f} USD{Fore.RESET}")
        else:
            print(f"[ {Fore.RED}FAILED{Fore.WHITE} ] {Fore.RED}To find a valid hash. Attempts: {attempts}{Fore.RESET}")

    print(f"Total ETH Found: {eth_found:.4f}")
    print(f"Total Money: {total_money:.2f} USD")


def create_account(connection):
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    # Check if username already exists
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Error", "Username already exists. Please try again.")
    else:
        # Insert the new account into the database
        cursor.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, password))
        connection.commit()
        messagebox.showinfo("Success", "Account created successfully!")


def login(connection):
    while True:
        print("1. Login")
        print("2. Create an account")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            # Check if the provided credentials are valid
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM accounts WHERE username = ? AND password = ?", (username, password))
            logged_in_user = cursor.fetchone()

            if logged_in_user:
                return username
            else:
                print("Invalid username or password. Please try again.")

        elif choice == "2":
            create_account(connection)

        else:
            print("Invalid choice. Please try again.")


# Connect to the SQLite database
connection = sqlite3.connect("accounts.db")

# Create the accounts table if it doesn't exist
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS accounts (username TEXT PRIMARY KEY, password TEXT)")

# Perform account login or create an account
print("Welcome to ETH Miner v1")
print_eth_miner_banner()
logged_in_username = login(connection)
print(f"Login successful! Welcome, {logged_in_username}.")

# Start mining
difficulty_level = 6
mine_ethereum(difficulty_level,)

# Wait for user input before closing the console window
input("Press Enter to exit...")
