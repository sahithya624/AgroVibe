import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, AlertCircle, CheckCircle, Loader2, ScanLine, FlaskConical } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { diseaseApi } from '@/lib/api';

export default function DiseaseDetection() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [cropType, setCropType] = useState<string>('tomato');

  const cropOptions = [
    { value: 'tomato', label: 'Tomato' },
    { value: 'corn', label: 'Corn (Maize)' },
    { value: 'potato', label: 'Potato' },
    { value: 'pepper', label: 'Pepper (Bell)' },
    { value: 'grape', label: 'Grape' },
    { value: 'apple', label: 'Apple' },
    { value: 'strawberry', label: 'Strawberry' },
    { value: 'peach', label: 'Peach' },
    { value: 'rice', label: 'Rice' },
    { value: 'wheat', label: 'Wheat' }
  ];

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    setFile(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
    setError(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': [] },
    maxFiles: 1
  });

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const data = await diseaseApi.predict(file, cropType);

      // Normalize backend response to match frontend expectations
      const normalizedResult = {
        disease: data.disease_name || data.disease || 'Unknown Disease',
        confidence: data.confidence || 0,
        is_healthy: data.disease_name?.toLowerCase().includes('healthy') || false,
        urgency: data.severity || 'Medium',
        affected_area: data.affected_area || 'Unknown',
        treatment_plan: data.treatment || data.treatment_plan || [],
        preventive_measures: data.prevention || data.preventive_measures || []
      };

      setResult(normalizedResult);
    } catch (err: any) {
      console.error('Disease detection error details:', JSON.stringify(err, null, 2));
      let errorMessage = 'Failed to analyze plant image.';
      if (err.message === 'Network Error') {
        errorMessage = `Network Error: Unable to reach server at ${diseaseApi.getBaseUrl()}. Please check if backend is running.`;
      } else if (err.response) {
        errorMessage = `Server Error (${err.response.status}): ${err.response.data?.detail || err.message}`;
      } else {
        errorMessage = err.message || errorMessage;
      }
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-gray-900">AI Disease Detection</h1>
        <p className="text-gray-500">Upload a clear photo of the affected plant leaf for instant diagnosis.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Upload Section */}
        <div className="space-y-4">
          {/* Crop Type Selector */}
          <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Crop Type
            </label>
            <select
              value={cropType}
              onChange={(e) => setCropType(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-all"
            >
              {cropOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <p className="mt-2 text-xs text-gray-500">
              Select the crop you're analyzing for accurate disease detection
            </p>
          </div>

          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm flex items-center gap-2">
              <AlertCircle className="h-4 w-4" />
              {error}
            </div>
          )}
          {!preview ? (
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-2xl h-80 flex flex-col items-center justify-center cursor-pointer transition-colors ${isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
                }`}
            >
              <input {...getInputProps()} />
              <div className="p-4 bg-primary-100 rounded-full mb-4 text-primary-600">
                <Upload className="h-8 w-8" />
              </div>
              <p className="text-gray-900 font-medium">Click or drag image here</p>
              <p className="text-sm text-gray-500 mt-1">Supports JPG, PNG</p>
            </div>
          ) : (
            <div className="relative rounded-2xl overflow-hidden h-80 bg-gray-100 border border-gray-200">
              <img src={preview} alt="Preview" className="w-full h-full object-cover" />
              <button
                onClick={reset}
                className="absolute top-4 right-4 p-2 bg-white/90 rounded-full shadow-sm hover:bg-white text-gray-700"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
          )}

          <button
            onClick={handleAnalyze}
            disabled={!file || loading}
            className="w-full py-3 bg-primary-600 text-white rounded-xl font-medium hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
          >
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                Analyzing Plant...
              </>
            ) : (
              'Detect Disease'
            )}
          </button>
        </div>

        {/* Results Section */}
        <div className="relative">
          <AnimatePresence mode="wait">
            {result ? (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm h-full"
              >
                <div className="flex items-center gap-3 mb-6">
                  {result.is_healthy ? (
                    <CheckCircle className="h-8 w-8 text-green-500" />
                  ) : (
                    <AlertCircle className="h-8 w-8 text-red-500" />
                  )}
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{result.disease}</h3>
                    <p className="text-sm text-gray-500">Confidence: {(result.confidence * 100).toFixed(1)}%</p>
                  </div>
                </div>

                <div className="space-y-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div className={`p-4 rounded-xl ${result.is_healthy ? 'bg-green-50' : 'bg-red-50'}`}>
                      <p className={`text-xs font-bold uppercase ${result.is_healthy ? 'text-green-600' : 'text-red-600'}`}>
                        {result.is_healthy ? 'Status' : 'Urgency'}
                      </p>
                      <p className={`text-lg font-semibold ${result.is_healthy ? 'text-green-900' : 'text-red-900'}`}>
                        {result.is_healthy ? 'Healthy' : result.urgency}
                      </p>
                    </div>
                    {!result.is_healthy && (
                      <div className="p-4 bg-orange-50 rounded-xl">
                        <p className="text-xs text-orange-600 font-bold uppercase">Affected Area</p>
                        <p className="text-lg font-semibold text-orange-900">{result.affected_area}</p>
                      </div>
                    )}
                  </div>

                  <div>
                    <h4 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
                      {result.is_healthy ? (
                        <CheckCircle className="h-5 w-5 text-primary-600" />
                      ) : (
                        <FlaskConical className="h-5 w-5 text-primary-600" />
                      )}
                      {result.is_healthy ? 'Preventive Care' : 'Recommended Treatment'}
                    </h4>
                    <ul className="space-y-2">
                      {((result.is_healthy ? result.preventive_measures : result.treatment_plan) || []).map((step: string, i: number) => (
                        <li key={i} className="flex gap-3 text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
                          <span className="font-bold text-gray-400">{i + 1}.</span>
                          {step}
                        </li>
                      ))}
                      {(!result.treatment_plan || result.treatment_plan.length === 0) && !result.is_healthy && (
                        <li className="text-sm text-gray-500 italic">No specific treatment plan available.</li>
                      )}
                    </ul>
                  </div>
                </div>
              </motion.div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-gray-200 rounded-2xl text-gray-400">
                <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4">
                  <ScanLine className="h-8 w-8 text-gray-300" />
                </div>
                <p>Analysis results will appear here</p>
              </div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
