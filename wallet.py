import tkinter as tk
import random
import string

class FastCoinWallet:
    def __init__(self, balance=0, security_key=""):
        self.balance = balance
        self.security_key = security_key

    def earn_fastcoin(self, amount=1):
        self.balance += amount
        self.save_balance()

    def get_balance(self):
        return self.balance

    def save_balance(self):
        encrypted_balance = self.encrypt(str(self.balance))
        with open("money.txt", "w") as file:
            file.write(encrypted_balance)
        print("Balance saved to money.txt")

    def load_balance(self):
        try:
            with open("money.txt", "r") as file:
                encrypted_balance = file.read()
                self.balance = int(self.decrypt(encrypted_balance))
        except FileNotFoundError:
            self.balance = 0

    def pay_fastcoin(self, amount, url):
        if amount <= self.balance:
            self.balance -= amount
            self.save_balance()
            print(f"Paid {amount} FC to {url}")
        else:
            print("Insufficient balance")

    def encrypt(self, text):
        return ''.join(chr(ord(char) + len(self.security_key)) for char in text)

    def decrypt(self, text):
        return ''.join(chr(ord(char) - len(self.security_key)) for char in text)

    def generate_security_key(self, length=16):
        characters = string.ascii_letters + string.digits + string.punctuation
        self.security_key = ''.join(random.choice(characters) for i in range(length))
        print(f"Generated security key: {self.security_key}")

class FastCoinApp:
    def __init__(self, root, wallet):
        self.root = root
        self.wallet = wallet

        self.root.title("FastCoin 2")
        print("New next-gen fastcoin.")
        self.security_label = tk.Label(root, text="Enter your security key or generate a new one:")
        self.security_label.pack(pady=10)
        self.security_entry = tk.Entry(root)
        self.security_entry.pack(pady=10)

        self.set_security_button = tk.Button(root, text="Set Security Key", command=self.set_security_key)
        self.set_security_button.pack(pady=10)

        self.generate_key_button = tk.Button(root, text="Generate Security Key", command=self.generate_security_key)
        self.generate_key_button.pack(pady=10)

        self.balance_label = tk.Label(root, text=f"Current balance: {self.wallet.get_balance()} FC")
        self.balance_label.pack(pady=10)

        self.amount_label = tk.Label(root, text="Enter amount of FastCoin to earn per click:")
        self.amount_label.pack(pady=10)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack(pady=10)

        self.earn_button = tk.Button(root, text="Earn FastCoin", command=self.earn_fastcoin)
        self.earn_button.pack(pady=10)

        self.triple_button = tk.Button(root, text="Triple Click Earnings", command=self.triple_click_earnings)
        self.triple_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Save Balance", command=self.save_balance)
        self.save_button.pack(pady=10)

        self.url_label = tk.Label(root, text="Enter URL to send FastCoin:")
        self.url_label.pack(pady=10)
        self.url_entry = tk.Entry(root)
        self.url_entry.pack(pady=10)

        self.amount_pay_label = tk.Label(root, text="Enter amount of FastCoin to send:")
        self.amount_pay_label.pack(pady=10)
        self.amount_pay_entry = tk.Entry(root)
        self.amount_pay_entry.pack(pady=10)

        self.pay_button = tk.Button(root, text="Pay FastCoin", command=self.pay_fastcoin)
        self.pay_button.pack(pady=10)

    def set_security_key(self):
        security_key = self.security_entry.get()
        self.wallet.security_key = security_key
        self.wallet.load_balance()
        self.balance_label.config(text=f"Current balance: {self.wallet.get_balance()} FC")
        print("Security key set")

    def generate_security_key(self):
        self.wallet.generate_security_key()
        self.security_entry.delete(0, tk.END)
        self.security_entry.insert(0, self.wallet.security_key)
        self.wallet.load_balance()
        self.balance_label.config(text=f"Current balance: {self.wallet.get_balance()} FC")

    def earn_fastcoin(self):
        try:
            amount = int(self.amount_entry.get())
            self.wallet.earn_fastcoin(amount)
            self.balance_label.config(text=f"Current balance: {self.wallet.get_balance()} FC")
        except ValueError:
            print("Please enter a valid amount")

    def triple_click_earnings(self):
        try:
            amount = int(self.amount_entry.get())
            self.wallet.earn_fastcoin(amount * 3)
            self.balance_label.config(text=f"Current balance: {self.wallet.get_balance()} FC")
        except ValueError:
            print("Please enter a valid amount")

    def save_balance(self):
        self.wallet.save_balance()
        print("Balance saved manually")

    def pay_fastcoin(self):
        url = self.url_entry.get()
        try:
            amount = int(self.amount_pay_entry.get())
            self.wallet.pay_fastcoin(amount, url)
            self.balance_label.config(text=f"Current balance: {self.wallet.get_balance()} FC")
        except ValueError:
            print("Please enter a valid amount")

def main():
    wallet = FastCoinWallet()
    root = tk.Tk()
    app = FastCoinApp(root, wallet)
    root.mainloop()

if __name__ == "__main__":
    main()

    root.mainloop()

if __name__ == "__main__":
    main()
