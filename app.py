from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()  # load variables from .env if present

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-me")

# Set log level from env (default INFO)
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
try:
    app.logger.setLevel(getattr(logging, log_level, logging.INFO))
except Exception:
    app.logger.setLevel(logging.INFO)

def _log_smtp_status_once():
    host = os.getenv("SMTP_HOST")
    user = os.getenv("SMTP_USER")
    pwd = os.getenv("SMTP_PASS")
    missing = [k for k,v in {"SMTP_HOST":host, "SMTP_USER":user, "SMTP_PASS":pwd}.items() if not v]
    app.logger.info("SMTP config detected => host=%s user=%s pass_set=%s missing=%s",
                    bool(host), bool(user), bool(pwd), missing)

# log saat app import (berguna untuk lokal dev)
_log_smtp_status_once()

# --- Sample data (silakan ganti dengan data Anda) ---
PROFILE = {
    "name": "Andi Muhammad Ichsan Jalaluddin",
    "role": "Cloud Engineer | DevOps Engineer",
    "summary": "I am a Cloud & DevOps Engineer with strong expertise in Google Cloud Platform (GCP) and Microsoft Azure, specializing in designing, deploying, and optimizing scalable, secure, and high-performance cloud infrastructures. My work involves integrating cloud-native services with modern DevOps practices to enhance automation, reliability, and delivery efficiency across environments. I am passionate about implementing CI/CD pipelines, infrastructure as code (IaC), cloud networking, cost optimization, and platform observability to ensure seamless operations and continuous improvement. For me, cloud and DevOps are more than just tools—they are enablers for innovation, operational excellence, and delivering real value to businesses and end-users.",
    "avatar": "static/images/photo.png",  # gunakan salah satu gambar yang sudah ada
    "location": "Jakarta, Indonesia",
    "email": "andiichsan123@gmail.com",
    "whatsapp": "6281231620512",
    "links": [
        {"label": "GitHub", "url": "https://github.com/ndchsn"},
        {"label": "LinkedIn", "url": "https://www.linkedin.com/in/andi-ichsan"},
        {"label": "Resume / CV", "url": "/static/Andi Muhammad Ichsan.pdf"},
    ],
}

EXPERIENCES = [
    {
        "company": "PT Multipolar Technology",
        "role": "Cloud Engineer",
        "period": "Juli 2024 — Now",
        "summary": "As a Cloud Engineer, I am responsible for designing, implementing, and maintaining cloud infrastructure for customers.",
        "highlights": [
            "Supporting customers in assessing their on-premises VMware server migration to GCP, Deploying GCP server projects for customers using automation Terraform Infrastructure as Code.",
            "Helping customers deploy server monitoring services via the Datadog marketplace.",
            "Supporting the projects High-Level Infrastructure Design on GCP.",
            "Assisting customers with surrounding necessary marketplace around GCP.",
            "Collaborating with presales on new infrastructure provision for customers and create BoQ.",
            "Creating QP documents such as Work Plans, LLD, UAT, Technical Documents, Work Reports, and more as activity records for customer projects.",
            "Perform use case project using CI/CD pipeline that integrate with Serverless, AI, PaaS, IaaS.",
            "Using Git to perform CI/CD with Cloud Build / Github Actions.",
            "Build a microservices app using Google Kubernetes Engine.",
            "Drafting Method of Procedure (MoP) documents as action plans for GCP projects.",
            "Providing customers with monthly billing reports under opex-based payment models.",
            "Assisting and advising customers on exporting billing usage data to BigQuery and further visualizing it with Looker Data Studio."
        ],
        "stack": ["Google Cloud Platform", "Microsoft Azure", "Infrastructure as Code", "IaaS", "PaaS", "SaaS", "Presales", "CI/CD", "Serverless", "Artificial Intelligence", "Containerization", "Docker"]
            },
    {
        "company": "Bangkit Academy led by Google, Tokopedia, Gojek, & Traveloka",
        "role": "Cloud Computing Cohort",
        "period": "January 2023 — January 2024",
        "summary": "Bangkit is a Google-led academy designed to produce high-caliber technical talent for world-class Indonesian technology companies and startups. Some of the activities are:",
        "highlights": [
            "Designing and implementing an infrastructure for a real-time mobile application using GCP.",
            "Designing ER-Diagram MySQL Databases and using Compute Engine as a databases.",
            "Deploy a backend API python (Flask) using Cloud Function.",
            "Collab with Machine Learning and Android Developer teams to ensure the mobile application runs effectively, scalability, and high availability. "
        ],
        "stack": ["Google Cloud Platform", "IaaS", "PaaS", "MySQL", "Python", "Flask", "Serverless"]
    }
]

EXPERTISE = [
    {"name": "Cloud Architecture", "desc": "Design architecture scalable, secure, and cost-efficient.", "icons": ["☁️", "🏗️"]},
    {"name": "CI/CD & Automation", "desc": "GitHub Action, Cloud Build, Azure DevOps.", "icons": ["🤖", "🚀"]},
    {"name": "Containers & Orchestration", "desc": "Docker, Kubernetes, Helm, GitOps.", "icons": ["🐳", "🧭"]},
    {"name": "Observability", "desc": "Metrics, logs, tracing, SLO, error budgets, Grafana, Prometheus.", "icons": ["📈", "🧩"]},
    {"name": "IaC & Platform", "desc": "Terraform, Ansible, modul reusable dan platform self-service.", "icons": ["🧱", "🔧"]},
    {"name": "Security", "desc": "Shift-left security, secrets management, image scanning.", "icons": ["🔐", "🛡️"]},
]

CERTIFICATIONS = [
    {"name": "GCP - Professional Cloud Architect", "issuer": "Google Cloud Platform", "year": "July 2024", "url": "https://www.credly.com/badges/bf6a5dd5-4adc-4e09-a4cc-d910174d0f96/public_url"},
    {"name": "GCP - Professional Cloud Network Engineer", "issuer": "Google Cloud Platform", "year": "March 2025", "url": "https://www.credly.com/badges/5e8bd2d1-a42a-426f-9152-fb466667b21e/public_url"},
    {"name": "GCP - Professional Cloud Security Engineer", "issuer": "Google Cloud Platform", "year": "April 2025", "url": "https://www.credly.com/badges/5f6cb191-a002-4ee7-8d64-258c439e6d75/public_url"},
    {"name": "GCP - Professional Cloud Developer", "issuer": "Google Cloud Platform", "year": "October 2025", "url": "https://www.credly.com/badges/05f0782e-7480-4720-a352-d218d9d76b27/public_url"},
    {"name": "GCP - Professional Cloud DevOps Engineer", "issuer": "Google Cloud Platform", "year": "October 2025"},
    {"name": "Azure - az-500 Security Engineer", "issuer": "Microsoft Azure", "year": "October 2025", "url": "https://learn.microsoft.com/api/credentials/share/en-us/AndiMuhammadIchsanJalaluddin-8142/7913E4E2C09ECBA1?sharingId=ED44CD5BBFD9E3C7"},
        
]

EDUCATION = [
    {
        "school": "Amikom Yogyakarta University",
        "degree": "S.Kom - Teknik Komputer | GPA 3.94",
        "period": "2020 - 2024",   
        "details": "Focusing on Cyber Security, Cloud Computing, and Computer Network."
    }
]


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        profile=PROFILE,
        experiences=EXPERIENCES,
        expertise=EXPERTISE,
        certifications=CERTIFICATIONS,
        education=EDUCATION,
        year=datetime.now().year
    )


@app.route("/contact", methods=["POST"])
def contact():
    import smtplib
    from email.mime.text import MIMEText

    name = request.form.get("name", "").strip()
    sender_email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    # Log incoming contact request
    app.logger.info("[CONTACT_REQUEST] name=%s email=%s len=%s", name or "-", sender_email or "-", len(message))

    if not message:
        flash("Pesan tidak boleh kosong.", "danger")
        return redirect(url_for("index") + "#contact")

    target = "andiichsan123@gmail.com"
    subject = f"[Portfolio] Pesan baru dari {name or 'Anonim'}"
    body = f"""Nama: {name or '-'}
Email: {sender_email or '-'}

Pesan:
{message}
"""

    # 1) Prefer SendGrid API if available (reliable on free hosts), else fallback to SMTP
    sent = False
    method_used = None
    sg_key = os.getenv("SENDGRID_API_KEY")
    sg_from = os.getenv("SENDGRID_FROM") or os.getenv("SMTP_USER") or target
    if sg_key:
        try:
            import requests
            payload = {
                "personalizations": [{"to": [{"email": target}]}],
                "from": {"email": sg_from},
                "subject": subject,
                "content": [{"type": "text/plain", "value": body}]
            }
            if sender_email:
                payload["reply_to"] = {"email": sender_email}
            headers = {
                "Authorization": f"Bearer {sg_key}",
                "Content-Type": "application/json"
            }
            r = requests.post("https://api.sendgrid.com/v3/mail/send", json=payload, headers=headers, timeout=20)
            if r.status_code in (200, 202):
                flash("Pesan terkirim. Terima kasih!", "success")
                sent = True
                method_used = "sendgrid"
            else:
                app.logger.error("SendGrid failed status=%s body=%s", r.status_code, r.text)
        except Exception as e:
            app.logger.exception("SendGrid exception: %s", e)

    # 2) SMTP config via env (fallback)
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    pwd = os.getenv("SMTP_PASS")
    use_smtp = bool(host and user and pwd)
    missing = [k for k,v in {"SMTP_HOST":host, "SMTP_USER":user, "SMTP_PASS":pwd}.items() if not v]

    if not sent and use_smtp:
        try:
            msg = MIMEText(body, "plain", "utf-8")
            msg["Subject"] = subject
            msg["From"] = user
            msg["To"] = target
            if sender_email:
                msg["Reply-To"] = sender_email

            # Try TLS:587, fallback SSL:465
            try:
                with smtplib.SMTP(host, port, timeout=20) as server:
                    server.starttls()
                    server.login(user, pwd)
                    server.send_message(msg)
            except OSError:
                import smtplib as _s
                with _s.SMTP_SSL(host, 465, timeout=20) as server:
                    server.login(user, pwd)
                    server.send_message(msg)

            flash("Pesan terkirim. Terima kasih!", "success")
            sent = True
            method_used = "smtp"
        except Exception as e:
            app.logger.exception("Gagal mengirim email (SMTP): %s", e)
            app.logger.info("[CONTACT_FALLBACK] to=%s subject=%s body=%s", target, subject, body)

    if sent:
        app.logger.info("[CONTACT_SENT] method=%s name=%s email=%s len=%s", method_used, name or "-", sender_email or "-", len(message))
    if not sent:
        # Fallback: log bila semua metode gagal/tdk dikonfigurasi
        app.logger.info("[CONTACT_LOG_ONLY] to=%s subject=%s body=%s", target, subject, body)
        detail = f" (missing: {', '.join(missing)})" if missing else ""
        flash(f"SMTP/API belum ready{detail}. Pesan dicatat di log.", "warning")

    return redirect(url_for("index") + "#contact")


if __name__ == "__main__":
    # Jalankan server
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)