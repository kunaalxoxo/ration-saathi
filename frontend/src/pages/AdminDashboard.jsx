import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle, 
  ShieldAlert, 
  Users, 
  Map, 
  Download,
  Filter,
  ArrowUpRight,
  ShieldCheck,
  Zap,
  Activity,
  ChevronRight,
  Search,
  MoreVertical
} from 'lucide-react';

const AdminDashboard = () => {
  const { t } = useTranslation();

  const [stats] = useState([
    { label: 'District Risk', value: '42.5', trend: '+2.1%', icon: ShieldAlert, color: 'rose' },
    { label: 'Total Grievances', value: '1,284', trend: '+12%', icon: BarChart3, color: 'brand' },
    { label: 'Resolution Rate', value: '94.2%', trend: '-0.5%', icon: TrendingUp, color: 'emerald' },
    { label: 'Active Dealers', value: '482', trend: 'Stable', icon: Map, color: 'indigo' },
  ]);

  const highRiskFps = [
    { code: 'RJ-BA-001', name: 'Shri Ram FPS', complaints: 24, anomaly: 8.2, tier: 'Critical' },
    { code: 'RJ-BA-089', name: 'Maruti Nandan Stores', complaints: 18, anomaly: 6.5, tier: 'High' },
    { code: 'RJ-BA-112', name: 'Jai Bhawani Traders', complaints: 15, anomaly: 5.9, tier: 'High' },
    { code: 'RJ-BA-045', name: 'Kalyan Samiti FPS', complaints: 12, anomaly: 4.2, tier: 'Medium' },
  ];

  return (
    <div className="space-y-10 animate-fade-in-up">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="w-2 h-2 bg-brand-500 rounded-full animate-pulse"></span>
            <span className="text-[10px] font-black text-brand-600 uppercase tracking-[0.2em]">Administrative Command Center</span>
          </div>
          <h2 className="text-4xl font-black text-slate-900 tracking-tight">Admin Intelligence</h2>
          <p className="text-slate-400 font-medium mt-1">District-wide PDS performance and anomaly detection</p>
        </div>
        
        <div className="flex items-center gap-3">
          <button className="btn btn-secondary gap-2.5 h-12 px-5 text-xs font-black uppercase tracking-widest">
            <Filter size={18} className="text-brand-600" />
            <span>Filters</span>
          </button>
          <button className="btn btn-primary gap-2.5 h-12 px-5 text-xs font-black uppercase tracking-widest shadow-brand-200">
            <Download size={18} />
            <span>Export Intel</span>
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((s, i) => (
          <StatCard key={i} {...s} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
        {/* Priority Alerts */}
        <div className="lg:col-span-4 space-y-6">
          <div className="flex items-center justify-between px-2">
            <h3 className="font-black text-slate-900 text-sm uppercase tracking-widest flex items-center gap-2">
              <AlertTriangle size={18} className="text-rose-500" />
              Priority Alerts
            </h3>
            <span className="w-6 h-6 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center text-[10px] font-black">2</span>
          </div>
          
          <div className="space-y-4">
            <AlertBox 
              title="Supply Anomaly Detected" 
              desc="FPS RJ-BA-001 reported 40% higher transactions than monthly allocation."
              time="12 mins ago"
              type="critical"
            />
            <AlertBox 
              title="High Grievance Volume" 
              desc="Shyamgarh village cluster shows a 300% spike in 'Short Supply' reports."
              time="2 hours ago"
              type="warning"
            />
          </div>

          <div className="card bg-brand-900 border-none p-8 text-white relative overflow-hidden group mt-10">
            <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16 transition-transform group-hover:scale-150 duration-700"></div>
            <div className="relative z-10 space-y-6">
              <div>
                <h4 className="text-xl font-black">Vigilance Mode</h4>
                <p className="text-brand-200 text-xs mt-2 leading-relaxed font-medium">Auto-generate inspection orders for high-risk fair price shops.</p>
              </div>
              <button className="w-full py-3.5 bg-white text-brand-900 rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-lg shadow-black/20 hover:bg-brand-50 transition-colors flex items-center justify-center gap-2">
                <span>Deploy Audit Team</span>
                <ChevronRight size={14} />
              </button>
            </div>
          </div>
        </div>

        {/* FPS Risk Table */}
        <div className="lg:col-span-8">
          <div className="table-container border-none">
            <div className="card-header flex justify-between items-center">
              <div>
                <h3 className="font-black text-slate-900 text-lg">Dealers Risk Registry</h3>
                <p className="text-xs text-slate-400 font-medium mt-0.5">Real-time risk scoring based on citizen feedback</p>
              </div>
              <div className="relative group">
                <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-300 group-focus-within:text-brand-600 transition-colors" />
                <input type="text" placeholder="Search code..." className="pl-9 pr-4 py-2 bg-slate-50 border-none rounded-xl text-[11px] font-black uppercase tracking-widest outline-none focus:ring-2 focus:ring-brand-100 transition-all w-40" />
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr>
                    <th className="table-header">Dealer Identity</th>
                    <th className="table-header text-center">Complaints</th>
                    <th className="table-header">Risk Profile</th>
                    <th className="table-header">Category</th>
                    <th className="table-header"></th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-50">
                  {highRiskFps.map((f) => (
                    <tr key={f.code} className="group hover:bg-slate-50/50 transition-all cursor-pointer">
                      <td className="table-cell">
                        <span className="font-black text-slate-900 group-hover:text-brand-600 transition-colors">{f.name}</span>
                        <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest mt-0.5">{f.code}</p>
                      </td>
                      <td className="table-cell text-center">
                        <span className="font-black text-slate-900 text-base">{f.complaints}</span>
                      </td>
                      <td className="table-cell">
                        <div className="flex items-center gap-3">
                          <div className="flex-1 h-2 bg-slate-100 rounded-full max-w-[80px] overflow-hidden shadow-inner">
                            <div className={`h-full rounded-full transition-all duration-1000 ${
                              f.tier === 'Critical' ? 'bg-rose-500' : 
                              f.tier === 'High' ? 'bg-orange-500' : 'bg-amber-500'
                            }`} style={{ width: `${f.anomaly * 10}%` }}></div>
                          </div>
                          <span className="text-[11px] font-black text-slate-900 tracking-tight">{f.anomaly}</span>
                        </div>
                      </td>
                      <td className="table-cell">
                        <span className={`badge ${
                          f.tier === 'Critical' ? 'badge-red' : 
                          f.tier === 'High' ? 'badge-yellow' : 'badge-slate'
                        }`}>
                          {f.tier}
                        </span>
                      </td>
                      <td className="table-cell text-right">
                        <button className="p-2 text-slate-300 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-all">
                          <MoreVertical size={16} />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon: Icon, label, value, trend, color }) => {
  const colorMap = {
    brand: 'text-brand-600 bg-brand-50',
    rose: 'text-rose-600 bg-rose-50',
    emerald: 'text-emerald-600 bg-emerald-50',
    indigo: 'text-indigo-600 bg-indigo-50',
  };
  
  return (
    <div className="card p-7 flex flex-col justify-between group">
      <div className="flex justify-between items-start">
        <div className={`p-3.5 rounded-2xl ${colorMap[color]} transition-transform group-hover:scale-110 duration-300 shadow-sm border border-black/5`}>
          <Icon size={22} />
        </div>
        <div className={`flex items-center gap-1 text-[10px] font-black ${trend.startsWith('+') ? 'text-rose-600' : trend === 'Stable' ? 'text-slate-400' : 'text-emerald-600'} bg-white px-2.5 py-1 rounded-full border border-slate-100 shadow-sm`}>
          {trend}
          {trend.startsWith('+') ? <ArrowUpRight size={12} /> : null}
        </div>
      </div>
      <div className="mt-5">
        <p className="text-[11px] font-black text-slate-400 uppercase tracking-[0.15em] leading-none">{label}</p>
        <p className="text-3xl font-black text-slate-900 mt-2.5 tracking-tight">{value}</p>
      </div>
    </div>
  );
};

const AlertBox = ({ title, desc, time, type }) => {
  const styles = {
    critical: 'border-rose-100 bg-rose-50/50 text-rose-900',
    warning: 'border-orange-100 bg-orange-50/50 text-orange-900'
  };
  const iconColors = {
    critical: 'text-rose-600 bg-rose-100',
    warning: 'text-orange-600 bg-orange-100'
  };

  return (
    <div className={`p-6 rounded-[2rem] border ${styles[type]} space-y-3 relative overflow-hidden group transition-all hover:shadow-lg`}>
      <div className="flex justify-between items-start relative z-10">
        <div className="flex items-center gap-3">
           <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${iconColors[type]}`}>
              <ShieldAlert size={16} />
           </div>
           <h4 className="font-black text-xs uppercase tracking-tight">{title}</h4>
        </div>
        <span className="text-[9px] font-black opacity-40 uppercase tracking-widest">{time}</span>
      </div>
      <p className="text-[11px] font-medium leading-relaxed opacity-70 relative z-10 pl-11">{desc}</p>
      <div className={`absolute top-0 right-0 w-20 h-20 opacity-10 -translate-y-4 translate-x-4 transition-transform group-hover:scale-150 ${type === 'critical' ? 'bg-rose-600' : 'bg-orange-600'} rounded-full blur-2xl`}></div>
    </div>
  );
};

export default AdminDashboard;
