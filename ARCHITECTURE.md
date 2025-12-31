# SmartFarmingAI Architecture

## System Architecture Diagram

```mermaid
graph TB
    subgraph "Frontend Layer"
        WEB[Web Application<br/>React/Next.js]
        MOBILE[Mobile App<br/>React Native/Flutter]
    end
    
    subgraph "API Layer - FastAPI"
        MAIN[main.py<br/>FastAPI App]
        HEALTH[/health]
        DISEASE[/api/predict-disease]
        SOIL[/api/soil-advice]
        IRRIGATION[/api/water-alert]
        YIELD[/api/yield-predict]
        MARKET[/api/market-insights]
    end
    
    subgraph "Service Layer"
        DS[Disease Service]
        SS[Soil Service]
        IS[Irrigation Service]
        YS[Yield Service]
        MS[Market Service]
        LLM[LLM Advisory Service]
    end
    
    subgraph "ML Models"
        CNN[Disease Detection<br/>ResNet18 CNN]
        RF[Yield Prediction<br/>Random Forest]
        GB[Soil Analysis<br/>Gradient Boosting]
    end
    
    subgraph "Data Processing"
        IMG[Image Preprocessor]
        SENSOR[Sensor Processor]
        TS[Time Series Processor]
    end
    
    subgraph "IoT Integration"
        IOT[IoT Handler]
        SOIL_SENSOR[Soil Sensors]
        WEATHER[Weather Sensors]
        IRRIG_SENSOR[Irrigation Sensors]
        CROP_SENSOR[Crop Monitors]
    end
    
    subgraph "Utilities"
        SEV[Severity Estimator]
        RISK[Risk Scorer]
        HELP[Helpers]
    end
    
    subgraph "External Services"
        OPENAI[OpenAI GPT-4]
        DB[(Database<br/>Future)]
    end
    
    WEB --> MAIN
    MOBILE --> MAIN
    
    MAIN --> HEALTH
    MAIN --> DISEASE
    MAIN --> SOIL
    MAIN --> IRRIGATION
    MAIN --> YIELD
    MAIN --> MARKET
    
    DISEASE --> DS
    SOIL --> SS
    IRRIGATION --> IS
    YIELD --> YS
    MARKET --> MS
    
    DS --> CNN
    DS --> IMG
    DS --> SEV
    DS --> LLM
    
    SS --> GB
    SS --> SENSOR
    SS --> RISK
    SS --> LLM
    
    IS --> SENSOR
    IS --> RISK
    IS --> LLM
    
    YS --> RF
    YS --> TS
    YS --> RISK
    YS --> LLM
    
    MS --> TS
    MS --> LLM
    
    LLM --> OPENAI
    
    IOT --> SOIL_SENSOR
    IOT --> WEATHER
    IOT --> IRRIG_SENSOR
    IOT --> CROP_SENSOR
    
    IOT --> SENSOR
    
    style MAIN fill:#4CAF50
    style LLM fill:#FF9800
    style CNN fill:#2196F3
    style RF fill:#2196F3
    style GB fill:#2196F3
    style OPENAI fill:#9C27B0
```

## Data Flow

### 1. Disease Detection Flow
```
User uploads image
    ↓
FastAPI endpoint (/api/predict-disease)
    ↓
Disease Service
    ↓
Image Preprocessor (resize, normalize)
    ↓
CNN Model (ResNet18)
    ↓
Severity Estimator (OpenCV analysis)
    ↓
LLM Advisory Service (treatment recommendations)
    ↓
JSON Response to user
```

### 2. Soil Health Flow
```
User submits soil data (NPK, pH)
    ↓
FastAPI endpoint (/api/soil-advice)
    ↓
Soil Service
    ↓
Sensor Processor (validation, cleaning)
    ↓
NPK Analysis + pH Assessment
    ↓
Fertilizer Calculations
    ↓
Risk Scorer
    ↓
LLM Advisory Service (improvement strategies)
    ↓
JSON Response to user
```

### 3. Irrigation Flow
```
User submits moisture/weather data
    ↓
FastAPI endpoint (/api/water-alert)
    ↓
Irrigation Service
    ↓
Calculate water requirements
    ↓
Assess urgency level
    ↓
Risk Scorer
    ↓
LLM Advisory Service (watering tips)
    ↓
JSON Response to user
```

### 4. Yield Prediction Flow
```
User submits crop/soil/weather data
    ↓
FastAPI endpoint (/api/yield-predict)
    ↓
Yield Service
    ↓
Feature Engineering
    ↓
Random Forest Model
    ↓
Quality Assessment
    ↓
Risk Scorer
    ↓
LLM Advisory Service (optimization tips)
    ↓
JSON Response to user
```

### 5. Market Insights Flow
```
User queries market data
    ↓
FastAPI endpoint (/api/market-insights)
    ↓
Market Service
    ↓
Price Forecasting Algorithm
    ↓
Trend Analysis
    ↓
Regional Comparison
    ↓
LLM Advisory Service (selling strategy)
    ↓
JSON Response to user
```

## Component Responsibilities

### API Routes
- Handle HTTP requests/responses
- Validate input data (Pydantic)
- Call appropriate services
- Format responses

### Services
- Business logic implementation
- Coordinate between models and utilities
- Data transformation
- Error handling

### ML Models
- Load trained models
- Perform predictions
- Return confidence scores
- Handle model-specific preprocessing

### Data Processing
- Image preprocessing
- Sensor data validation
- Time series analysis
- Feature engineering

### IoT Integration
- Receive sensor data
- Store historical readings
- Aggregate statistics
- Detect anomalies

### Utilities
- Severity estimation
- Risk scoring
- Helper functions
- Common operations

### LLM Advisory
- Generate natural language recommendations
- Context-aware advice
- Fallback to rule-based systems
- API integration management

## Technology Stack Summary

| Layer | Technologies |
|-------|-------------|
| **API Framework** | FastAPI, Uvicorn |
| **Deep Learning** | PyTorch, TorchVision |
| **Machine Learning** | Scikit-learn |
| **Computer Vision** | OpenCV |
| **Data Processing** | NumPy, Pandas |
| **Validation** | Pydantic |
| **AI Integration** | OpenAI GPT-4 |
| **Image Handling** | Pillow |
| **Visualization** | Matplotlib, Seaborn |

## Scalability Considerations

### Current Implementation
- Single server deployment
- In-memory IoT data storage
- Synchronous processing

### Future Enhancements
- Microservices architecture
- Database integration (PostgreSQL/MongoDB)
- Redis caching
- Message queue (RabbitMQ/Kafka)
- Containerization (Docker)
- Orchestration (Kubernetes)
- Load balancing
- Horizontal scaling

## Security Architecture

### Current
- Environment variable configuration
- Pydantic input validation
- CORS middleware

### Planned
- JWT authentication
- Role-based access control
- API rate limiting
- Request encryption
- Audit logging
- API key management
