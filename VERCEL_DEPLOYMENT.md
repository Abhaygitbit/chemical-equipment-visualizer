# Vercel Deployment Guide

## Prerequisites
- Vercel Account (https://vercel.com/abhays-projects-0099f8ce)
- GitHub Repository (https://github.com/Abhaygitbit/chemical-equipment-visualizer)

## Step 1: Configure Backend URL
Before deploying, you need a backend URL. Options:
- Render.com (free tier available)
- Railway.app
- Heroku
- AWS, Google Cloud, etc.

## Step 2: Deploy Frontend to Vercel

### Option A: Using Vercel CLI (Recommended)
1. Install Vercel CLI:
   ```
   npm install -g vercel
   ```

2. From the `frontend-web` directory, run:
   ```
   vercel --prod
   ```

3. When prompted, enter your project details and configure environment variables.

### Option B: Connect GitHub Repository
1. Go to https://vercel.com/abhays-projects-0099f8ce
2. Click "Add New..." → "Project"
3. Select your GitHub repository
4. Set the following build settings:
   - **Framework**: React
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install`

5. Add Environment Variables:
   - **REACT_APP_API_URL**: Your backend API URL (e.g., `https://your-backend.com/api`)

6. Click Deploy

## Step 3: Backend Deployment
Deploy your Django backend to a hosting service and update the `REACT_APP_API_URL` in Vercel.

## Step 4: Test the Deployment
1. Visit your Vercel deployment URL
2. Upload a CSV file to test the integration
3. Verify data appears on the dashboard

## Important Notes
- Update `CORS_ALLOWED_ORIGINS` in Django settings.py with your Vercel domain
- Update `CSRF_TRUSTED_ORIGINS` for production
- Never commit sensitive information to Git
- Use environment variables for API URLs and secrets

## Files Created/Modified for Vercel
- `vercel.json` - Build configuration
- `.vercelignore` - Files to ignore during deployment
- `.env.production` - Production environment variables

## Support
For issues with Vercel deployment, visit: https://vercel.com/docs
