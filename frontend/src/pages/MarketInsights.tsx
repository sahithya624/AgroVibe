import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, IndianRupee, Loader2, AlertCircle } from 'lucide-react';
import { marketApi } from '@/lib/api';

import { SUPPORTED_CROPS } from '@/lib/constants';

export default function MarketInsights() {
  const [loading, setLoading] = useState(true);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [crop, setCrop] = useState('Tomato');

  const fetchInsights = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await marketApi.getInsights({
        crop_type: crop,
        region: 'Maharashtra', // Default region
        quantity: 1.0
      });
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch market insights.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInsights();
  }, [crop]);

  if (loading && !result) {
    return (
      <div className="h-[60vh] flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Market Insights</h1>
          <p className="text-gray-500">Real-time prices and future trends powered by AI.</p>
        </div>
        <div className="flex items-center gap-3">
          <select
            className="bg-white border border-gray-300 rounded-lg px-4 py-2 text-sm font-medium outline-none focus:ring-2 focus:ring-primary-500"
            value={crop}
            onChange={(e) => setCrop(e.target.value)}
          >
            {SUPPORTED_CROPS.map(c => (
              <option key={c} value={c}>{c}</option>
            ))}
          </select>
          <button
            onClick={fetchInsights}
            disabled={loading}
            className="p-2 text-gray-400 hover:text-primary-600 transition-colors"
          >
            <Loader2 className={`h-5 w-5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-600 flex items-center gap-3">
          <AlertCircle className="h-5 w-5" />
          {error}
        </div>
      )}

      {result && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
              <p className="text-sm text-gray-500">Current Avg Price</p>
              <div className="flex items-center gap-2 mt-1">
                <IndianRupee className="h-5 w-5 text-gray-400" />
                <span className="text-3xl font-bold text-gray-900">
                  {result.current_price?.toLocaleString()}
                </span>
                <span className="text-xs text-gray-500">/ quintal</span>
              </div>
              <div className={`mt-4 flex items-center gap-1 text-sm font-medium w-fit px-2 py-1 rounded ${result.trend === 'up' ? 'text-green-600 bg-green-50' : 'text-red-600 bg-red-50'
                }`}>
                {result.trend === 'up' ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
                {result.percent_change > 0 ? '+' : ''}{result.percent_change}% this week
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
              <p className="text-sm text-gray-500">Best Recommended Market</p>
              <h3 className="text-xl font-bold text-gray-900 mt-1">{result.best_market}</h3>
              <p className="text-sm text-gray-500 mt-1">Status: Active</p>
              <div className="mt-4 text-sm text-primary-600 font-medium cursor-pointer hover:underline">
                View Price Details &rarr;
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
              <p className="text-sm text-gray-500">AI Price Forecast</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-2xl font-bold text-gray-900">{result.forecast}</span>
              </div>
              <p className="text-xs text-gray-500 mt-2 line-clamp-2">{result.recommendation}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm h-[400px]">
              <h3 className="font-bold text-gray-900 mb-6">Price Trend (Last 30 Days)</h3>
              <ResponsiveContainer width="100%" height="85%">
                <LineChart data={result.historical_data || []}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                  <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{ fill: '#9ca3af' }} />
                  <YAxis axisLine={false} tickLine={false} tick={{ fill: '#9ca3af' }} />
                  <Tooltip
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Line
                    type="monotone"
                    dataKey="price"
                    stroke={result.trend === 'up' ? '#10b981' : '#ef4444'}
                    strokeWidth={3}
                    dot={{ fill: result.trend === 'up' ? '#10b981' : '#ef4444', strokeWidth: 2 }}
                    activeDot={{ r: 8 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm h-[400px]">
              <div className="mb-6">
                <h3 className="font-bold text-gray-900">AI Risk Analysis</h3>
                <p className="text-sm text-gray-500">Identified factors affecting future prices.</p>
              </div>
              <div className="space-y-4">
                {(result.risk_factors || []).map((risk: string, i: number) => (
                  <div key={i} className="flex gap-3 items-start p-3 bg-gray-50 rounded-lg">
                    <div className="w-2 h-2 rounded-full bg-orange-400 mt-1.5 flex-shrink-0" />
                    <p className="text-sm text-gray-700">{risk}</p>
                  </div>
                ))}
                {(!result.risk_factors || result.risk_factors.length === 0) && (
                  <p className="text-center text-gray-400 py-12">No major risks identified at this time.</p>
                )}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
