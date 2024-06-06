'''
Functions related to subscription management (add, update, delete, search).
'''
import csv
import os
from tabulate import tabulate

class Subscriptions:
    def __init__(self, username=None):
        """
        Initializes the Subscriptions class with an optional username.
        Loads subscriptions from the CSV file.
        """
        self.username = username
        self.subscriptions = self.load_subscriptions()

    def load_subscriptions(self):
        """
        Loads subscriptions from the 'subscriptions.csv' file.
        Returns a list of subscriptions where each subscription is represented as a dictionary.
        """
        subscriptions = []
        if os.path.exists('subscriptions.csv'):
            with open('subscriptions.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    subscriptions.append({
                        "username": row[0],
                        "subscription_name": row[1],
                        "payment_day": row[2]
                    })
        return subscriptions

    def add(self, username, subscription_name, payment_day):
        """
        Adds a new subscription to the list and saves it to the CSV file.
        """
        self.subscriptions.append({
            "username": username,
            "subscription_name": subscription_name,
            "payment_day": payment_day
        })
        self.save_subscriptions()

    def update(self, username, old_subscription_name, new_subscription_name, new_payment_day):
        """
        Updates an existing subscription with a new name and payment day.
        If the subscription is not found, prints an error message.
        """
        found = False
        for subscription in self.subscriptions:
            if subscription["username"] == username and subscription["subscription_name"] == old_subscription_name:
                subscription["subscription_name"] = new_subscription_name
                subscription["payment_day"] = new_payment_day
                found = True
                break
        if found:
            self.save_subscriptions()
        else:
            print(f"Subscription '{old_subscription_name}' for user '{username}' not found.")

    def delete(self, username, subscription_name):
        """
        Deletes a subscription from the list and saves the updated list to the CSV file.
        If the subscription is not found, prints an error message.
        """
        found = False
        for subscription in self.subscriptions:
            if subscription["username"] == username and subscription["subscription_name"] == subscription_name:
                self.subscriptions.remove(subscription)
                found = True
                break
        if found:
            self.save_subscriptions()
        else:
            print(f"Subscription '{subscription_name}' for user '{username}' not found.")

    def search(self, username, subscription_name):
        """
        Searches for a subscription by username and subscription name.
        Returns True if found, otherwise returns False.
        """
        for subscription in self.subscriptions:
            if subscription["username"] == username and subscription["subscription_name"] == subscription_name:
                return True
        return False

    def save_subscriptions(self):
        """
        Saves the current list of subscriptions to the 'subscriptions.csv' file.
        """
        with open('subscriptions.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for subscription in self.subscriptions:
                writer.writerow([subscription["username"], subscription["subscription_name"], subscription["payment_day"]])

    def display(self):
        """
        Displays the subscriptions in a tabular format.
        If a username is specified, filters the subscriptions by that user.
        Uses the 'tabulate' library to format the output.
        """
        if self.subscriptions:
            headers = ["Username", "Subscription Name", "Payment Day"]
            if self.username:
                rows = [[s["username"], s["subscription_name"], s["payment_day"]] for s in self.subscriptions if s["username"] == self.username]
            else:
                rows = [[s["username"], s["subscription_name"], s["payment_day"]] for s in self.subscriptions]
            if rows:
                print(tabulate(rows, headers, tablefmt="grid"))
            else:
                print(f"No subscriptions found for user '{self.username}'.")
        else:
            print("No subscriptions found.")

# Example usage:
if __name__ == "__main__":
    sub_manager = Subscriptions()

    # Add a new subscription
    sub_manager.add('john_doe', 'Netflix', '15')
    
    # Update an existing subscription
    sub_manager.update('john_doe', 'Netflix', 'Amazon Prime', '20')
    
    # Delete a subscription
    sub_manager.delete('john_doe', 'Amazon Prime')
    
    # Search for a subscription
    found = sub_manager.search('john_doe', 'Netflix')
    print("Subscription found:", found)
    
    # Display all subscriptions
    sub_manager.display()

