import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# === CONFIGURATION ===
ZOHO_USER = "contact@tokentap.ca"
ZOHO_APP_PASSWORD = "VtaTYZPxhyAd"
ZOHO_SMTP_HOST = "smtp.zoho.com"
ZOHO_SMTP_PORT = 587  # STARTTLS

RECIPIENT = "tonyblum@me.com"

# === TRACKING PIXEL ===
tracking_pixel = '<img src="http://157.180.114.124:8008/track?id=tony001" width="1" height="1" style="display:none;" />'

# === EMAIL HTML CONTENT ===
html_content = f"""
<html>
  <body style="margin:0; background:#000; color:#fff; font-family:sans-serif; text-align:center;">
    <a href="https://tokentap.ca" target="_blank">
      <img src="https://tokentap.ca/email-assets/pink-black.png" width="300" style="display:block;margin:0 auto;" />
    </a>
    <h1 style="color:#ff40a1;">Welcome to TokenTap</h1>
    <p style="color:#ccc;">Loyalty Tokens are live.</p>
    {tracking_pixel}
  </body>
</html>
"""

# === COMPOSE MESSAGE ===
msg = MIMEMultipart("alternative")
msg["Subject"] = "Welcome to TokenTap 👋"
msg["From"] = ZOHO_USER
msg["To"] = RECIPIENT
msg.attach(MIMEText(html_content, "html"))

# === SEND ===
try:
    print("🔌 Connecting with STARTTLS...")
    with smtplib.SMTP(ZOHO_SMTP_HOST, ZOHO_SMTP_PORT) as server:
        server.starttls()
        server.login(ZOHO_USER, ZOHO_APP_PASSWORD)
        server.sendmail(ZOHO_USER, RECIPIENT, msg.as_string())
    print("📤 Email sent successfully.")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
