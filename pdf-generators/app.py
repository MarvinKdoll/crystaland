"""
Crystaland PDF Generator API
Receives Kajabi purchase webhooks, fetches buyer's numerology data from ActiveCampaign,
generates a personalized PDF, and emails it to the customer.

Environment variables required (set in Render dashboard):
  AC_API_URL    - e.g. https://crystaland.api-us1.com
  AC_API_KEY    - ActiveCampaign API key
  SMTP_HOST     - e.g. smtp.gmail.com
  SMTP_PORT     - e.g. 587
  SMTP_USER     - sending email address
  SMTP_PASS     - app password (Gmail) or SMTP password
  SENDER_NAME   - e.g. Crystaland
  WEBHOOK_SECRET - optional shared secret to verify Kajabi webhooks
"""

import os
import json
import smtplib
import logging
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from flask import Flask, request, jsonify

# Import PDF generators
from pdf_email_brief import generate_free_report
from pdf_generator_33page import generate_33page_report
from pdf_77page_premium import generate_77page_report

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("crystaland")

app = Flask(__name__)

# ── Config ───────────────────────────────────────────────────────
AC_API_URL    = os.environ.get("AC_API_URL", "https://crystaland.api-us1.com")
AC_API_KEY    = os.environ.get("AC_API_KEY", "")
SMTP_HOST     = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT     = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER     = os.environ.get("SMTP_USER", "")
SMTP_PASS     = os.environ.get("SMTP_PASS", "")
SENDER_NAME   = os.environ.get("SENDER_NAME", "Crystaland")
WEBHOOK_SECRET= os.environ.get("WEBHOOK_SECRET", "")


# ── ActiveCampaign Helpers ────────────────────────────────────────
def ac_headers():
    return {"Api-Token": AC_API_KEY, "Content-Type": "application/json"}


def get_contact_by_email(email: str) -> dict | None:
    """Look up an AC contact by email and return their field data."""
    url = f"{AC_API_URL}/api/3/contacts"
    params = {"email": email}
    try:
        resp = requests.get(url, headers=ac_headers(), params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        contacts = data.get("contacts", [])
        if not contacts:
            log.warning(f"No AC contact found for {email}")
            return None
        contact = contacts[0]
        contact_id = contact["id"]
        # Fetch field values
        fv_url = f"{AC_API_URL}/api/3/contacts/{contact_id}/fieldValues"
        fv_resp = requests.get(fv_url, headers=ac_headers(), timeout=10)
        fv_resp.raise_for_status()
        field_values = fv_resp.json().get("fieldValues", [])
        fields = {}
        for fv in field_values:
            fields[str(fv["field"])] = fv["value"]
        return {
            "name": f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip(),
            "email": email,
            "fields": fields,  # keyed by AC field ID string
        }
    except Exception as e:
        log.error(f"AC lookup failed for {email}: {e}")
        return None


def build_report_data(email: str, name: str = "") -> dict:
    """
    Build the data dict needed by the PDF generators.
    AC field IDs (from your form embed):
      8  = lp (Life Path)
      10 = exp (Expression)
      11 = su (Soul Urge)
      12 = per (Personality)
      13 = py (Personal Year)
      14 = hd_type
      15 = hd_profile
      16 = hd_authority
    """
    contact = get_contact_by_email(email)
    if not contact:
        # Fall back to minimal data so PDF still generates
        return {"name": name or email.split("@")[0].title(), "email": email,
                "lp": 1, "exp": 1, "su": 1, "per": 1, "py": 1,
                "hd_type": "generator", "hd_profile": "3/5", "hd_authority": "sacral"}
    f = contact["fields"]

    def safe_int(field_id, default=1):
        try:
            v = int(f.get(str(field_id), default) or default)
            return v if v >= 1 else default
        except (ValueError, TypeError):
            return default

    return {
        "name":         contact.get("name") or name or email.split("@")[0].title(),
        "email":        email,
        "lp":           safe_int(8),
        "exp":          safe_int(10),
        "su":           safe_int(11),
        "per":          safe_int(12),
        "py":           safe_int(13),
        "hd_type":      f.get("14", "generator") or "generator",
        "hd_profile":   f.get("15", "3/5") or "3/5",
        "hd_authority": f.get("16", "sacral") or "sacral",
    }


# ── Email Helper ──────────────────────────────────────────────────
def send_pdf_email(to_email: str, to_name: str, pdf_bytes: bytes,
                   filename: str, subject: str, body_html: str):
    """Send the PDF as an email attachment."""
    msg = MIMEMultipart("mixed")
    msg["From"]    = f"{SENDER_NAME} <{SMTP_USER}>"
    msg["To"]      = to_email
    msg["Subject"] = subject

    # HTML body
    msg.attach(MIMEText(body_html, "html"))

    # PDF attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(pdf_bytes)
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
    msg.attach(part)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
    log.info(f"PDF email sent to {to_email} ({filename})")


def email_body(name: str, tier: str) -> str:
    first = name.split()[0] if name else "friend"
    bodies = {
        "free": f"""
<div style="background:#08080f;color:#e8e0d0;font-family:Georgia,serif;padding:40px;max-width:600px;margin:auto;">
  <p style="color:#c9a96e;font-size:13px;letter-spacing:2px;">CRYSTALAND</p>
  <h1 style="color:#f5f0e8;">Your Numerology Blueprint is here, {first}.</h1>
  <p>Your personalized report is attached to this email. Open it when you have a quiet moment — it was built for you.</p>
  <p style="color:#c9a96e;">Read slowly. Let what resonates land.</p>
  <p style="margin-top:32px;">With love,<br><strong style="color:#c9a96e;">Rita & the Crystaland team</strong></p>
  <p style="font-size:11px;color:#7a7068;margin-top:40px;">crystaland.online</p>
</div>""",
        "33": f"""
<div style="background:#08080f;color:#e8e0d0;font-family:Georgia,serif;padding:40px;max-width:600px;margin:auto;">
  <p style="color:#c9a96e;font-size:13px;letter-spacing:2px;">CRYSTALAND</p>
  <h1 style="color:#f5f0e8;">Your Complete Blueprint has arrived, {first}.</h1>
  <p>Your 33-page numerology report is attached. This is your full chart — the deep dive into every number, every cycle, every layer of who you came here to be.</p>
  <p>Set aside real time with it. It will meet you exactly where you are.</p>
  <p style="color:#c9a96e;">Your path. Your numbers. Your identity.</p>
  <p style="margin-top:32px;">With love,<br><strong style="color:#c9a96e;">Rita & the Crystaland team</strong></p>
  <p style="font-size:11px;color:#7a7068;margin-top:40px;">crystaland.online</p>
</div>""",
        "77": f"""
<div style="background:#08080f;color:#e8e0d0;font-family:Georgia,serif;padding:40px;max-width:600px;margin:auto;">
  <p style="color:#c9a96e;font-size:13px;letter-spacing:2px;">CRYSTALAND</p>
  <h1 style="color:#f5f0e8;">The Full Transmission is yours, {first}.</h1>
  <p>Your 77-page report — numerology, Human Design, month-by-month forecast, and the full transmission of your soul's blueprint — is attached.</p>
  <p>This is the most comprehensive map of your design we offer. Return to it often. It will mean different things at different moments in your life.</p>
  <p style="color:#c9a96e;">You were never lost. You were always this.</p>
  <p style="margin-top:32px;">With love and deep respect for your path,<br><strong style="color:#c9a96e;">Rita & the Crystaland team</strong></p>
  <p style="font-size:11px;color:#7a7068;margin-top:40px;">crystaland.online</p>
</div>""",
    }
    return bodies.get(tier, bodies["free"])


# ── Webhook Routes ────────────────────────────────────────────────
def extract_customer(payload: dict) -> tuple[str, str]:
    """Extract email and name from Kajabi webhook payload."""
    # Kajabi sends purchase webhooks with 'customer' or 'member' object
    customer = payload.get("customer") or payload.get("member") or {}
    email = (customer.get("email") or payload.get("email") or "").strip().lower()
    first = customer.get("first_name") or payload.get("first_name") or ""
    last  = customer.get("last_name")  or payload.get("last_name")  or ""
    name  = f"{first} {last}".strip() or customer.get("name") or payload.get("name") or ""
    return email, name


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "crystaland-pdf-api"})


@app.route("/webhook/33page", methods=["POST"])
def webhook_33page():
    """Kajabi purchase webhook for 33-page $47 report."""
    try:
        payload = request.get_json(force=True) or {}
        email, name = extract_customer(payload)
        if not email:
            return jsonify({"error": "No email in payload"}), 400
        log.info(f"33-page webhook received for {email}")
        data = build_report_data(email, name)
        pdf_bytes = generate_33page_report(data)
        fname = "crystaland-complete-blueprint.pdf"
        subj  = f"Your Complete Numerology Blueprint is here, {data['name'].split()[0]}"
        send_pdf_email(email, data["name"], pdf_bytes, fname, subj, email_body(data["name"], "33"))
        return jsonify({"status": "sent", "email": email}), 200
    except Exception as e:
        log.error(f"33-page webhook error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/webhook/77page", methods=["POST"])
def webhook_77page():
    """Kajabi purchase webhook for 77-page $97 report."""
    try:
        payload = request.get_json(force=True) or {}
        email, name = extract_customer(payload)
        if not email:
            return jsonify({"error": "No email in payload"}), 400
        log.info(f"77-page webhook received for {email}")
        data = build_report_data(email, name)
        pdf_bytes = generate_77page_report(data)
        fname = "crystaland-full-transmission.pdf"
        subj  = f"The Full Transmission is yours, {data['name'].split()[0]}"
        send_pdf_email(email, data["name"], pdf_bytes, fname, subj, email_body(data["name"], "77"))
        return jsonify({"status": "sent", "email": email}), 200
    except Exception as e:
        log.error(f"77-page webhook error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/webhook/free", methods=["POST"])
def webhook_free():
    """Optional: trigger free report delivery via webhook."""
    try:
        payload = request.get_json(force=True) or {}
        email, name = extract_customer(payload)
        if not email:
            return jsonify({"error": "No email in payload"}), 400
        data = build_report_data(email, name)
        pdf_bytes = generate_free_report(data)
        fname = "crystaland-numerology-blueprint.pdf"
        subj  = f"Your Numerology Blueprint is here, {data['name'].split()[0]}"
        send_pdf_email(email, data["name"], pdf_bytes, fname, subj, email_body(data["name"], "free"))
        return jsonify({"status": "sent", "email": email}), 200
    except Exception as e:
        log.error(f"Free webhook error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/test/generate", methods=["POST"])
def test_generate():
    """
    Test endpoint — generate a PDF without sending email.
    POST { "tier": "free"|"33"|"77", "email": "...", "name": "..." }
    """
    body = request.get_json(force=True) or {}
    tier  = body.get("tier", "free")
    email = body.get("email", "test@crystaland.online")
    name  = body.get("name", "Test User")
    data  = build_report_data(email, name)
    if tier == "77":
        pdf_bytes = generate_77page_report(data)
        fname = "test-full-transmission.pdf"
    elif tier == "33":
        pdf_bytes = generate_33page_report(data)
        fname = "test-complete-blueprint.pdf"
    else:
        pdf_bytes = generate_free_report(data)
        fname = "test-free-report.pdf"
    from flask import Response
    return Response(pdf_bytes, mimetype="application/pdf",
                    headers={"Content-Disposition": f"attachment; filename={fname}"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
