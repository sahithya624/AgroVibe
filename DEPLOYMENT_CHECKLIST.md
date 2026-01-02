# AgroVibe - Complete Deployment Checklist

## ✅ Current Status

### Backend (Render) - LIVE ✓
- **URL**: https://agrovibe.onrender.com
- **Status**: Deployed and running
- **Database**: Connected to Supabase ✓

### Frontend (Vercel/Netlify) - NEEDS SETUP
- **Status**: Needs deployment or redeployment

---

## 🔧 Step-by-Step Deployment Guide

### 1. Supabase Database Setup (REQUIRED)

#### A. Run the Schema
1. Go to https://supabase.com/dashboard
2. Select your project: `gwodkcstkpgpxeabvkei`
3. Click **SQL Editor** in the left sidebar
4. Click **New Query**
5. Copy the entire contents of `backend/database/schema.sql`
6. Paste into the SQL editor
7. Click **Run** (or press Ctrl+Enter)
8. Verify: You should see "Success. No rows returned" message

#### B. Verify Tables Created
1. Go to **Table Editor** in Supabase dashboard
2. You should see these tables:
   - users
   - disease_detections
   - soil_analyses
   - yield_predictions
   - market_insights
   - irrigation_logs
   - notifications
   - chat_history
   - farm_fields
   - weather_cache
   - crop_encyclopedia

---

### 2. Render Backend - Environment Variables (COMPLETED ✓)

Your Render service already has these variables set:
- ✓ `SUPABASE_URL`
- ✓ `SUPABASE_ANON_KEY` (being used as SUPABASE_KEY)
- ✓ `SUPABASE_SERVICE_ROLE_KEY`
- ✓ `ENABLE_REAL_DB=true`
- ✓ `GROQ_API_KEY` (if you have it)

**Optional additions:**
- `WEATHER_API_KEY` - Get from https://openweathermap.org/api
- `DEFAULT_CITY` - Your default city (e.g., "Mumbai")

---

### 3. Frontend Deployment

#### Option A: Deploy to Vercel (Recommended)

1. **Push Latest Changes to GitHub**
   ```bash
   git add .
   git commit -m "chore: update production environment variables"
   git push
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com
   - Click **Add New Project**
   - Import your GitHub repository: `sahithya624/AgroVibe`
   - Select the `frontend` directory as the root

3. **Configure Build Settings**
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Add Environment Variables in Vercel**
   Go to Project Settings → Environment Variables and add:
   
   ```
   VITE_API_BASE_URL=https://agrovibe.onrender.com/api
   VITE_SUPABASE_URL=https://gwodkcstkpgpxeabvkei.supabase.co
   VITE_SUPABASE_ANON_KEY=<your_supabase_anon_key>
   ```

5. **Deploy**
   - Click **Deploy**
   - Wait for build to complete
   - Your app will be live at `https://your-project.vercel.app`

#### Option B: Deploy to Netlify

1. **Push Latest Changes** (same as above)

2. **Connect to Netlify**
   - Go to https://netlify.com
   - Click **Add new site** → **Import an existing project**
   - Connect to GitHub and select `sahithya624/AgroVibe`

3. **Configure Build Settings**
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`

4. **Add Environment Variables**
   Go to Site settings → Environment variables:
   
   ```
   VITE_API_BASE_URL=https://agrovibe.onrender.com/api
   VITE_SUPABASE_URL=https://gwodkcstkpgpxeabvkei.supabase.co
   VITE_SUPABASE_ANON_KEY=<your_supabase_anon_key>
   ```

5. **Deploy**
   - Click **Deploy site**
   - Your app will be live at `https://your-site.netlify.app`

---

### 4. Post-Deployment Verification

#### A. Test Backend
1. Visit: https://agrovibe.onrender.com
2. You should see: `{"message":"Welcome to SmartFarmingAI API","status":"Running","version":"1.0.0"}`

#### B. Test Frontend
1. Visit your deployed frontend URL
2. Try to **Sign Up** with a valid email (e.g., `test@example.com`)
3. Check if you can:
   - Upload an image for disease detection
   - View the dashboard
   - Navigate between pages

#### C. Check Database
1. Go to Supabase → Table Editor → `users`
2. After signing up, you should see your user record

---

### 5. Common Issues & Solutions

#### Issue: "Email address is invalid"
**Solution**: Use a complete, valid email format (e.g., `user@example.com`, not `user@gmail`)

#### Issue: Frontend can't connect to backend
**Solution**: 
- Verify `VITE_API_BASE_URL` is set correctly in Vercel/Netlify
- Check CORS is enabled in backend (already done)
- Ensure backend is running (check Render logs)

#### Issue: Database errors
**Solution**:
- Verify schema was run successfully in Supabase
- Check RLS policies are enabled
- Ensure `ENABLE_REAL_DB=true` in Render

---

### 6. Optional Enhancements

#### Add Weather API
1. Get free API key from https://openweathermap.org/api
2. Add to Render environment variables:
   ```
   WEATHER_API_KEY=your_key_here
   DEFAULT_CITY=Mumbai
   ```

#### Enable Email Confirmations in Supabase
1. Go to Supabase → Authentication → Settings
2. Enable "Confirm email" if you want email verification
3. Configure email templates

---

## 📋 Final Checklist

- [ ] Supabase schema executed successfully
- [ ] All tables visible in Supabase Table Editor
- [ ] Render backend is live and responding
- [ ] Frontend deployed to Vercel/Netlify
- [ ] Environment variables set in frontend platform
- [ ] Can sign up with valid email
- [ ] Can log in successfully
- [ ] Disease detection works
- [ ] Dashboard loads properly

---

## 🎉 Success Criteria

Your deployment is complete when:
1. ✅ Backend shows "Database connection verified" in logs
2. ✅ Frontend loads without errors
3. ✅ Users can sign up and log in
4. ✅ All features (disease detection, soil analysis, etc.) work
5. ✅ Data is being saved to Supabase

---

## 📞 Support

If you encounter issues:
1. Check Render logs for backend errors
2. Check browser console for frontend errors
3. Verify all environment variables are set correctly
4. Ensure Supabase schema was run successfully

**Current Deployment URLs:**
- Backend: https://agrovibe.onrender.com
- Frontend: (To be deployed)
- Supabase: https://gwodkcstkpgpxeabvkei.supabase.co
