import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Gmail credentials
sender_email = "l7205716@gmail.com"
sender_password = "fpas cfgd htco ccnd"
def send_mail(to,name):
# Recipient email address
            recipient_email = "tabonunez.tn@gmail.com"

            # Create the MIME object
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = to
            message["Subject"] = "Tickets confirmation"

            # Attach the message body
            body = "Felicidades %s aqui estan tus entradas"%name
            message.attach(MIMEText(body, "plain"))

            # Connect to the SMTP server
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                # Log in to your Gmail account
                server.login(sender_email, sender_password)

                # Send the email
                server.sendmail(sender_email, to, message.as_string())

            print("Email sent successfully!")

