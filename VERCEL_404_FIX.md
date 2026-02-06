# 🔧 VERCEL 404 FIX - COMPLETE GUIDE

## Problem: 404 NOT_FOUND on Vercel

Your Vercel deployment is showing 404 because the root directory isn't set to `frontend-web`. Follow these exact steps:

---

## ✅ STEP 1: Access Vercel Settings (DO THIS NOW!)

1. Go to: https://vercel.com/abhays-projects-0099f8ce
2. Look for your project named `chemical-equipment-visualizer` or similar
3. Click on the project name to open it
4. Click on the **SETTINGS** tab at the top

---

## ✅ STEP 2: Set Root Directory to frontend-web

1. In Settings, look for **"Root Directory"** on the left menu
2. Click on **"Root Directory"**
3. You should see a dropdown with current value
4. **Clear it and type**: `frontend-web`
5. **Click "Save"** at the bottom

**Screenshot of what to look for:**
- Left sidebar: "Root Directory"
- Input field showing: `frontend-web`
- Save button at bottom

---

## ✅ STEP 3: Add Environment Variables

1. Still in Settings, click **"Environment Variables"** on the left
2. Click **"Add New"** button
3. Fill in:
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `http://localhost:8000/api`
   - **Select**: Production, Preview, Development (all three checkboxes)
4. Click **"Save"**

---

## ✅ STEP 4: Trigger Redeploy

1. Click on **"Deployments"** tab
2. Find your latest deployment (the top one)
3. Click the **three dots (...)** menu on the right
4. Click **"Redeploy"**
5. Wait 2-5 minutes for the build to complete
6. You should see: "✓ Ready"

---

## ✅ STEP 5: Test the Deployment

1. Click the **"Visit"** button or copy your deployment URL
2. Should be something like: `https://chemical-equipment-visualizer-ten.vercel.app`
3. You should see:
   - 🧪 Title: "Chemical Equipment Visualizer"
   - 📁 Upload area with "Click to select CSV file"
   - 🚀 Upload button

**If you still see 404:**
- Clear browser cache (Ctrl+Shift+Del)
- Try incognito/private browser window

---

## 🔧 Backend Upload 404 Fix

If upload shows 404 error, it's because the backend URL isn't correct. Do this:

### For Local Testing (Backend on Localhost):
1. Your React app shows: `http://localhost:3000` ✅
2. Backend is: `http://localhost:8000` ✅
3. API calls go to: `http://localhost:8000/api` ✅

**In browser DevTools (F12), Console should show:**
```
No CORS errors if both are on localhost
```

### For Production (Backend Deployed):
1. Deploy backend first (Render.com, Railway, Heroku)
2. Get backend URL (e.g., `https://my-backend.render.com`)
3. Update Vercel env var: `REACT_APP_API_URL=https://my-backend.render.com/api`
4. Redeploy Vercel frontend
5. Update Django CORS settings:
   ```python
   CORS_ALLOWED_ORIGINS = [
       "https://chemical-equipment-visualizer-ten.vercel.app",  # Your Vercel URL
       "http://localhost:3000",
   ]
   ```

---

## ✅ Complete Checklist

- [ ] Went to https://vercel.com/abhays-projects-0099f8ce
- [ ] Clicked on your project
- [ ] Opened "Settings"
- [ ] Found "Root Directory" and set it to `frontend-web`
- [ ] Clicked "Save"
- [ ] Went to "Environment Variables"
- [ ] Added `REACT_APP_API_URL=http://localhost:8000/api`
- [ ] Clicked "Save"
- [ ] Went to "Deployments"
- [ ] Clicked "Redeploy" on latest deployment
- [ ] Waited for build to complete
- [ ] Visited the URL and saw the app (not 404)
- [ ] Tested file upload with sample CSV

---

## 📋 Sample Test CSV

If you want to test upload, create a file named `test.csv`:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-A,Centrifugal,100.5,50.2,80.5
Pump-B,Positive Displacement,150.3,60.1,85.2
Compressor-A,Rotary,250.3,40.8,75.2
```

Upload this file to test the API.

---

## 🐛 Troubleshooting

### Still Seeing 404?
1. Clear browser cache (Ctrl+Shift+Delete)
2. Try in incognito window
3. Check if Redeploy completed (should say "✓ Ready")
4. Wait 5 minutes and refresh

### Upload Returns 404?
1. Check browser DevTools (F12)
2. Go to "Network" tab
3. Try uploading file
4. Check if request goes to correct URL
5. Should be: `http://localhost:8000/api/upload/`

### CORS Errors?
1. This means frontend can't reach backend
2. Check if backend is running
3. Update API URL if backend changed location

---

## 📞 Need Help?

Run this to verify backend is working:
```bash
curl http://localhost:8000/api/health/
```

You should see:
```json
{"status":"healthy","datasets":2}
```

If backend isn't responding, start it:
```bash
cd backend
python manage.py runserver
```

---

**DO THESE STEPS NOW AND YOUR 404 WILL BE FIXED!**
