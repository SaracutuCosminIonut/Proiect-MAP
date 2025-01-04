import urllib.request
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import messagebox, ttk

# Configurații utilizator
STOCK_API_URL = "https://finnhub.io/api/v1/quote"
SEARCH_API_URL = "https://finnhub.io/api/v1/search"
TRENDING_API_URL = "https://finnhub.io/api/v1/stock/symbol"
API_KEY = "ctsl3epr01qin3c01btgctsl3epr01qin3c01bu0"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Funcție pentru a obține prețul stocului
def get_stock_price(stock_symbol):
    try:
        url = f"{STOCK_API_URL}?symbol={stock_symbol}&token={API_KEY}"
        with urllib.request.urlopen(url) as response:
            data = response.read()
            parsed_data = json.loads(data)
            return {
                "current": parsed_data.get("c", None),
                "change": parsed_data.get("d", None),
                "percent": parsed_data.get("dp", None)
            }
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la obținerea prețului stocului: {e}")
        return None

# Funcție pentru a căuta simbolul unui stoc după nume
def search_stock_symbol(stock_name):
    try:
        url = f"{SEARCH_API_URL}?q={stock_name}&token={API_KEY}"
        with urllib.request.urlopen(url) as response:
            data = response.read()
            parsed_data = json.loads(data)
            if parsed_data["count"] > 0:
                return parsed_data["result"][0]["symbol"]  # Primul rezultat
            else:
                messagebox.showinfo("Info", "Nu s-a găsit niciun simbol pentru acest nume de stoc.")
                return None
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la căutarea simbolului stocului: {e}")
        return None

# Funcție pentru a obține stocurile în creștere sau scădere
def get_top_stocks():
    try:
        url = f"{TRENDING_API_URL}?exchange=US&token={API_KEY}"
        with urllib.request.urlopen(url) as response:
            data = response.read()
            parsed_data = json.loads(data)
            return parsed_data[:10]  # Primele 10 stocuri
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la obținerea topului stocurilor: {e}")
        return []

# Funcție pentru verificarea și afișarea detaliilor stocului
def display_stock_details():
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

        current_price = stock_details.get("current", "N/A")
        change = stock_details.get("change", "N/A")
        percent = stock_details.get("percent", "N/A")

        tk.Label(details_window, text=f"Simbol: {stock_symbol}").pack(pady=5)
        tk.Label(details_window, text=f"Preț curent: {current_price}").pack(pady=5)
        tk.Label(details_window, text=f"Schimbare: {change} ({percent}%)").pack(pady=5)

        def open_alert_window():
            alert_window = tk.Toplevel(details_window)
            alert_window.title("Setare Alerte")

            tk.Label(alert_window, text="Valoare țintă:").grid(row=0, column=0, pady=5, padx=5)
            target_price_entry = tk.Entry(alert_window, width=30)
            target_price_entry.grid(row=0, column=1, pady=5, padx=5)

            tk.Label(alert_window, text="Adresa email:").grid(row=1, column=0, pady=5, padx=5)
            email_entry = tk.Entry(alert_window, width=30)
            email_entry.grid(row=1, column=1, pady=5, padx=5)

            def set_alert():
                target_price = target_price_entry.get().strip()
                user_email = email_entry.get().strip()

                if not target_price or not user_email:
                    messagebox.showwarning("Avertisment", "Toate câmpurile sunt obligatorii.")
                    return

                try:
                    target_price = float(target_price)
                    if stock_details["current"] >= target_price:
                        send_email_notification(user_email, stock_symbol, stock_details["current"])
                    else:
                        messagebox.showinfo("Info", "Alerte setată cu succes!")
                except ValueError:
                    messagebox.showerror("Eroare", "Valoarea țintă trebuie să fie un număr valid.")

            tk.Button(alert_window, text="Setează alertă", command=set_alert).grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(details_window, text="Setează alertă", command=open_alert_window).pack(pady=10)

# Funcție pentru a afișa top 10 stocuri
def show_top_stocks():
    top_stocks = get_top_stocks()
    if top_stocks:
        top_window = tk.Toplevel(root)
        top_window.title("Top 10 Stocuri")

        tree = ttk.Treeview(top_window, columns=("Symbol", "Description", "Current", "Change", "Percent"), show="headings")
        tree.heading("Symbol", text="Simbol")
        tree.heading("Description", text="Descriere")
        tree.heading("Current", text="Preț Curent")
        tree.heading("Change", text="Schimbare")
        tree.heading("Percent", text="Procent")

        for stock in top_stocks:
            stock_price = get_stock_price(stock["symbol"])
            tree.insert("", "end", values=(
                stock["symbol"],
                stock["description"],
                stock_price.get("current", "N/A"),
                stock_price.get("change", "N/A"),
                stock_price.get("percent", "N/A")
            ))

        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Interfața grafică
root = tk.Tk()
root.title("Monitorizare Stocuri")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

stock_name_label = tk.Label(frame, text="Nume stoc:")
stock_name_label.grid(row=0, column=0, sticky="e")
stock_name_entry = tk.Entry(frame, width=30)
stock_name_entry.grid(row=0, column=1)

display_button = tk.Button(frame, text="Afișează detalii", command=display_stock_details)
display_button.grid(row=1, column=0, columnspan=2, pady=10)

show_top_button = tk.Button(frame, text="Top 10 Stocuri", command=show_top_stocks)
show_top_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
