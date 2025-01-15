import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox
from config import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD

def send_email_notification(email, stock_symbol, current_price, alert_type, target_price):
    try:
        message = MIMEMultipart()
        message["From"] = EMAIL_ADDRESS
        message["To"] = email
        message["Subject"] = f"Alertă stoc: {stock_symbol}"

        if alert_type == "Creștere":
            condition = "a depășit"
        elif alert_type == "Scădere":
            condition = "este mai mic decât"
        else:  # "Atinge valoarea"
            condition = "a atins"

        # Adjust message based on the alert condition
        if alert_type == "Creștere" and current_price > target_price:
            condition = "a depășit"
        elif alert_type == "Scădere" and current_price < target_price:
            condition = "este mai mic decât"
        else:
            condition = "a atins"

        body = f"Stocul {stock_symbol} {condition} valoarea țintă de {target_price}. Preț curent: {current_price}."
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)

        messagebox.showinfo("Succes", "Email trimis cu succes!")
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la trimiterea email-ului: {e}")
