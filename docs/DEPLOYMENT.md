# Deployment Guide - Vertex AI Staging

## Prerequisites

1. **GCP Project Setup**
   - Project ID: `aipodcaster-481909` (already configured)
   - Vertex AI API enabled
   - Service account with permissions

2. **Local Configuration**
   - Service account JSON: `/Users/sargupta/Desktop/AI Video/gcp-credentials.json`
   - `.env` configured for Vertex AI

## Quick Staging Deployment

### Option 1: Cloud Run (Recommended)

```bash
# 1. Authenticate
gcloud auth login
gcloud config set project aipodcaster-481909

# 2. Build and push container
gcloud builds submit --tag gcr.io/aipodcaster-481909/ai-video-production

# 3. Deploy to Cloud Run
gcloud run deploy ai-video-staging \
  --image gcr.io/aipodcaster-481909/ai-video-production \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_GENAI_USE_VERTEXAI=true,GOOGLE_CLOUD_PROJECT=aipodcaster-481909 \
  --memory 2Gi \
  --timeout 300
```

### Option 2: Compute Engine VM

```bash
# 1. Create VM
gcloud compute instances create ai-video-staging \
  --zone=us-central1-a \
  --machine-type=n1-standard-2 \
  --scopes=https://www.googleapis.com/auth/cloud-platform

# 2. SSH and deploy
gcloud compute ssh ai-video-staging --zone=us-central1-a

# On VM:
git clone <repo-url>
cd AI\ Video
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy credentials
# Configure .env

# Run
python run_e2e_sequential.py "Test Topic"
```

## Testing Staging

```bash
# Get service URL
gcloud run services describe ai-video-staging \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'

# Test endpoint
curl -X POST https://[SERVICE-URL]/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test Deployment"}'
```

## Monitoring

```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=ai-video-staging" --limit 50

# Check metrics
gcloud monitoring dashboards list
```

## Rollback

```bash
# List revisions
gcloud run revisions list --service ai-video-staging

# Rollback to previous
gcloud run services update-traffic ai-video-staging \
  --to-revisions=REVISION-NAME=100
```

## Environment Variables for Staging

```bash
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=aipodcaster-481909
DEFAULT_MODEL=gemini-2.0-flash
LOG_LEVEL=INFO
DEBUG=false
```

## Cost Estimation

**Cloud Run (per request):**
- Compute: ~$0.00002400/request
- Vertex AI: ~$0.002/1K tokens
- Storage: Minimal

**Estimated Monthly (1000 requests):**
- ~$25-50 USD

## Next Steps

1. Deploy to staging using Cloud Run
2. Run smoke tests
3. Monitor for 24-48 hours
4. If stable, promote to production
5. Set up alerts and monitoring dashboards
