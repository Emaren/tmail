import os, time, smtplib, webbrowser
from pathlib import Path
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

# ---------- CONFIG ----------
def load_config():
    load_dotenv()
    return {
        "DRY_RUN": os.getenv("DRY_RUN", "0") == "1",
        "SMTP_USER": os.getenv("SMTP_USER"),
        "SMTP_PASS": os.getenv("SMTP_PASS"),
        "SMTP_HOST": os.getenv("SMTP_HOST", "smtp.zoho.com"),
        "SMTP_PORT": int(os.getenv("SMTP_PORT", 587)),
        "TO_EMAIL": os.getenv("TO_EMAIL"),
        "TRACK_HOST": os.getenv("TRACK_HOST", "track.tokentap.ca"),
        "AUTO_OPEN_HTML": os.getenv("OPEN_HTML", "0") == "1",
    }

# ---------- TRACKING PIXELS ----------
def build_tracking_pixels(track_host, ts):
    base = f"https://{track_host}/track"
    p1   = f"{base}?id=tony_public&ts={ts}"
    p2   = f"{base}?id=tony_local&ts={ts}"
    click= f"{base}?id=hidden_click&ts={ts}"
    return f"""
      <img src="{p1}" width="1" height="1" style="display:block;width:1px;height:1px" alt="">
      <img src="{p2}" width="1" height="1" style="display:block;width:1px;height:1px" alt="">
      <div style="display:none;background-image:url('{p1}');width:1px;height:1px"></div>
      <a href="{click}" style="display:inline-block;width:1px;height:1px;overflow:hidden">
        <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
             width="1" height="1" alt="">
      </a>"""

# ---------- TEMPLATE ----------
def build_email_html(tracking_pixels):
    with open("email_template.html", encoding="utf-8") as f:
        return f.read().replace("{{tracking_pixels}}", tracking_pixels)

# ---------- MESSAGE BUILDER ----------
def build_message(cfg, html, ts):
    msg = MIMEMultipart("alternative")
    from email.utils import formataddr

    msg["From"] = formataddr(("Tony with TokenTap", cfg["SMTP_USER"]))
    msg["To"]   = cfg["TO_EMAIL"]
    msg["Subject"] = f"Your Brand’s Token Is Ready 🪙 $BOO"

    # Add unsubscribe headers for compliant mail clients
    msg.add_header(
        'List-Unsubscribe',
        '<mailto:unsubscribe@tokentap.ca?subject=unsubscribe>'
    )
    msg.add_header(
        'List-Unsubscribe-Post',
        'List-Unsubscribe=One-Click'
    )

    # Plain-text preview
    txt = MIMEText("View this email in an HTML‑capable mail client.", "plain", "utf-8")
    msg.attach(txt)

    # HTML part
    html_part = MIMEText(html, "html", "utf-8")
    encoders.encode_base64(html_part)
    msg.attach(html_part)

    return msg

# ---------- SENDER ----------
def send_email(cfg, html, ts):
    msg = build_message(cfg, html, ts)
    with smtplib.SMTP(cfg["SMTP_HOST"], cfg["SMTP_PORT"], timeout=10) as s:
        s.starttls()
        s.login(cfg["SMTP_USER"], cfg["SMTP_PASS"])
        print(f"📨 Sending email to: {msg['To']}")
        s.send_message(msg)
    print("📤 Email sent successfully.")

# ---------- MAIN ----------
def main():
    cfg = load_config()
    ts = int(time.time())

    html = build_email_html(build_tracking_pixels(cfg["TRACK_HOST"], ts))
    Path("emails").mkdir(exist_ok=True)
    Path(f"emails/email_debug_{ts}.html").write_text(html, encoding="utf‑8")

    if cfg["AUTO_OPEN_HTML"]:
        webbrowser.open(f"file://{Path.cwd()}/emails/email_debug_{ts}.html")

    if cfg["DRY_RUN"]:
        print("🧪 DRY‑RUN: email not sent.")
    else:
        send_email(cfg, html, ts)

if __name__ == "__main__":
    main()
