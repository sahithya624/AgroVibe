-- ============================================
-- SmartFarmingAI Database Schema for Supabase
-- Optimized for Production Deployment
-- ============================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1. Profiles / Users Table
-- This table links directly to Supabase Auth
-- ============================================

CREATE TABLE IF NOT EXISTS public.users (
    -- Link to auth.users UUID
    id UUID PRIMARY KEY REFERENCES auth.users ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    
    -- Farm-specific info
    phone_number TEXT,
    farm_location TEXT,
    farm_size_acres DECIMAL(10, 2),
    primary_crops TEXT[], -- Array of crops they grow
    profile_image_url TEXT,
    
    -- App preferences
    preferred_language TEXT DEFAULT 'en',
    notifications_enabled BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    -- Check constraints
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
);

-- Enable RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- ============================================
-- 2. Auth Trigger
-- Automatically creates a user record when someone signs up
-- ============================================

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.users (id, email, full_name)
    VALUES (
        new.id, 
        new.email, 
        COALESCE(new.raw_user_meta_data->>'full_name', 'User ' || substr(new.id::text, 1, 8))
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for auth.users
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ============================================
-- 3. Feature Tables
-- ============================================

-- Disease Detection History
CREATE TABLE IF NOT EXISTS public.disease_detections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    crop_type VARCHAR(100),
    disease_name VARCHAR(255),
    confidence_score DECIMAL(5, 4),
    image_url TEXT,
    treatment_recommendation TEXT,
    severity VARCHAR(50), -- low, medium, high, critical
    detection_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    location_lat DECIMAL(10, 8),
    location_lng DECIMAL(11, 8),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Soil Health Analysis History
CREATE TABLE IF NOT EXISTS public.soil_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    nitrogen DECIMAL(10, 2) NOT NULL,
    phosphorus DECIMAL(10, 2) NOT NULL,
    potassium DECIMAL(10, 2) NOT NULL,
    ph DECIMAL(4, 2) NOT NULL,
    crop_type VARCHAR(100) NOT NULL,
    field_size DECIMAL(10, 2) NOT NULL, -- in acres
    soil_health_score DECIMAL(5, 2), -- 0-100
    npk_status JSONB, 
    fertilizer_recommendations JSONB,
    advisory TEXT,
    location_lat DECIMAL(10, 8),
    location_lng DECIMAL(11, 8),
    analysis_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Yield Predictions History
CREATE TABLE IF NOT EXISTS public.yield_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    crop_type VARCHAR(100) NOT NULL,
    field_size DECIMAL(10, 2) NOT NULL,
    soil_quality DECIMAL(5, 2) NOT NULL,
    avg_temperature DECIMAL(5, 2),
    total_rainfall DECIMAL(10, 2),
    fertilizer_used DECIMAL(10, 2),
    irrigation_frequency DECIMAL(5, 2),
    predicted_yield DECIMAL(10, 2),
    confidence_level VARCHAR(50),
    yield_per_acre DECIMAL(10, 2),
    advisory TEXT,
    recommendations JSONB,
    prediction_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expected_harvest_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Market Insights History
CREATE TABLE IF NOT EXISTS public.market_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    crop_type VARCHAR(100) NOT NULL,
    region VARCHAR(255) NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL,
    current_price DECIMAL(10, 2),
    price_trend VARCHAR(50),
    demand_level VARCHAR(50),
    best_selling_time VARCHAR(255),
    market_advisory TEXT,
    price_forecast JSONB,
    insight_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Irrigation Logs
CREATE TABLE IF NOT EXISTS public.irrigation_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    soil_moisture DECIMAL(5, 2) NOT NULL,
    temperature DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    crop_type VARCHAR(100) NOT NULL,
    crop_stage VARCHAR(50),
    field_size DECIMAL(10, 2),
    weather_data JSONB,
    should_irrigate BOOLEAN,
    water_amount DECIMAL(10, 2),
    irrigation_priority VARCHAR(50),
    reasoning TEXT,
    alert_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    scheduled_irrigation_time TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'pending',
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Notifications
CREATE TABLE IF NOT EXISTS public.notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    severity VARCHAR(50) DEFAULT 'info',
    related_entity_type VARCHAR(50),
    related_entity_id UUID,
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- AI Chat History
CREATE TABLE IF NOT EXISTS public.chat_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    chat_type VARCHAR(50),
    context JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Farm Fields
CREATE TABLE IF NOT EXISTS public.farm_fields (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    field_name VARCHAR(255) NOT NULL,
    field_size DECIMAL(10, 2) NOT NULL,
    location_lat DECIMAL(10, 8),
    location_lng DECIMAL(11, 8),
    current_crop VARCHAR(100),
    planting_date DATE,
    expected_harvest_date DATE,
    soil_type VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Weather Cache
CREATE TABLE IF NOT EXISTS public.weather_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    city VARCHAR(255) NOT NULL,
    temperature DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    weather_condition VARCHAR(255),
    weather_data JSONB,
    fetched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(city, fetched_at)
);

-- Crop Encyclopedia
CREATE TABLE IF NOT EXISTS public.crop_encyclopedia (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_name VARCHAR(100) UNIQUE NOT NULL,
    scientific_name VARCHAR(255),
    category VARCHAR(100),
    description TEXT,
    optimal_temperature_min DECIMAL(5, 2),
    optimal_temperature_max DECIMAL(5, 2),
    water_requirements VARCHAR(50),
    soil_ph_min DECIMAL(4, 2),
    soil_ph_max DECIMAL(4, 2),
    growing_season VARCHAR(100),
    days_to_maturity INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 4. RLS Policies
-- ============================================

-- Function to check if user is admin (optional)
-- CREATE OR REPLACE FUNCTION public.is_admin() ...

-- Enable RLS on all tables
ALTER TABLE public.disease_detections ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.soil_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.yield_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.market_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.irrigation_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.farm_fields ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.crop_encyclopedia ENABLE ROW LEVEL SECURITY;

-- Users Policy
CREATE POLICY "Users can view own data" ON public.users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own data" ON public.users FOR UPDATE USING (auth.uid() = id);

-- Disease Detections Policy
CREATE POLICY "Users can manage own disease detections" ON public.disease_detections
    FOR ALL USING (auth.uid() = user_id);

-- Soil Analysis Policy
CREATE POLICY "Users can manage own soil analyses" ON public.soil_analyses
    FOR ALL USING (auth.uid() = user_id);

-- Yield Prediction Policy
CREATE POLICY "Users can manage own yield predictions" ON public.yield_predictions
    FOR ALL USING (auth.uid() = user_id);

-- Market Insights Policy
CREATE POLICY "Users can manage own market insights" ON public.market_insights
    FOR ALL USING (auth.uid() = user_id);

-- Irrigation Logs Policy
CREATE POLICY "Users can manage own irrigation logs" ON public.irrigation_logs
    FOR ALL USING (auth.uid() = user_id);

-- Chat History Policy
CREATE POLICY "Users can manage own chat history" ON public.chat_history
    FOR ALL USING (auth.uid() = user_id);

-- Notifications Policy
CREATE POLICY "Users can manage own notifications" ON public.notifications
    FOR ALL USING (auth.uid() = user_id);

-- Farm Fields Policy
CREATE POLICY "Users can manage own farm fields" ON public.farm_fields
    FOR ALL USING (auth.uid() = user_id);

-- Crop Encyclopedia Policy (Public Read Only)
CREATE POLICY "Anyone can view crop encyclopedia" ON public.crop_encyclopedia
    FOR SELECT USING (true);

-- ============================================
-- 5. Triggers for updated_at
-- ============================================

CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_farm_fields_updated_at BEFORE UPDATE ON public.farm_fields
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_crop_encyclopedia_updated_at BEFORE UPDATE ON public.crop_encyclopedia
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ============================================
-- 6. Storage Buckets Setup
-- Run these as a separate script if needed, or include here
-- Note: Requires storage extension enabled
-- ============================================

-- Create buckets via SQL (Supabase specific)
-- Note: This might fail if the user doesn't have permissions, but it's good to have it documented.
/*
INSERT INTO storage.buckets (id, name, public) 
VALUES ('disease-images', 'disease-images', true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO storage.buckets (id, name, public) 
VALUES ('avatars', 'avatars', true)
ON CONFLICT (id) DO NOTHING;

-- Storage Policies
CREATE POLICY "Users can upload disease images" ON storage.objects
    FOR INSERT WITH CHECK (bucket_id = 'disease-images' AND auth.role() = 'authenticated');

CREATE POLICY "Anyone can view disease images" ON storage.objects
    FOR SELECT USING (bucket_id = 'disease-images');

CREATE POLICY "Users can upload own avatar" ON storage.objects
    FOR INSERT WITH CHECK (bucket_id = 'avatars' AND auth.uid()::text = (storage.foldername(name))[1]);
*/

-- ============================================
-- 7. Sample Data
-- ============================================

INSERT INTO public.crop_encyclopedia (crop_name, scientific_name, category, optimal_temperature_min, optimal_temperature_max, water_requirements, soil_ph_min, soil_ph_max, days_to_maturity)
VALUES 
    ('Tomato', 'Solanum lycopersicum', 'Vegetable', 18, 27, 'medium', 6.0, 6.8, 75),
    ('Rice', 'Oryza sativa', 'Grain', 20, 35, 'high', 5.5, 6.5, 120),
    ('Wheat', 'Triticum aestivum', 'Grain', 12, 25, 'medium', 6.0, 7.0, 120),
    ('Corn', 'Zea mays', 'Grain', 18, 32, 'medium', 5.8, 7.0, 90),
    ('Potato', 'Solanum tuberosum', 'Vegetable', 15, 20, 'medium', 5.0, 6.0, 90),
    ('Sugarcane', 'Saccharum officinarum', 'Sugar', 20, 30, 'high', 6.0, 7.5, 365)
ON CONFLICT (crop_name) DO NOTHING;

-- ============================================
-- 8. Performance Indexes
-- ============================================

CREATE INDEX IF NOT EXISTS idx_disease_user ON public.disease_detections(user_id);
CREATE INDEX IF NOT EXISTS idx_soil_user ON public.soil_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_yield_user ON public.yield_predictions(user_id);
CREATE INDEX IF NOT EXISTS idx_market_user ON public.market_insights(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user_is_read ON public.notifications(user_id, is_read);
CREATE INDEX IF NOT EXISTS idx_chat_user_created ON public.chat_history(user_id, created_at DESC);

-- ============================================
-- End of Schema
-- ============================================
