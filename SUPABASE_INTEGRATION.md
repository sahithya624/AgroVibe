# Supabase Integration Guide for Backend

This file contains example code for integrating Supabase database operations into your FastAPI backend.

## Installation

Add to your `requirements.txt`:
```
supabase==1.0.3
asyncpg==0.28.0
sqlalchemy==2.0.23
```

## Environment Variables

Add to your `.env`:
```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_service_role_key
```

## Example: Database Service

Create `backend/services/database_service.py`:

```python
from supabase import create_client, Client
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Optional
import os

# Supabase client (for storage, auth, realtime)
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# PostgreSQL connection (for direct SQL queries)
database_url = os.getenv("DATABASE_URL")
# Convert postgresql:// to postgresql+asyncpg://
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(database_url, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    """Dependency for getting database session"""
    async with AsyncSessionLocal() as session:
        yield session
```

## Example: Save Disease Detection

```python
async def save_disease_detection(
    user_id: str,
    crop_type: str,
    disease_name: str,
    confidence_score: float,
    image_url: str,
    treatment: str,
    severity: str
):
    """Save disease detection to Supabase"""
    try:
        result = supabase.table("disease_detections").insert({
            "user_id": user_id,
            "crop_type": crop_type,
            "disease_name": disease_name,
            "confidence_score": confidence_score,
            "image_url": image_url,
            "treatment_recommendation": treatment,
            "severity": severity
        }).execute()
        
        return {"success": True, "data": result.data}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Example: Get User's Disease History

```python
async def get_disease_history(user_id: str, limit: int = 10):
    """Get user's disease detection history"""
    try:
        result = supabase.table("disease_detections")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("detection_date", desc=True)\
            .limit(limit)\
            .execute()
        
        return {"success": True, "data": result.data}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Example: Save Soil Analysis

```python
async def save_soil_analysis(
    user_id: str,
    nitrogen: float,
    phosphorus: float,
    potassium: float,
    ph: float,
    crop_type: str,
    field_size: float,
    soil_health_score: float,
    recommendations: dict,
    advisory: str
):
    """Save soil analysis to Supabase"""
    try:
        result = supabase.table("soil_analyses").insert({
            "user_id": user_id,
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium,
            "ph": ph,
            "crop_type": crop_type,
            "field_size": field_size,
            "soil_health_score": soil_health_score,
            "fertilizer_recommendations": recommendations,
            "advisory": advisory
        }).execute()
        
        return {"success": True, "data": result.data}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Example: Integration in Routes

Update `backend/api/routes/disease_routes.py`:

```python
from backend.services.database_service import supabase
from backend.api.deps import get_current_user

@router.post("/disease-detect")
async def detect_disease(
    image: UploadFile = File(...), 
    crop_type: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    # Existing disease detection logic
    result = await analyze_disease(image, crop_type=crop_type)
    
    # Save to database if successful
    if result.get("success"):
        await save_disease_detection(
            user_id=current_user["id"],
            crop_type=crop_type,
            disease_name=result.get("disease"),
            confidence_score=result.get("confidence"),
            image_url="",  # Upload to Supabase Storage first
            treatment=result.get("treatment"),
            severity=result.get("severity")
        )
    
    return result
```

## Example: Upload Image to Supabase Storage

```python
async def upload_disease_image(user_id: str, image: UploadFile) -> str:
    """Upload disease image to Supabase Storage"""
    try:
        # Read file content
        contents = await image.read()
        
        # Generate unique filename
        import uuid
        filename = f"{user_id}/{uuid.uuid4()}.jpg"
        
        # Upload to Supabase Storage
        result = supabase.storage\
            .from_("disease-images")\
            .upload(filename, contents)
        
        # Get public URL
        public_url = supabase.storage\
            .from_("disease-images")\
            .get_public_url(filename)
        
        return public_url
    except Exception as e:
        raise Exception(f"Upload failed: {str(e)}")
```

## Example: Create Notification

```python
async def create_notification(
    user_id: str,
    title: str,
    message: str,
    notification_type: str,
    severity: str = "info"
):
    """Create a notification for user"""
    try:
        result = supabase.table("notifications").insert({
            "user_id": user_id,
            "title": title,
            "message": message,
            "notification_type": notification_type,
            "severity": severity
        }).execute()
        
        return {"success": True, "data": result.data}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Example: Get Dashboard Data

```python
async def get_dashboard_stats(user_id: str):
    """Get aggregated dashboard statistics"""
    try:
        # Get recent detections count
        disease_count = supabase.table("disease_detections")\
            .select("*", count="exact")\
            .eq("user_id", user_id)\
            .execute()
        
        # Get recent soil analyses
        soil_count = supabase.table("soil_analyses")\
            .select("*", count="exact")\
            .eq("user_id", user_id)\
            .execute()
        
        # Get unread notifications
        notifications = supabase.table("notifications")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("is_read", False)\
            .execute()
        
        return {
            "total_disease_detections": disease_count.count,
            "total_soil_analyses": soil_count.count,
            "unread_notifications": len(notifications.data),
            "notifications": notifications.data[:5]  # Last 5
        }
    except Exception as e:
        return {"error": str(e)}
```

## Setting Up Supabase Storage Buckets

Run this in Supabase SQL Editor to create storage buckets:

```sql
-- Create storage bucket for disease images
INSERT INTO storage.buckets (id, name, public)
VALUES ('disease-images', 'disease-images', true);

-- Create storage bucket for user avatars
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true);

-- Storage policies (allow authenticated users to upload)
CREATE POLICY "Users can upload disease images"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'disease-images');

CREATE POLICY "Anyone can view disease images"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'disease-images');
```

## Best Practices

1. **Use Connection Pooling**: Configure max connections in SQLAlchemy
2. **Error Handling**: Always wrap database calls in try-except
3. **Indexes**: Use the indexes already created in schema.sql
4. **Transactions**: Use database transactions for multi-step operations
5. **Validation**: Validate data before inserting to database
6. **Row Level Security**: Leverage Supabase RLS for security
7. **Caching**: Cache frequently accessed data (e.g., crop encyclopedia)

## Migration from Mock Data

To migrate your current implementation:

1. Replace in-memory storage with database calls
2. Update auth service to use `users` table
3. Save all analysis results to respective tables
4. Use Supabase Storage for file uploads
5. Implement notification system
6. Add dashboard endpoint with aggregated data

## Testing Database Connection

Create a test endpoint:

```python
@router.get("/test-db")
async def test_database():
    """Test database connection"""
    try:
        # Test Supabase connection
        result = supabase.table("users").select("count").execute()
        
        return {
            "success": True,
            "message": "Database connection successful",
            "user_count": len(result.data) if result.data else 0
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
```
