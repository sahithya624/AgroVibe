import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FlaskConical, Loader2, Leaf, AlertCircle } from 'lucide-react';
import { soilApi } from '@/lib/api';

export default function SoilHealth() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [formData, setFormData] = useState({
    nitrogen: 280,
    phosphorus: 45,
    potassium: 220,
    ph: 6.5,
    crop: 'Tomato',
    field_size: 1.0
  });
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await soilApi.getAdvice({
        ...formData,
        crop_type: formData.crop,
        field_size: formData.field_size
      });
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze soil.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Soil Health & Advisory</h1>
        <p className="text-gray-500">Enter your soil test results to get AI-powered recommendations.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Form */}
        <div className="lg:col-span-1 bg-white p-6 rounded-xl border border-gray-200 shadow-sm h-fit">
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-xs flex items-center gap-2">
                <AlertCircle className="h-4 w-4" />
                {error}
              </div>
            )}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Crop Type</label>
              <select
                className="w-full rounded-lg border-gray-300 border p-2.5 focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
                value={formData.crop}
                onChange={e => setFormData({ ...formData, crop: e.target.value })}
              >
                <option>Tomato</option>
                <option>Potato</option>
                <option>Wheat</option>
                <option>Rice</option>
                <option>Corn</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Field Size (Hectares)</label>
              <input
                type="number"
                step="0.1"
                className="w-full rounded-lg border-gray-300 border p-2.5 outline-none focus:border-primary-500"
                value={formData.field_size}
                onChange={e => setFormData({ ...formData, field_size: Number(e.target.value) })}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nitrogen (N)</label>
                <input
                  type="number"
                  className="w-full rounded-lg border-gray-300 border p-2.5 outline-none focus:border-primary-500"
                  value={formData.nitrogen}
                  onChange={e => setFormData({ ...formData, nitrogen: Number(e.target.value) })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Phosphorus (P)</label>
                <input
                  type="number"
                  className="w-full rounded-lg border-gray-300 border p-2.5 outline-none focus:border-primary-500"
                  value={formData.phosphorus}
                  onChange={e => setFormData({ ...formData, phosphorus: Number(e.target.value) })}
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Potassium (K)</label>
                <input
                  type="number"
                  className="w-full rounded-lg border-gray-300 border p-2.5 outline-none focus:border-primary-500"
                  value={formData.potassium}
                  onChange={e => setFormData({ ...formData, potassium: Number(e.target.value) })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">pH Level</label>
                <input
                  type="number"
                  step="0.1"
                  className="w-full rounded-lg border-gray-300 border p-2.5 outline-none focus:border-primary-500"
                  value={formData.ph}
                  onChange={e => setFormData({ ...formData, ph: Number(e.target.value) })}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-primary-600 text-white rounded-xl font-medium hover:bg-primary-700 disabled:opacity-50 mt-4 flex items-center justify-center gap-2"
            >
              {loading ? <Loader2 className="animate-spin h-5 w-5" /> : 'Analyze Soil'}
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="lg:col-span-2">
          {result ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              {/* Score Card */}
              <div className="bg-gradient-to-br from-primary-900 to-primary-800 rounded-2xl p-8 text-white relative overflow-hidden">
                <div className="absolute top-0 right-0 p-32 bg-white/5 rounded-full -mr-16 -mt-16 blur-2xl"></div>
                <div className="relative z-10 flex items-center justify-between">
                  <div>
                    <h3 className="text-primary-100 font-medium mb-1">Overall Soil Health</h3>
                    <div className="text-5xl font-bold mb-2">{result.health_score}/100</div>
                    <div className="inline-block px-3 py-1 bg-white/20 rounded-full text-sm backdrop-blur-sm">
                      Status: {result.status}
                    </div>
                  </div>
                  <div className="h-24 w-24 rounded-full border-4 border-white/20 flex items-center justify-center">
                    <Leaf className="h-10 w-10 text-primary-200" />
                  </div>
                </div>
              </div>

              {/* Recommendations */}
              <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <FlaskConical className="h-5 w-5 text-primary-600" />
                  AI Recommendations
                </h3>
                <div className="space-y-3">
                  {result.recommendations.map((rec: any, i: number) => (
                    <div key={i} className="flex gap-3 p-4 bg-gray-50 rounded-lg border border-gray-100">
                      <div className="h-6 w-6 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center flex-shrink-0 text-xs font-bold">
                        {i + 1}
                      </div>
                      <div>
                        {typeof rec === 'string' ? (
                          <p className="text-gray-700 text-sm">{rec}</p>
                        ) : (
                          <div className="text-sm">
                            <span className="font-bold text-gray-900">{rec.nutrient || 'Nutrient'}: </span>
                            <span className="text-gray-700">Apply {rec.quantity_kg_per_ha} kg/ha ({rec.timing})</span>
                            {rec.description && <p className="text-gray-600 mt-1">{rec.description}</p>}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-gray-400 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200 min-h-[400px]">
              <FlaskConical className="h-12 w-12 mb-4 text-gray-300" />
              <p>Fill out the form to generate a soil health report</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
