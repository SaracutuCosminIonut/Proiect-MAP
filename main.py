import tkinter as tk
from ui import display_stock_details, show_top_stocks

def main():
    root = tk.Tk()
    root.title("Monitorizare Stocuri")
    root.configure(bg="#2e2e2e")

    frame = tk.Frame(root, padx=10, pady=10, bg="#2e2e2e")
    frame.pack(padx=10, pady=10)

    stock_name_label = tk.Label(frame, text="Nume stoc:", font=("Helvetica", 12), bg="#2e2e2e", fg="white")
    stock_name_label.grid(row=0, column=0, sticky="e")
    stock_name_entry = tk.Entry(frame, width=30, font=("Helvetica", 12), bg="#3e3e3e", fg="white", insertbackground="white")
    stock_name_entry.grid(row=0, column=1)

    display_button = tk.Button(frame, text="Afișează detalii", command=lambda: display_stock_details(root, stock_name_entry), bg="#007acc", fg="white", font=("Helvetica", 12), relief="flat", activebackground="#005999")
    display_button.grid(row=1, column=0, columnspan=2, pady=10)

    show_top_button = tk.Button(frame, text="Top 10 Stocuri", command=lambda: show_top_stocks(root), bg="#007acc", fg="white", font=("Helvetica", 12), relief="flat", activebackground="#005999")
    show_top_button.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()