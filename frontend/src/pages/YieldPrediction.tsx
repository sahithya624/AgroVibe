import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Sprout, Loader2, AlertCircle } from 'lucide-react';
import { yieldApi } from '@/lib/api';

import { SUPPORTED_CROPS } from '@/lib/constants';

export default function YieldPrediction() {
  const [formData, setFormData] = useState({
    crop_type: 'Wheat',
    field_size: 2.5,
    soil_quality: 75,
    avg_temperature: 25,
    total_rainfall: 500,
    fertilizer_used: 150,
    irrigation_frequency: 3
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await yieldApi.predict(formData);
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate yield prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900">AI Yield Prediction</h1>
        <p className="text-gray-500">Forecast your harvest quantity based on current conditions.</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-gray-100 bg-gray-50">
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm flex items-center gap-2">
              <AlertCircle className="h-4 w-4" />
              {error}
            </div>
          )}
          <form onSubmit={handlePredict} className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Crop</label>
              <select
                className="w-full rounded-lg border-gray-300 border p-2 text-sm"
                value={formData.crop_type}
                onChange={(e) => setFormData({ ...formData, crop_type: e.target.value })}
              >
                {SUPPORTED_CROPS.map(crop => (
                  <option key={crop} value={crop}>{crop}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold text-gray-500 uppercase mb-1">Area (Hectares)</label>
              <input
                type="number"
                step="0.1"
                className="w-full rounded-lg border-gray-300 border p-2 text-sm"
                placeholder="e.g. 2.5"
                value={formData.field_size}
                onChange={(e) => setFormData({ ...formData, field_size: parseFloat(e.target.value) })}
              />
            </div>
            <div className="flex items-end">
              <button
                type="submit"
                disabled={loading}
                className="w-full py-2 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 text-sm flex items-center justify-center gap-2"
              >
                {loading ? <Loader2 className="animate-spin h-4 w-4" /> : 'Calculate Yield'}
              </button>
            </div>
          </form>
        </div>

        <div className="p-8">
          {result ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center space-y-8"
            >
              <div>
                <p className="text-sm font-medium text-gray-500 mb-2">Estimated Yield</p>
                <div className="flex items-center justify-center gap-2 text-5xl font-bold text-primary-700">
                  {result.predicted_yield}
                  <span className="text-xl text-gray-400 font-normal self-end mb-2">{result.yield_unit}</span>
                </div>
                <div className="mt-4 inline-flex items-center gap-2 px-3 py-1 bg-green-50 text-green-700 rounded-full text-sm font-medium">
                  Quality Grade: {result.quality_grade}
                </div>
                <p className="text-xs text-gray-400 mt-2">
                  Confidence Score: {(result.confidence_score * 100).toFixed(0)}%
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-left">
                <div className="space-y-3">
                  <h3 className="font-bold text-gray-900 flex items-center gap-2">
                    <AlertCircle className="h-4 w-4 text-orange-500" />
                    Risk Factors
                  </h3>
                  <ul className="space-y-2">
                    {result.risk_factors.map((risk: string, i: number) => (
                      <li key={i} className="text-sm text-gray-600 pl-4 border-l-2 border-orange-200">{risk}</li>
                    ))}
                  </ul>
                </div>
                <div className="space-y-3">
                  <h3 className="font-bold text-gray-900 flex items-center gap-2">
                    <TrendingUp className="h-4 w-4 text-primary-500" />
                    Optimization
                  </h3>
                  <ul className="space-y-2">
                    {result.recommendations.map((rec: string, i: number) => (
                      <li key={i} className="text-sm text-gray-600 pl-4 border-l-2 border-primary-200">{rec}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {result.confidence_reasoning && (
                <div className="mt-8 p-4 bg-gray-50 rounded-xl text-left">
                  <p className="text-xs font-bold text-gray-400 uppercase mb-2">Analysis Context</p>
                  <p className="text-sm text-gray-600 italic">"{result.confidence_reasoning}"</p>
                </div>
              )}
            </motion.div>
          ) : (
            <div className="text-center py-12 text-gray-400">
              <Sprout className="h-12 w-12 mx-auto mb-3 text-gray-300" />
              <p>Enter details above to generate prediction</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
