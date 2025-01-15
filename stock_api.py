import urllib.request
import json
from tkinter import messagebox
from config import STOCK_API_URL, SEARCH_API_URL, SYMBOL_API_URL, API_KEY

def get_stock_price(stock_symbol):
    try:
        url = f"{STOCK_API_URL}?symbol={stock_symbol}&token={API_KEY}"
        with urllib.request.urlopen(url) as response:
            data = response.read().decode("utf-8")
            parsed_data = json.loads(data)
            return {
                "current": parsed_data.get("c", "N/A"),
                "change": parsed_data.get("d", "N/A"),
                "percent": parsed_data.get("dp", "N/A")
            }
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la obținerea prețului stocului: {e}")
        return None

def search_stock_symbol(stock_name):
    try:
        url = f"{SEARCH_API_URL}?q={stock_name}&token={API_KEY}"
        with urllib.request.urlopen(url) as response:
            data = response.read().decode("utf-8")
            parsed_data = json.loads(data)
            if parsed_data.get("count", 0) > 0:
                return parsed_data["result"][0]["symbol"]
            else:
                messagebox.showinfo("Info", "Nu s-a găsit niciun simbol pentru acest nume de stoc.")
                return None
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la căutarea simbolului stocului: {e}")
        return None

# stock_api.py

def get_top_stocks():
    try:
        url = f"{SYMBOL_API_URL}?exchange=US&token={API_KEY}"
        with urllib.request.urlopen(url) as response:
            data = response.read().decode("utf-8")
            parsed_data = json.loads(data)[:10]
            
            top_stocks = []
            for stock in parsed_data:
                symbol = stock["symbol"]
                stock_details = get_stock_price(symbol)
                if stock_details:
                    stock.update({
                        "current": stock_details["current"],
                        "change": stock_details["change"]
                    })
                top_stocks.append(stock)
                
            return top_stocks
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la obținerea topului stocurilor: {e}")
        return []
