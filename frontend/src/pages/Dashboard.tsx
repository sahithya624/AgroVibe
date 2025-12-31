import { motion } from 'framer-motion';
import { CloudSun, Droplets, Thermometer, Wind, TrendingUp } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { name: 'Mon', price: 2400 },
  { name: 'Tue', price: 1398 },
  { name: 'Wed', price: 9800 },
  { name: 'Thu', price: 3908 },
  { name: 'Fri', price: 4800 },
  { name: 'Sat', price: 3800 },
  { name: 'Sun', price: 4300 },
];

const StatCard = ({ title, value, subtext, icon: Icon, color }: any) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm"
  >
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-500">{title}</p>
        <h3 className="text-2xl font-bold mt-1 text-gray-900">{value}</h3>
        <p className="text-xs mt-1 text-gray-500">{subtext}</p>
      </div>
      <div className={`p-3 rounded-full ${color}`}>
        <Icon className="h-6 w-6 text-white" />
      </div>
    </div>
  </motion.div>
);

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-2xl font-bold text-gray-900">Farm Overview</h1>
        <p className="text-gray-500">Welcome back! Here's what's happening on your farm today.</p>
      </div>

      {/* Weather Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Temperature"
          value="28°C"
          subtext="Sunny, Humidity 65%"
          icon={Thermometer}
          color="bg-orange-500"
        />
        <StatCard
          title="Soil Moisture"
          value="45%"
          subtext="Optimal level"
          icon={Droplets}
          color="bg-blue-500"
        />
        <StatCard
          title="Wind Speed"
          value="12 km/h"
          subtext="North-East direction"
          icon={Wind}
          color="bg-gray-500"
        />
        <StatCard
          title="Next Rainfall"
          value="2 Days"
          subtext="Light showers expected"
          icon={CloudSun}
          color="bg-primary-500"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Market Trends Chart */}
        <div className="lg:col-span-2 bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="font-bold text-gray-900">Market Price Trends (Tomato)</h3>
            <span className="text-sm text-green-600 font-medium flex items-center gap-1">
              <TrendingUp className="h-4 w-4" /> +12.5%
            </span>
          </div>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data}>
                <defs>
                  <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.1} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#9ca3af' }} />
                <YAxis axisLine={false} tickLine={false} tick={{ fill: '#9ca3af' }} />
                <Tooltip />
                <Area type="monotone" dataKey="price" stroke="#10b981" fillOpacity={1} fill="url(#colorPrice)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Alerts Section */}
        <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
          <h3 className="font-bold text-gray-900 mb-4">Recent Alerts</h3>
          <div className="space-y-4">
            {[
              { title: "Irrigation Needed", desc: "Field B moisture low", type: "warning", time: "2h ago" },
              { title: "High Pest Risk", desc: "Conditions favorable for aphids", type: "danger", time: "5h ago" },
              { title: "Market Price Surge", desc: "Tomato prices up by 10%", type: "success", time: "1d ago" },
            ].map((alert, i) => (
              <div key={i} className="flex gap-3 items-start p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors">
                <div className={`mt-1 h-2 w-2 rounded-full ${alert.type === 'warning' ? 'bg-yellow-500' :
                  alert.type === 'danger' ? 'bg-red-500' : 'bg-green-500'
                  }`} />
                <div>
                  <h4 className="text-sm font-medium text-gray-900">{alert.title}</h4>
                  <p className="text-xs text-gray-500">{alert.desc}</p>
                  <span className="text-[10px] text-gray-400 mt-1 block">{alert.time}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
