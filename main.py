'''
Contains the main logic of the application.
Handles user authentication and menu navigation.
'''

import csv
import os
from reminder import Reminder # Written by Baran Kara
from subscription import Subscriptions # Written by Umut Akdumanlı 
from analysis import Analysis # Written by Alpay Albayrak
from payment import Payment # Written by Kübra Kalan  
from search import Search # Written by Arda ÇAM

class Application:
    def __init__(self):
        self.users = self.load_users()  # Load existing users from file
        self.username = None
        self.password = None
        
        # Construct all necessary classes
        self.subs = Subscriptions()
        self.reminder = Reminder()
        self.payment = Payment()
        self.analysis = Analysis('subscriptions.csv', 'prices.csv')
        self.search = Search()
        

    def load_users(self, filename='users.csv'):
        users = {}
        if os.path.exists(filename):  # Check if the user file exists
            with open(filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:  # Check if row is not empty
                        username, password = row
                        users[username] = password  # Populate users dictionary
        return users

    def save_user(self, username, password, filename='users.csv'):
        # Save a new user to the file
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password])

    def sign_in(self):
        # Prompt the user to sign in
        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")

        if self.username in self.users and self.users[self.username] == self.password:
            print("Sign in successful!")
            return True
        else:
            print("Invalid username or password.")
            return False

    def sign_up(self):
        # Prompt the user to sign up
        self.username = input("Choose a username: ")
        if self.username in self.users:
            print("Username already exists. Please choose a different username.")
            return

        self.password = input("Choose a password: ")
        self.users[self.username] = self.password
        self.save_user(self.username, self.password)  # Save the new user
        print("Sign up successful!")

    def display_menu(self):
        # Display the main menu and handle user choices
        while True:
            print("\nMain Menu:")
            print("1. Display")
            print("2. Payment")
            print("3. Settings")
            print("4. Exit")

            choice = input("Choose an option (1/2/3/4): ").strip()

            if choice == "1":
                self.display_submenu()  # Navigate to display submenu
            elif choice == "2":
                print("Payment selected.")
                self.payment.enter_card_details()  # Handle payment details
            elif choice == "3":
                self.settings_submenu()  # Navigate to settings submenu
            elif choice == "4":
                print("Exiting the menu.")
                break  # Exit the main menu
            else:
                print("Invalid choice. Please choose 1, 2, 3, or 4.")

    def display_submenu(self):
        # Display the submenu for various actions
        while True:
            print("\nDisplay Menu:")
            print("1. Subscription")
            print("2. Reminder")
            print("3. Expense Analysis")
            print("4. Back to Main Menu")

            choice = input("Choose an option (1/2/3/4): ").strip()

            if choice == "1":
                print("Subscription selected.")                
                self.subs.display()  # Display subscriptions
            elif choice == "2":
                print("Reminder selected.")
                self.reminder.main()  # Handle reminders
            elif choice == "3":
                print("Expense Analysis selected.")
                self.analysis.total_price(self.username)  # Display expense analysis
            elif choice == "4":
                break  # Return to main menu
            else:
                print("Invalid choice. Please choose 1, 2, 3, or 4.")

    def settings_submenu(self):
        # Display the settings submenu for configuration
        while True:
            print("\nSettings Menu:")
            print("1. Subscription")
            print("2. Search")
            print("3. Back to Main Menu")

            choice = input("Choose an option (1/2/3): ").strip()

            if choice == "1":
                print("Subscription selected.")

                print("\nSubscriptions Setting Menu:")
                print("1. Add new subscription")
                print("2. Update a subscription")
                print("3. Delete a subscription")

                sub_choice = input("Choose an option (1/2/3): ").strip()
                    
                if sub_choice == "1":
                    print("Add selected")
                    new_subscription_name = input("Enter subscribed application's name: ")
                    new_subscription_payment_date = input("Enter subscription payment day: ")
                    self.subs.add(self.username, new_subscription_name, new_subscription_payment_date)
                                        
                elif sub_choice == "2":
                    print("Update selected.")
                    old_subscription_name = input("Enter the name of the subscription to be replaced: ")
                    new_subscription_name = input("Enter subscribed application's name: ")
                    new_subscription_payment_date = input("Enter subscription payment day: ")
                    self.subs.update(self.username, old_subscription_name, new_subscription_name, new_subscription_payment_date)
                                       
                elif sub_choice == "3":
                    print("Delete selected")
                    subscription_name_to_delete = input("Enter subscription's name to delete: ")
                    self.subs.delete(self.username, subscription_name_to_delete) 
                    
            elif choice == "2":
                print("Search selected.")
                self.search.main()  # Handle search functionality
            elif choice == "3":
                break  # Return to main menu
            else:
                print("Invalid choice. Please choose 1, 2, or 3.")

    def main(self):
        # Main loop for the application
        while True:
            choice = input("Do you want to sign in, sign up, or exit? (sign in/sign up/exit): ").strip().lower()

            if choice == "sign in":
                if self.sign_in():  # If sign in is successful, display the menu
                    self.display_menu()
            elif choice == "sign up":
                self.sign_up()  # Handle user sign up
            elif choice == "exit":
                print("Exiting the program.")
                break  # Exit the application
            else:
                print("Invalid choice. Please choose 'sign in', 'sign up', or 'exit'.")

if __name__ == "__main__":
    app = Application()  # Create the application instance
    app.main()  # Run the main loop
