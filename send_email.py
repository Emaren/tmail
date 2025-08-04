import os
import socket
import time
from dotenv import load_dotenv
import yagmail

def print_log(label, value):
    print(f"🔍 {label}: {value}")

# === LOAD ENV ===
load_dotenv()
DRY_RUN = os.getenv("DRY_RUN", "0") == "1"

# === CONFIGURATION ===
ZOHO_USER         = os.getenv("SMTP_USER")
ZOHO_APP_PASSWORD = os.getenv("SMTP_PASS")
ZOHO_SMTP_HOST    = os.getenv("SMTP_HOST", "smtp.zoho.com")
ZOHO_SMTP_PORT    = int(os.getenv("SMTP_PORT", 465))
RECIPIENT         = os.getenv("TO_EMAIL", "tonyblum@me.com")

print_log("SMTP User", ZOHO_USER)
print_log("SMTP Host", ZOHO_SMTP_HOST)
print_log("SMTP Port", ZOHO_SMTP_PORT)
print_log("Recipient", RECIPIENT)
print_log("Dry Run Mode", DRY_RUN)

# === SETUP SMTP CLIENT ===
if not DRY_RUN:
    try:
        print("🔌 Connecting to Zoho SMTP...")
        yag = yagmail.SMTP(
            user=ZOHO_USER,
            password=ZOHO_APP_PASSWORD,
            host=ZOHO_SMTP_HOST,
            port=ZOHO_SMTP_PORT,
            smtp_ssl=True,
            smtp_starttls=False
        )
        print("✅ SMTP connection established.")
    except Exception as e:
        print(f"❌ SMTP connection failed: {e}")
        exit(1)

# === GENERATE TIMESTAMP ===
ts = int(time.time())
print_log("Generated timestamp", ts)

# === BETTER LAN IP RESOLUTION ===
def get_lan_ip():
    try:
        import netifaces
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface).get(netifaces.AF_INET)
            if addrs:
                for addr in addrs:
                    ip = addr['addr']
                    if not ip.startswith("127."):
                        return ip
    except:
        pass
    return socket.gethostbyname(socket.gethostname()) or "172.20.10.5"

lan_ip = get_lan_ip()
print_log("Resolved LAN IP", lan_ip)

# === TRACKING PIXELS ===
localhost_pixel = (
    f'<img src="http://localhost:8008/track?id=tony_localhost&ts={ts}" '
    'width="1" height="1" style="display:none;" />'
)

lan_pixel = (
    f'<img src="http://{lan_ip}:8008/track?id=tony_lan&ts={ts}" '
    'width="1" height="1" style="display:none;" />'
)

tracking_pixels = localhost_pixel + lan_pixel
print_log("Tracking Pixel [localhost]", localhost_pixel)
print_log("Tracking Pixel [LAN]", lan_pixel)

# === EMAIL HTML CONTENT ===
html_content = f"""
<html>
  <body style="margin:0; background:#000; color:#fff; font-family:sans-serif; text-align:center;">
    <a href="https://tokentap.ca" target="_blank">
      <img src="https://tokentap.ca/email-assets/pink-black.png" width="300" style="display:block;margin:0 auto;" />
    </a>
    <h1 style="color:#ff40a1;">Welcome to TokenTap</h1>
    <p style="color:#ccc;">Loyalty Tokens are live.</p>
    {tracking_pixels}
  </body>
</html>
"""

print_log("Email Subject", f"1TokenTap 👋 · {ts}")
print_log("HTML Snippet", html_content.strip()[:300] + "...")

# === SAVE TO FILE FOR DEBUGGING ===
debug_path = f"email_debug_{ts}.html"
with open(debug_path, "w") as f:
    f.write(html_content)
print_log("Saved HTML to file", debug_path)

# === SEND EMAIL ===
if DRY_RUN:
    print("🧪 DRY RUN MODE: Email not sent.")
else:
    try:
        yag.send(
            to=RECIPIENT,
            subject=f"TokenTap 👋 · {ts}",
            contents=html_content
        )
        print("📤 Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
