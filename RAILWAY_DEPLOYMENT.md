# Railway Deployment Guide

## Why the Initial Deployment Failed

Railway auto-detected your project and tried to use **Railpack** (which doesn't support docker-compose), causing the build to fail with "Error creating build plan with Railpack".

## ✅ Solution: Deploy Services Individually on Railway

Instead of using docker-compose, Railway works best with individual services. Here's how:

### Step 1: Remove Previous Deployment
1. Go to your Railway project dashboard
2. Click the failed deployment card
3. Click "Settings" → "Danger Zone" → "Delete Project"

### Step 2: Create Separate Services

#### **Service 1: PostgreSQL Database (Easiest)**
1. In Railway dashboard → **"New"** → **"Database"** → **"Postgres"**
2. Wait for it to provision (< 1 minute)
3. Copy the connection string from the "Connect" tab

#### **Service 2: Backend API**
1. **"New"** → **"GitHub Repo"** → Select `eastleigh-united-fc`
2. Use this **Custom Dockerfile**: `backend/Dockerfile.railway`
3. Set **Root Directory**: `backend/`
4. Add Environment Variables (check what Railway provides):
   ```
   SECRET_KEY=31da8b3139077ecd78c679e6bec18774c48550de24f06903627b37e115ffceb3
   POSTGRES_PASSWORD=your-secure-db-password
   DATABASE_URL=${{ Postgres.DATABASE_URL }}
   FLASK_ENV=production
   ```
5. Click "Deploy"

#### **Service 3: Frontend**
1. **"New"** → **"GitHub Repo"** → Select `eastleigh-united-fc`
2. Use this **Custom Dockerfile**: `frontend/Dockerfile`
3. Set **Root Directory**: `frontend/`
4. Add Environment Variable:
   ```
   REACT_APP_API_URL=https://your-backend-url.up.railway.app
   REACT_APP_ADMIN_USERNAME=admin
   REACT_APP_ADMIN_PASSWORD=your-secure-admin-password
   ```
5. Click "Deploy"

### Step 3: Connect Services

1. Go to Backend service
2. Click **"Variables"** tab
3. Click **"Reference"** next to DATABASE_URL
4. Select the **Postgres** service
5. Do the same for Frontend → REACT_APP_API_URL → Backend service

### Step 4: Get Your URLs
- **Frontend URL**: From Frontend service "Deploy" tab
- **Backend URL**: From Backend service "Deploy" tab

---

## Alternative: Keep Using docker-compose (Advanced)

If you want to stick with docker-compose, configure Railway differently:

1. Deploy to **Render** or **DigitalOcean** instead (better docker-compose support)
2. Or use Railway with a **custom Docker image** that handles composition

---

## Environment Variable Reference

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | Generated secure key (use the one from deploy-setup.sh) |
| `POSTGRES_PASSWORD` | Strong random password |
| `DATABASE_URL` | Railway provides this automatically |
| `REACT_APP_API_URL` | Your Railway Backend URL |
| `REACT_APP_ADMIN_USERNAME` | `admin` |
| `REACT_APP_ADMIN_PASSWORD` | Secure password you set |

---

## Troubleshooting

**Backend won't connect to database?**
- Check DATABASE_URL is set correctly
- Ensure it references the Postgres service

**Frontend shows 404 errors?**
- Check REACT_APP_API_URL is correct
- Add a trailing slash: `https://your-backend.up.railway.app/api/`

**Build fails on Railway?**
- Check Root Directory is set correctly
- Verify Dockerfile path is correct
- Check environment variables are set

---

## Quick Reference: What Gets Deployed Where

| Component | Platform | Dockerfile |
|-----------|----------|-----------|
| **Database** | Railway Postgres | (Built-in) |
| **Backend API** | Railway (Docker) | `backend/Dockerfile.railway` |
| **Frontend** | Railway (Docker) | `frontend/Dockerfile` |