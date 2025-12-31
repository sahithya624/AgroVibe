# 🚀 SmartFarmingAI Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)
```bash
# Navigate to project directory
cd SmartFarmingAI

# Install all required packages
pip install -r requirements.txt
```

### Step 2: Configure Environment (1 minute)
```bash
# Copy environment template
copy .env.example .env  # Windows
# OR
cp .env.example .env    # Linux/Mac

# Edit .env file and add your OpenAI API key (optional)
# OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Create Model Directory (30 seconds)
```bash
mkdir backend\ml_models\saved_models  # Windows
# OR
mkdir -p backend/ml_models/saved_models  # Linux/Mac
```

### Step 4: Start the Server (30 seconds)
```bash
uvicorn backend.main:app --reload
```

### Step 5: Test the API (1 minute)
Open your browser and visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 Testing Each Feature

### 1. Test Disease Detection
```bash
# Using curl (replace with actual image path)
curl -X POST "http://localhost:8000/api/predict-disease" \
  -F "image=@path/to/plant_leaf.jpg"
```

**Or use Swagger UI at** http://localhost:8000/docs

### 2. Test Soil Health Analysis
```bash
curl -X POST "http://localhost:8000/api/soil-advice" \
  -H "Content-Type: application/json" \
  -d '{
    "nitrogen": 280,
    "phosphorus": 45,
    "potassium": 220,
    "ph": 6.5,
    "crop_type": "tomato",
    "field_size": 2.5
  }'
```

### 3. Test Smart Irrigation
```bash
curl -X POST "http://localhost:8000/api/water-alert" \
  -H "Content-Type: application/json" \
  -d '{
    "soil_moisture": 45,
    "temperature": 28,
    "humidity": 65,
    "crop_type": "tomato",
    "crop_stage": "flowering",
    "field_size": 2.5
  }'
```

### 4. Test Yield Prediction
```bash
curl -X POST "http://localhost:8000/api/yield-predict" \
  -H "Content-Type: application/json" \
  -d '{
    "crop_type": "tomato",
    "field_size": 2.5,
    "soil_quality": 75,
    "avg_temperature": 25,
    "total_rainfall": 600,
    "fertilizer_used": 150,
    "irrigation_frequency": 3
  }'
```

### 5. Test Market Insights
```bash
curl -X POST "http://localhost:8000/api/market-insights" \
  -H "Content-Type: application/json" \
  -d '{
    "crop_type": "tomato",
    "region": "north_america",
    "quantity": 10
  }'
```

## 📱 Using Swagger UI (Recommended for Beginners)

1. Start the server: `uvicorn backend.main:app --reload`
2. Open browser: http://localhost:8000/docs
3. Click on any endpoint (e.g., `/api/soil-advice`)
4. Click "Try it out"
5. Fill in the request body
6. Click "Execute"
7. View the response below

## 🐍 Using Python Requests

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Test soil advice
response = requests.post(
    f"{BASE_URL}/api/soil-advice",
    json={
        "nitrogen": 280,
        "phosphorus": 45,
        "potassium": 220,
        "ph": 6.5,
        "crop_type": "tomato",
        "field_size": 2.5
    }
)

print(response.json())
```

## 🔧 Troubleshooting

### Issue: Module not found errors
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Port 8000 already in use
**Solution**: Use a different port
```bash
uvicorn backend.main:app --reload --port 8001
```

### Issue: CORS errors
**Solution**: Already configured in `main.py`. For production, update allowed origins.

### Issue: OpenAI API errors
**Solution**: Either:
1. Add valid API key to `.env` file, OR
2. System will use mock responses automatically

## 📊 Expected Responses

### Successful Response Example
```json
{
  "success": true,
  "soil_health_score": 75,
  "npk_status": {
    "nitrogen": {"value": 280, "status": "medium"},
    "phosphorus": {"value": 45, "status": "medium"},
    "potassium": {"value": 220, "status": "medium"}
  },
  "fertilizer_recommendations": {
    "nitrogen": 150,
    "phosphorus": 75,
    "potassium": 100
  },
  "advisory": "Your soil health is good..."
}
```

## 🎓 Next Steps

1. ✅ **Explore all endpoints** using Swagger UI
2. ✅ **Train ML models** using notebooks in `ml_notebooks/`
3. ✅ **Build frontend** following guide in `frontend/README.md`
4. ✅ **Add database** for data persistence
5. ✅ **Deploy to cloud** (AWS, GCP, Azure)

## 📚 Documentation

- **Main README**: `README.md`
- **Architecture**: `ARCHITECTURE.md`
- **API Docs**: http://localhost:8000/docs (when running)
- **Walkthrough**: See artifacts folder

## 💡 Pro Tips

1. Use **Swagger UI** for interactive testing
2. Check **logs** in terminal for debugging
3. Use **mock responses** to test without trained models
4. Add **OpenAI API key** for better recommendations
5. Read **service files** to understand business logic

## 🆘 Need Help?

- Check the main `README.md` for detailed documentation
- Review code comments in service files
- Use Swagger UI for endpoint details
- Check `ARCHITECTURE.md` for system design

---

**Happy Farming! 🌾**
