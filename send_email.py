import os
import time
import smtplib
import webbrowser
from pathlib import Path
from dotenv import load_dotenv
import yagmail

# === CONFIGURATION ===
def print_log(label, value):
    print(f"🔍 {label}: {value}")

def load_config():
    load_dotenv()
    return {
        "DRY_RUN": os.getenv("DRY_RUN", "0") == "1",
        "SMTP_USER": os.getenv("SMTP_USER"),
        "SMTP_PASS": os.getenv("SMTP_PASS"),
        "SMTP_HOST": os.getenv("SMTP_HOST", "smtp.zoho.com"),
        "SMTP_PORT": int(os.getenv("SMTP_PORT", 587)),
        "TO_EMAIL": os.getenv("TO_EMAIL", "tonyblum@me.com"),
        "TRACK_HOST": os.getenv("TRACK_HOST", "track.tokentap.ca"),
        "AUTO_OPEN_HTML": os.getenv("OPEN_HTML", "0") == "1",
    }

def build_tracking_pixels(track_host, ts):
    base_url = f"https://{track_host}/track"
    pixel_public = f"{base_url}?id=tony_public&ts={ts}"
    pixel_local  = f"{base_url}?id=tony_localhost&ts={ts}"
    click_track  = f"{base_url}?id=hidden_click&ts={ts}"

    return f"""
    <!-- Primary tracking pixels -->
    <img src="{pixel_public}" width="1" height="1" style="display:block!important;width:1px!important;height:1px!important;border:none!important;outline:none!important;" alt="" />
    <img src="{pixel_local}" width="1" height="1" style="display:block!important;width:1px!important;height:1px!important;border:none!important;outline:none!important;" alt="" />

    <!-- Fallback CSS pixel -->
    <div style="display:none!important; background-image: url('{pixel_public}'); width:1px; height:1px;"></div>

    <!-- Hidden click tracker -->
    <a href="{click_track}" style="display:inline-block;width:1px;height:1px;overflow:hidden;">
      <img src="https://tokentap.ca/email-assets/invisible-dot.png" width="1" height="1" alt="" style="display:block;" />
    </a>
    """

def build_email_html(tracking_pixels: str) -> str:
    with open("email_template.html", "r") as f:
        template = f.read()
    return template.replace("{{tracking_pixels}}", tracking_pixels)

def save_html_file(content: str, ts: int) -> str:
    emails_dir = Path("emails")
    emails_dir.mkdir(exist_ok=True)
    file_path = emails_dir / f"email_debug_{ts}.html"
    file_path.write_text(content)
    return str(file_path)

def send_email(config, html_content, ts):
    try:
        print("📨 Sending email now...")
        yag = yagmail.SMTP(
            user=config["SMTP_USER"],
            password=config["SMTP_PASS"],
            host=config["SMTP_HOST"],
            port=config["SMTP_PORT"],
            smtp_ssl=False,
            smtp_starttls=True,
            timeout=10
        )
        yag.send(
            to=config["TO_EMAIL"],
            subject=f"19💌 TokenTap 👋 · {ts}",
            contents=html_content
        )
        print("📤 Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def main():
    config = load_config()
    for k, v in config.items():
        print_log(k, v)

    ts = int(time.time())
    print_log("Generated timestamp", ts)

    tracking_pixels = build_tracking_pixels(config["TRACK_HOST"], ts)
    html_content = build_email_html(tracking_pixels)

    print_log("Email Subject", f"💌 TokenTap 👋 · {ts}")
    print_log("HTML Snippet", html_content.strip()[:300] + "...")

    html_path = save_html_file(html_content, ts)
    print_log("Saved HTML to file", html_path)

    if config["AUTO_OPEN_HTML"]:
        webbrowser.open(f"file://{html_path}")

    if config["DRY_RUN"]:
        print("🧪 DRY RUN MODE: Email not sent.")
    else:
        send_email(config, html_content, ts)

if __name__ == "__main__":
    os.environ["YAGMAIL_DISABLE_KEYRING"] = "true"
    smtplib.socket.setdefaulttimeout(10)
    main()
