# 🌾 SmartFarmingAI - Production Deployment

## 📦 What's Included

Your project is now ready for deployment with the following files:

### Core Application Files
- ✅ **Backend**: FastAPI application in `/backend`
- ✅ **Frontend**: React + Vite application in `/frontend`
- ✅ **Database Schema**: `backend/database/schema.sql` (15+ tables)

### Deployment Configuration Files
- ✅ **render.yaml**: Backend deployment config for Render
- ✅ **.env.example**: Environment variables template
- ✅ **requirements.txt**: Python dependencies

### Documentation
- ✅ **DEPLOYMENT_GUIDE.md**: Detailed deployment instructions (see artifacts)
- ✅ **SUPABASE_INTEGRATION.md**: Database integration examples
- ✅ **QUICKSTART.md**: Local development guide
- ✅ **ARCHITECTURE.md**: System architecture

---

## 🚀 Quick Start: Deploy in 20 Minutes

### Prerequisites
- GitHub account
- Supabase account (free)
- Render account (free)
- Vercel account (free)

### Step-by-Step

#### 1. Setup Database (Supabase) - 5 minutes
```bash
# 1. Go to https://supabase.com
# 2. Create new project
# 3. Copy content from backend/database/schema.sql
# 4. Paste in SQL Editor → Run
# 5. Save these credentials:
#    - Project URL
#    - anon key (public)
#    - service_role key (secret)
#    - Database connection string
```

#### 2. Deploy Backend (Render) - 10 minutes
```bash
# 1. Push code to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_REPO_URL
git push -u origin main

# 2. Go to https://render.com
# 3. New Web Service → Connect GitHub repo
# 4. Use these settings:
#    - Build: pip install -r requirements.txt
#    - Start: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
# 5. Add environment variables from Supabase
# 6. Deploy!
```

#### 3. Deploy Frontend (Vercel) - 5 minutes
```bash
# 1. Go to https://vercel.com
# 2. Import GitHub repo
# 3. Settings:
#    - Framework: Vite
#    - Root Directory: frontend
#    - Build: npm run build
#    - Output: dist
# 4. Add environment variables:
#    VITE_API_BASE_URL=https://YOUR-BACKEND.onrender.com/api
#    VITE_SUPABASE_URL=https://YOUR-PROJECT.supabase.co
#    VITE_SUPABASE_ANON_KEY=your_anon_key
# 5. Deploy!
```

---

## 🔑 Required API Keys

### Get These First (All Free)

1. **Groq API Key** (REQUIRED)
   - Get from: https://console.groq.com
   - Used for: AI-powered recommendations
   - Free tier: Very generous

2. **Supabase Credentials** (REQUIRED)
   - Get from: Your Supabase project dashboard
   - Used for: Database, authentication, storage
   - Free tier: 500MB database, 1GB storage

### Optional (Enhance Features)

3. **OpenWeatherMap API** (Optional)
   - Get from: https://openweathermap.org/api
   - Used for: Real-time weather data
   - Free tier: 1000 calls/day

4. **OpenAI API** (Optional)
   - Get from: https://platform.openai.com
   - Used for: Alternative to Groq
   - Note: Costs money per request

---

## ⚙️ Environment Variables

### Backend Environment Variables (Set in Render)

```env
# Database (from Supabase)
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI... (service_role key - keep secret!)

# AI Service (from Groq)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx

# Authentication (generate yourself)
JWT_SECRET_KEY=<run: openssl rand -hex 32>

# Optional APIs
WEATHER_API_KEY=xxxxxxxxxxxxx (optional)
OPENAI_API_KEY=sk-xxxxxxxxxx (optional)
DEFAULT_CITY=New York
```

### Frontend Environment Variables (Set in Vercel)

```env
VITE_API_BASE_URL=https://your-backend.onrender.com/api
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI... (anon PUBLIC key - safe to expose)
```

### Generate JWT Secret

Run this command locally:
```bash
openssl rand -hex 32
```

Copy the output and use it as your `JWT_SECRET_KEY`.

---

## 📋 Deployment Checklist

### Before Deployment
- [ ] Code tested locally
- [ ] All files committed to Git
- [ ] GitHub repository created
- [ ] API keys obtained

### Supabase Setup
- [ ] Project created
- [ ] schema.sql executed
- [ ] Tables verified (check in Table Editor)
- [ ] Credentials copied

### Render (Backend)
- [ ] Web service created
- [ ] GitHub connected
- [ ] Build/start commands set
- [ ] Environment variables added
- [ ] First deploy successful
- [ ] `/health` endpoint working
- [ ] `/docs` endpoint accessible

### Vercel (Frontend)
- [ ] Project imported
- [ ] Build settings configured
- [ ] Environment variables set
- [ ] Deploy successful
- [ ] Site loads properly

### Final Configuration
- [ ] Backend CORS updated with Vercel URL
- [ ] Supabase auth URLs configured
- [ ] Test user signup/login
- [ ] Test disease detection
- [ ] Test soil analysis
- [ ] Test yield prediction
- [ ] Test market insights

---

## 🌐 Your Production URLs

After deployment, you'll have these URLs:

```
Frontend Application:
→ https://smartfarmingai.vercel.app

Backend API:
→ https://smartfarmingai-backend.onrender.com

API Documentation:
→ https://smartfarmingai-backend.onrender.com/docs

Database:
→ db.xxxxxxxxxxxxx.supabase.co (via Supabase Dashboard)
```

---

## 🛠️ Database Schema Overview

The `schema.sql` includes:

### Core Tables
- **users**: User authentication and profiles
- **disease_detections**: Disease analysis history
- **soil_analyses**: Soil health records
- **yield_predictions**: Crop yield forecasts
- **market_insights**: Market analysis data
- **irrigation_logs**: Smart irrigation records

### Additional Tables
- **notifications**: User alerts and messages
- **farm_fields**: Multi-field management
- **chat_history**: AI chat conversations
- **weather_cache**: Weather data cache
- **sensor_data**: IoT sensor readings
- **crop_encyclopedia**: Crop reference data (pre-populated)

### Features
- ✅ Row Level Security (RLS) enabled
- ✅ Automatic timestamps with triggers
- ✅ Indexes for performance
- ✅ Sample crop data included
- ✅ Full text search ready

---

## 🔍 Verify Deployment

### Test Backend
```bash
# Health check
curl https://your-backend.onrender.com/health

# API docs
open https://your-backend.onrender.com/docs
```

### Test Database
```sql
-- In Supabase SQL Editor
SELECT tablename FROM pg_tables WHERE schemaname = 'public';
-- Should show 15+ tables
```

### Test Frontend
```bash
# Open in browser
open https://your-app.vercel.app

# Test features:
# 1. Sign up
# 2. Login
# 3. Try each feature
```

---

## 🐛 Troubleshooting

### Backend Won't Start
1. Check environment variables in Render
2. Verify `requirements.txt` has all dependencies
3. Check logs in Render dashboard
4. Ensure `DATABASE_URL` is correct

### Frontend Can't Connect to Backend
1. Verify `VITE_API_BASE_URL` in Vercel
2. Check CORS settings in backend
3. Clear browser cache
4. Check Network tab in DevTools

### Database Connection Issues
1. Verify Supabase project is active
2. Check connection string format
3. Ensure password doesn't have special characters breaking URL
4. Test connection in Supabase dashboard

### Render Free Tier Slowness
- Free tier spins down after 15 min inactivity
- First request takes 30-60 seconds to wake up
- Solution: Upgrade to paid plan ($7/mo) or use a ping service

---

## 💰 Cost Estimate

### Free Forever (What you get)
- **Supabase**: 500MB database, 1GB storage, 2GB bandwidth
- **Render**: 750 hours/month (enough for one service)
- **Vercel**: 100GB bandwidth, unlimited deployments
- **Groq**: Very generous free tier for AI

**Total: $0/month** for hobby projects!

### When to Upgrade
- **Heavy traffic**: Upgrade Render ($7/mo) for always-on
- **More data**: Upgrade Supabase ($25/mo) for more storage
- **Production**: Consider all paid plans for reliability

---

## 📚 Additional Resources

### Deployment Documentation
- Full guide in artifacts: `deployment_guide.md`
- Quick reference: `deployment_summary.md`
- Integration guide: `SUPABASE_INTEGRATION.md`

### Platform Documentation
- [Supabase Docs](https://supabase.com/docs)
- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)

### Local Development
- Quick start: `QUICKSTART.md`
- Architecture: `ARCHITECTURE.md`
- Project summary: `PROJECT_SUMMARY.md`

---

## 🎉 You're All Set!

Everything you need for deployment is ready:

✅ Database schema created  
✅ Deployment configs prepared  
✅ Environment variables documented  
✅ Step-by-step guides provided  
✅ Troubleshooting help available  

**Start deploying now!** Follow the 3-step process above, and you'll be live in 20 minutes!

---

## 📞 Need Help?

Check the comprehensive guides in the artifacts folder:
- Detailed deployment guide
- Supabase integration examples
- Troubleshooting section

Good luck with your deployment! 🚀🌾
