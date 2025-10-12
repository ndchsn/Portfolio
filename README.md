<<<<<<< HEAD
# cicdportfolio
=======

# Portfolio (Flask) — Cloud / DevOps themed

Simple personal portfolio built with Flask and styled to have a cloud / DevOps vibe.

Getting started (Windows PowerShell):

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python app.py
```

Open http://127.0.0.1:5000 in your browser.

Docker (build and run):

```powershell
docker build -t portfolio-flask .
docker run -p 5000:5000 portfolio-flask
```

Controls & features:
- Animation toggle: use the "Turn off animations" button at the top-right to disable/enable background animations; the choice is remembered in localStorage.
- Accessibility: the site respects prefers-reduced-motion and provides the toggle for users on low-performance devices.

Files added:
- `app.py` — Flask app and route
- `templates/` — Jinja2 templates (`base.html`, `index.html`)
- `static/css/style.css` — Styles with cloud/devops vibe
- `static/images/` — background and avatar images
- `static/js/animations.js` — subtle particle/cloud animation
- `requirements.txt`, `Dockerfile`, `README.md`

Next steps / suggestions:
- Replace placeholder text and image with your real content and photo.
- Add Lottie animations (drop .json into `static/` and reference in `base.html`) for richer visuals.
- Add contact form backend or integrate a form service.
- Deploy to a PaaS: Render, Fly, or as a container on AWS/GCP.

## Deploy to GCP Cloud Run using GitHub Actions

This repo includes a GitHub Actions workflow (`.github/workflows/deploy-cloudrun.yml`) that builds a Docker image, pushes it to Google Container Registry (GCR) and deploys to Cloud Run when you push to `main`.

Prerequisites:
- A GCP project with billing enabled.
- `gcloud` and IAM permissions to create service accounts (you'll do this in the Console).

Steps (concise):

1. Create a service account and grant roles

	- In GCP Console -> IAM & Admin -> Service Accounts -> Create Service Account.
	- Grant the service account these roles (minimum):
		- Cloud Run Admin (roles/run.admin)
		- Storage Admin or Storage Object Admin (for Container Registry push) (roles/storage.admin)
		- Service Account User (roles/iam.serviceAccountUser)

2. Create a JSON key for the service account

	- After creating the service account, choose "Keys" -> "Add Key" -> Create new key -> JSON. Download the JSON file.

3. Add GitHub secrets

	- In your GitHub repo, go to Settings -> Secrets and variables -> Actions -> New repository secret.
	- Add the following secrets:
		- `GCP_SA_KEY` — the entire JSON file content (copy-paste). Keep this secret.
		- `GCP_PROJECT_ID` — your GCP project id (e.g. `my-gcp-project`).
		- `GCP_REGION` — Cloud Run region (e.g. `us-central1`).

4. Push to `main`

	- The workflow triggers on pushes to `main`. It will:
		- authenticate using the service account key,
		- build a Docker image and push it to `gcr.io/<PROJECT>/portfolio-flask:<sha>`,
		- deploy to Cloud Run as a service named `portfolio-flask` and allow unauthenticated access.

Notes and tweaks
- If you prefer Artifact Registry instead of GCR, modify the workflow's build/push steps accordingly.
- For private Cloud Run (no unauthenticated access), remove `--allow-unauthenticated` and manage IAM to allow members.
- You can change the Cloud Run service name and other `gcloud run deploy` flags as needed (concurrency, memory, min-instances).

Troubleshooting
- If the workflow fails to authenticate, double-check `GCP_SA_KEY` content and that the service account has the required roles.
- For build failures, inspect Docker build logs in the Actions run and ensure the `Dockerfile` is compatible with your base image.

>>>>>>> 3361dcb (Initial commit: Flask portfolio)
