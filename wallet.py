import tkinter as tk
from cryptography.fernet import Fernet

class FastCoinWallet:
    def __init__(self, balance=0):
        self.balance = balance
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def earn_fastcoin(self, amount=1):
        self.balance += amount
        self.save_balance()

    def get_balance(self):
        return self.balance

    def save_balance(self):
        encrypted_balance = self.cipher.encrypt(str(self.balance).encode())
        with open("money.txt", "wb") as file:
            file.write(encrypted_balance)

    def load_balance(self):
        try:
            with open("money.txt", "rb") as file:
                encrypted_balance = file.read()
                self.balance = int(self.cipher.decrypt(encrypted_balance).decode())
        except FileNotFoundError:
            self.balance = 0

    def pay_fastcoin(self, amount, url):
        if amount <= self.balance:
            self.balance -= amount
            self.save_balance()
            print(f"Paid {amount} FC to {url}")
        else:
            print("Insufficient balance")

class FastCoinApp:
    def __init__(self, root, wallet):
        self.root = root
        self.wallet = wallet

        self.root.title("FastCoin")

        self.balance_label = tk.Label(root, text=f"Current balance: {self.wallet.get_balance()} FC")
        self.balance_label.pack(pady=10)

        self.earn_button = tk.Button(root, text="Earn 1 FC", command=self.earn_fastcoin)
        self.earn_button.pack(pady=10)

        self.url_label = tk.Label(root, text="Enter URL to send FastCoin:")
        self.url_label.pack(pady=10)
        self.url_entry = tk.Entry(root)
        self.url_entry.pack(pady=10)

        self.amount_label = tk.Label(root, text="Enter amount of FastCoin to send:")
        self.amount_label.pack(pady=10)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack(pady=10)

        self.pay_button = tk.Button(root, text="Pay FastCoin", command=self.pay_fastcoin)
        self.pay_button.pack(pady=10)

    def earn_fastcoin(self):
        self.wallet.earn_fastcoin()
        self.balance_label.config(text=f"Current balance: {self.wallet.get_balance()} FC")

    def pay_fastcoin(self):
        url = self.url_entry.get()
        try:
            amount = int(self.amount_entry.get())
            self.wallet.pay_fastcoin(amount, url)
            self.balance_label.config(text=f"Current balance: {self.wallet.get_balance()} FC")
        except ValueError:
            print("Please enter a valid amount")

def main():
    wallet = FastCoinWallet()
    wallet.load_balance()
    root = tk.Tk()
    app = FastCoinApp(root, wallet)
    root.mainloop()

if __name__ == "__main__":
    main()
