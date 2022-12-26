import smtplib
from email.mime.text import MIMEText
from config import email_login, email_password, text_script


def send_email(client_email, data):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email_login, email_password)
    content = f"{text_script}{data}"
    msg = MIMEText(content, "html")
    msg["Subject"] = "Result from tally.so"
    msg["To"] = client_email
    msg["From"] = "From: Tally.so"
    server.sendmail(msg=msg.as_string(), from_addr=email_login, to_addrs=client_email)
    print(f"[INFO] Email успешно отправлен {client_email}")
