import pandas as pd
import os
from datetime import datetime

class BakeryManagementSystem:
    def __init__(self, filename='bakery_orders.csv'):
        self.filename = filename
        if os.path.exists(self.filename):
            self.orders = pd.read_csv(self.filename)
            if not self.orders.empty:
                self.next_order_id = self.orders["Order ID"].max() + 1
            else:
                self.next_order_id = 1
        else:
            self.orders = pd.DataFrame(columns=["Order ID", "Customer Name", "Order", "Quantity", "Order Date"])
            self.next_order_id = 1
        self.log_filename = 'bakery_log.txt'
        self.backup_filename = 'bakery_orders_backup.csv'

    def save_orders(self):
        self.orders.to_csv(self.filename, index=False)

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def validate_quantity(self, quantity):
        return quantity.isdigit() and int(quantity) > 0

    def log_action(self, action):
        with open(self.log_filename, 'a') as log_file:
            log_file.write(f"{datetime.now()} - {action}\n")

    def send_notification(self, message):
        print(f"Notification: {message}")

    def add_order(self, name, order, quantity, order_date):
        if not self.validate_quantity(quantity):
            print("Invalid quantity. Please enter a positive integer.")
            return
        if not self.validate_date(order_date):
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return

        new_order = pd.DataFrame({
            "Order ID": [self.next_order_id],
            "Customer Name": [name],
            "Order": [order],
            "Quantity": [int(quantity)],
            "Order Date": [order_date]
        })
        self.orders = pd.concat([self.orders, new_order], ignore_index=True)
        self.save_orders()
        self.log_action(f"Added order ID: {self.next_order_id}")
        self.send_notification(f"New order added: {name}, {order}, {quantity}, {order_date}")
        print(f"Order added successfully with order ID: {self.next_order_id}")
        self.next_order_id += 1

    def update_order(self, order_id, name=None, order=None, quantity=None, order_date=None):
        idx = self.orders.index[self.orders["Order ID"] == order_id].tolist()
        if idx:
            if name:
                self.orders.at[idx[0], "Customer Name"] = name
            if order:
                self.orders.at[idx[0], "Order"] = order
            if quantity:
                if not self.validate_quantity(quantity):
                    print("Invalid quantity. Please enter a positive integer.")
                    return
                self.orders.at[idx[0], "Quantity"] = int(quantity)
            if order_date:
                if not self.validate_date(order_date):
                    print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                    return
                self.orders.at[idx[0], "Order Date"] = order_date
            self.save_orders()
            self.log_action(f"Updated order ID: {order_id}")
            self.send_notification(f"Order updated: {order_id}, {name}, {order}, {quantity}, {order_date}")
            print(f"Order ID {order_id} updated successfully.")
        else:
            print(f"Order ID {order_id} not found.")

    def delete_order(self, order_id):
        idx = self.orders.index[self.orders["Order ID"] == order_id].tolist()
        if idx:
            self.orders = self.orders.drop(idx)
            self.save_orders()
            self.log_action(f"Deleted order ID: {order_id}")
            self.send_notification(f"Order deleted: {order_id}")
            print(f"Order ID {order_id} deleted successfully.")
        else:
            print(f"Order ID {order_id} not found.")

    def lookup_order(self, order_id):
        order = self.orders[self.orders["Order ID"] == order_id]
        if not order.empty:
            print(order.to_string(index=False))
        else:
            print(f"Order ID {order_id} not found.")

    def filter_orders(self, customer_name=None, start_date=None, end_date=None):
        filtered_orders = self.orders
        if customer_name:
            filtered_orders = filtered_orders[filtered_orders["Customer Name"].str.contains(customer_name, case=False, na=False)]
        if start_date:
            filtered_orders = filtered_orders[filtered_orders["Order Date"] >= start_date]
        if end_date:
            filtered_orders = filtered_orders[filtered_orders["Order Date"] <= end_date]
        if filtered_orders.empty:
            print("No orders found.")
        else:
            print(filtered_orders.to_string(index=False))

    def export_orders_to_csv(self, filename):
        self.orders.to_csv(filename, index=False)
        self.log_action(f"Exported orders to {filename}")
        print(f"All orders have been exported to {filename}")

    def backup_orders(self):
        self.orders.to_csv(self.backup_filename, index=False)
        self.log_action("Backup orders")
        print(f"Backup created successfully at {self.backup_filename}")

    def restore_orders(self):
        if os.path.exists(self.backup_filename):
            self.orders = pd.read_csv(self.backup_filename)
            self.save_orders()
            self.next_order_id = self.orders["Order ID"].max() + 1
            self.log_action("Restored orders from backup")
            print("Orders restored successfully from backup.")
        else:
            print("No backup file found.")

    def order_summary(self):
        print("Order Summary")
        print("-------------")
        total_orders = len(self.orders)
        total_quantity = self.orders["Quantity"].sum()
        most_popular_order = self.orders["Order"].mode()[0] if total_orders > 0 else "None"
        print(f"Total Orders: {total_orders}")
        print(f"Total Quantity: {total_quantity}")
        print(f"Most Popular Order: {most_popular_order}")

    def authenticate_user(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        return username == "admin" and password == "password"

    def menu(self):
        if not self.authenticate_user():
            print("Authentication failed. Exiting system.")
            return

        while True:
            print("\nBakery Management System")
            print("1. Add Order")
            print("2. Update Order")
            print("3. Delete Order")
            print("4. Lookup Order")
            print("5. Filter Orders")
            print("6. Export Orders to CSV")
            print("7. Backup Orders")
            print("8. Restore Orders")
            print("9. Order Summary")
            print("10. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter customer name: ")
                order = input("Enter order: ")
                quantity = input("Enter quantity: ")
                order_date = input("Enter order date (YYYY-MM-DD): ")
                self.add_order(name, order, quantity, order_date)
            elif choice == '2':
                order_id = int(input("Enter order ID to update: "))
                name = input("Enter new customer name (leave blank to keep unchanged): ")
                order = input("Enter new order (leave blank to keep unchanged): ")
                quantity = input("Enter new quantity (leave blank to keep unchanged): ")
                order_date = input("Enter new order date (YYYY-MM-DD) (leave blank to keep unchanged): ")
                self.update_order(order_id, name or None, order or None, quantity or None, order_date or None)
            elif choice == '3':
                order_id = int(input("Enter order ID to delete: "))
                self.delete_order(order_id)
            elif choice == '4':
                order_id = int(input("Enter order ID to lookup: "))
                self.lookup_order(order_id)
            elif choice == '5':
                customer_name = input("Enter customer name to filter by (leave blank to ignore): ")
                start_date = input("Enter start date (YYYY-MM-DD) to filter by (leave blank to ignore): ")
                end_date = input("Enter end date (YYYY-MM-DD) to filter by (leave blank to ignore): ")
                self.filter_orders(customer_name or None, start_date or None, end_date or None)
            elif choice == '6':
                filename = input("Enter filename to export to (e.g., orders.csv): ")
                self.export_orders_to_csv(filename)
            elif choice == '7':
                self.backup_orders()
            elif choice == '8':
                self.restore_orders()
            elif choice == '9':
                self.order_summary()
            elif choice == '10':
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    system = BakeryManagementSystem()
    system.menu()
