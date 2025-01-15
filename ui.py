import tkinter as tk
import re
from tkinter import messagebox, ttk
from stock_api import get_stock_price, search_stock_symbol, get_top_stocks
from email_utils import send_email_notification

def display_stock_details(root, stock_name_entry):
    stock_name = stock_name_entry.get().strip()
    if not stock_name:
        messagebox.showwarning("Avertisment", "Introduceți numele unui stoc.")
        return

    stock_symbol = search_stock_symbol(stock_name)
    if not stock_symbol:
        return

    stock_details = get_stock_price(stock_symbol)
    if stock_details:
        details_window = tk.Toplevel(root)
        details_window.title(f"Detalii pentru {stock_name}")
        details_window.configure(bg="#2e2e2e")

        current_price = stock_details.get("current", "N/A")
        change = stock_details.get("change", "N/A")
        percent = stock_details.get("percent", "N/A")

        tk.Label(details_window, text=f"Simbol: {stock_symbol}", font=("Helvetica", 12, "bold"), bg="#2e2e2e", fg="white").pack(pady=5)
        tk.Label(details_window, text=f"Preț curent: {current_price}", font=("Helvetica", 12), bg="#2e2e2e", fg="white").pack(pady=5)
        tk.Label(details_window, text=f"Schimbare: {change} ({percent}%)", font=("Helvetica", 12), bg="#2e2e2e", fg="white").pack(pady=5)

        def open_alert_window():
            alert_window = tk.Toplevel(details_window)
            alert_window.title("Setare Alerte")
            alert_window.configure(bg="#2e2e2e")

            tk.Label(alert_window, text="Valoare țintă:", font=("Helvetica", 10), bg="#2e2e2e", fg="white").grid(row=0, column=0, pady=5, padx=5)
            target_price_entry = tk.Entry(alert_window, width=30, bg="#3e3e3e", fg="white", insertbackground="white")
            target_price_entry.grid(row=0, column=1, pady=5, padx=5)

            tk.Label(alert_window, text="Adresa de email:", font=("Helvetica", 10), bg="#2e2e2e", fg="white").grid(row=1, column=0, pady=5, padx=5)
            email_entry = tk.Entry(alert_window, width=30, bg="#3e3e3e", fg="white", insertbackground="white")
            email_entry.grid(row=1, column=1, pady=5, padx=5)

            tk.Label(alert_window, text="Tip notificare:", font=("Helvetica", 10), bg="#2e2e2e", fg="white").grid(row=2, column=0, pady=5, padx=5)
            notification_type = ttk.Combobox(alert_window, values=["Creștere", "Scădere", "Atinge valoarea"], state="readonly")
            notification_type.grid(row=2, column=1, pady=5, padx=5)
            notification_type.current(0)

            def validate_email(email):
                pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                return re.match(pattern, email)

            def set_alert():
                target_price = target_price_entry.get().strip()
                user_email = email_entry.get().strip()
                notification_option = notification_type.get()

                if not target_price or not user_email:
                    messagebox.showwarning("Avertisment", "Toate câmpurile sunt obligatorii.")
                    return

                if not validate_email(user_email):
                    messagebox.showerror("Eroare", "Introduceți o adresă de email validă.")
                    return

                try:
                    target_price = float(target_price)
                    if (notification_option == "Creștere" and stock_details["current"] >= target_price) or \
                       (notification_option == "Scădere" and stock_details["current"] <= target_price) or \
                       (notification_option == "Atinge valoarea" and stock_details["current"] == target_price):
                        send_email_notification(user_email, stock_symbol, stock_details["current"], notification_option, target_price)
                    else:
                        messagebox.showinfo("Info", "Alerte setată cu succes!")
                except ValueError:
                    messagebox.showerror("Eroare", "Valoarea țintă trebuie să fie un număr valid.")

            tk.Button(alert_window, text="Setează alertă", command=set_alert, bg="#007acc", fg="white", relief="flat", activebackground="#005999").grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(details_window, text="Setează alertă", command=open_alert_window, bg="#007acc", fg="white", relief="flat", activebackground="#005999").pack(pady=10)


def show_top_stocks(root):
    top_stocks = get_top_stocks()
    if top_stocks:
        top_window = tk.Toplevel(root)
        top_window.title("Top 10 Stocuri")
        top_window.configure(bg="#2e2e2e")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Helvetica", 10), rowheight=25, background="#3e3e3e", fieldbackground="#3e3e3e", foreground="white")
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#007acc", foreground="white")

        tree = ttk.Treeview(top_window, columns=("Symbol", "Description", "Price", "Change"), show="headings")
        tree.heading("Symbol", text="Simbol")
        tree.heading("Description", text="Descriere")
        tree.heading("Price", text="Preț")
        tree.heading("Change", text="Schimbare")

        for stock in top_stocks:
            symbol = stock["symbol"]
            description = stock.get("description", "N/A")
            price = stock.get("current", "N/A")
            change = stock.get("change", "N/A")

            try:
                change_value = float(change)
            except (ValueError, TypeError):
                change_value = 0

            tags = ("positive",) if change_value > 0 else ("negative",)
            tree.insert("", "end", values=(symbol, description, price, change), tags=tags)

        tree.tag_configure("positive", foreground="green")
        tree.tag_configure("negative", foreground="red")

        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
