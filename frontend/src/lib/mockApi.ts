// Simulation of Backend Logic
export const simulateDelay = (ms = 1500) => new Promise(resolve => setTimeout(resolve, ms));

export const mockDiseaseAnalysis = async (_file: File) => {
  await simulateDelay(2000);
  return {
    disease_name: "Tomato Early Blight",
    confidence: 0.94,
    severity: "Moderate",
    affected_area: "15%",
    treatment: [
      "Remove affected leaves immediately.",
      "Apply copper-based fungicides.",
      "Ensure proper air circulation between plants.",
      "Avoid overhead watering to reduce moisture on leaves."
    ]
  };
};

export const mockSoilAnalysis = async (_data: any) => {
  await simulateDelay();
  const score = Math.floor(Math.random() * (95 - 60) + 60);
  return {
    health_score: score,
    status: score > 80 ? "Excellent" : score > 70 ? "Good" : "Needs Attention",
    recommendations: [
      "Nitrogen levels are slightly low; consider adding urea.",
      "pH is optimal for most vegetable crops.",
      "Organic matter content is good."
    ]
  };
};

export const mockYieldPrediction = async (_data: any) => {
  await simulateDelay();
  return {
    predicted_yield: 4.5, // tons per hectare
    unit: "tons/ha",
    confidence_interval: [4.2, 4.8],
    factors: {
      rainfall: "Positive Impact",
      soil_quality: "Neutral",
      temperature: "Positive Impact"
    }
  };
};

export const mockIrrigationAdvice = async (_data: any) => {
  await simulateDelay();
  return {
    status: "Watering Needed",
    urgency: "High",
    amount: "15mm",
    next_schedule: "Tomorrow Morning",
    reason: "Soil moisture is below 30% and temperature is high."
  };
};
