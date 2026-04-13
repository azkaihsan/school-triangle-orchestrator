# Deploy to Google Cloud Run

Complete guide for deploying the School Triangle Orchestrator API to Cloud Run.

---

## Prerequisites

- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated
- A GCP project with billing enabled
- Docker installed (only needed for local testing)
- Your AlloyDB / Cloud SQL PostgreSQL instance ready (or any `DATABASE_URL`)
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/)

---

## 1. Set Your GCP Project

```bash
gcloud config set project YOUR_PROJECT_ID
export PROJECT_ID=$(gcloud config get-value project)
export REGION=asia-southeast1
```

---

## 2. Enable Required APIs

```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com
```

---

## 3. Create Artifact Registry Repository

```bash
gcloud artifacts repositories create school-triangle \
  --repository-format=docker \
  --location=$REGION \
  --description="School Triangle Orchestrator images"
```

Authenticate Docker:
```bash
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```

---

## 4. Store Secrets in Secret Manager

Store your database URL and Gemini API key as GCP secrets (never hardcode them):

```bash
# PostgreSQL / AlloyDB connection string
echo -n "postgresql+asyncpg://USER:PASSWORD@HOST:5432/DBNAME?sslmode=require" | \
  gcloud secrets create school-triangle-db-url --data-file=-

# Gemini API key (from https://aistudio.google.com/)
echo -n "YOUR_GEMINI_API_KEY" | \
  gcloud secrets create school-triangle-gemini-key --data-file=-
```

> **AlloyDB users:** use the AlloyDB instance's private IP if Cloud Run is in the same VPC,
> or connect via AlloyDB Auth Proxy. See [AlloyDB + Cloud Run guide](https://cloud.google.com/alloydb/docs/connect-run).

---

## 5a. Deploy with Cloud Build (CI/CD — Recommended)

This uses `cloudbuild.yaml` at the repo root to build, push, and deploy automatically.

Grant Cloud Build the Cloud Run deployer role:
```bash
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

Trigger a manual build:
```bash
gcloud builds submit --config=cloudbuild.yaml \
  --substitutions=_REGION=$REGION,SHORT_SHA=$(git rev-parse --short HEAD) .
```

Or connect your GitHub repository in the **Cloud Build → Triggers** console for automatic deploys on every push.

---

## 5b. Deploy Manually (One-off)

Build and push the image:
```bash
IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/school-triangle/school-triangle-orchestrator:latest"

docker build -t $IMAGE artifacts/api-server/
docker push $IMAGE
```

Deploy to Cloud Run:
```bash
gcloud run deploy school-triangle-orchestrator \
  --image=$IMAGE \
  --region=$REGION \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080 \
  --min-instances=0 \
  --max-instances=5 \
  --memory=512Mi \
  --cpu=1 \
  --set-env-vars=NODE_ENV=production \
  --update-secrets=DATABASE_URL=school-triangle-db-url:latest,GEMINI_API_KEY=school-triangle-gemini-key:latest
```

---

## 6. Verify Deployment

```bash
SERVICE_URL=$(gcloud run services describe school-triangle-orchestrator \
  --region=$REGION --format='value(status.url)')

# Health check
curl $SERVICE_URL/api/healthz

# List students
curl $SERVICE_URL/api/students

# Swagger UI
echo "Open in browser: $SERVICE_URL/api/docs"
```

---

## Environment Variables Reference

| Variable | Where Set | Description |
|---|---|---|
| `PORT` | Cloud Run (auto) | Port to listen on (Cloud Run sets this automatically) |
| `NODE_ENV` | `--set-env-vars` | Set to `production` to disable hot-reload |
| `DATABASE_URL` | Secret Manager | PostgreSQL/AlloyDB connection string |
| `GEMINI_API_KEY` | Secret Manager | Google AI Studio API key |

---

## AlloyDB Specific Notes

If using AlloyDB (as designed for production):

1. **Same VPC:** Set `DATABASE_URL` to the AlloyDB private IP. Ensure Cloud Run is configured to use VPC egress:
   ```bash
   gcloud run services update school-triangle-orchestrator \
     --region=$REGION \
     --vpc-connector=YOUR_VPC_CONNECTOR \
     --vpc-egress=private-ranges-only
   ```

2. **AlloyDB Auth Proxy:** Use the proxy sidecar pattern for secure connections without managing SSL certs. See [AlloyDB Auth Proxy docs](https://cloud.google.com/alloydb/docs/auth-proxy/overview).

---

## Useful Commands

```bash
# View logs
gcloud run services logs read school-triangle-orchestrator --region=$REGION --limit=50

# Update an env var
gcloud run services update school-triangle-orchestrator \
  --region=$REGION \
  --set-env-vars=KEY=VALUE

# Roll back to a previous revision
gcloud run revisions list --service=school-triangle-orchestrator --region=$REGION
gcloud run services update-traffic school-triangle-orchestrator \
  --region=$REGION \
  --to-revisions=REVISION_NAME=100
```
