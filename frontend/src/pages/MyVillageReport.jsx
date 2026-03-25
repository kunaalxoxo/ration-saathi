import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/authContext';
import { 
  BarChart3, 
  MapPin, 
  Users, 
  CheckCircle2, 
  AlertCircle, 
  ArrowLeft,
  Loader2,
  TrendingUp,
  Activity,
  ChevronRight,
  Download,
  Calendar
} from 'lucide-react';

const MyVillageReport = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  useEffect(() => {
    fetchReport();
  }, []);
  
  const fetchReport = async () => {
    setLoading(true);
    setError('');
    try {
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const dummyData = {
        villageName: "Shyamgarh",
        totalRationCards: 120,
        activeCards: 110,
        totalCasesThisMonth: 8,
        resolvedCases: 5,
        pendingCases: 3,
        fpsPerformance: [
          { fpsCode: 'RJ-BA-001', name: 'Shri Ram FPS', complaints: 2, resolutionRate: 80, trend: 'Up' },
          { fpsCode: 'RJ-BA-002', name: 'Krishna FPS', complaints: 0, resolutionRate: 100, trend: 'Stable' },
          { fpsCode: 'RJ-BA-003', name: 'Shiv Shakti FPS', complaints: 4, resolutionRate: 60, trend: 'Down' }
        ]
      };
      
      setReportData(dummyData);
    } catch (err) {
      setError('Failed to load village report.');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="space-y-10 animate-fade-in-up">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="w-2 h-2 bg-brand-500 rounded-full animate-pulse"></span>
            <span className="text-[10px] font-black text-brand-600 uppercase tracking-[0.2em]">Village Analytics Engine</span>
          </div>
          <h2 className="text-4xl font-black text-slate-900 tracking-tight">Village Intelligence</h2>
          <p className="text-slate-400 font-medium mt-1">Granular performance metrics for <span className="text-slate-900 font-bold">{reportData?.villageName || 'your village'}</span></p>
        </div>
        
        <div className="flex items-center gap-3">
          <button className="btn btn-secondary gap-2.5 h-12 px-5 text-xs font-black uppercase tracking-widest">
            <Download size={18} className="text-brand-600" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {loading && (
        <div className="h-[400px] flex flex-col items-center justify-center space-y-6">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-brand-50 rounded-full"></div>
            <div className="w-16 h-16 border-4 border-t-brand-600 rounded-full absolute top-0 left-0 animate-spin"></div>
            <Activity size={24} className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-brand-600" />
          </div>
          <p className="text-sm font-black text-slate-400 uppercase tracking-widest">Aggregating Local Data...</p>
        </div>
      )}

      {error && (
        <div className="p-8 bg-rose-50 border border-rose-100 rounded-[2.5rem] text-rose-600 text-center max-w-lg mx-auto">
          <AlertCircle size={40} className="mx-auto mb-4 opacity-50" />
          <p className="font-black text-lg tracking-tight mb-2">Data Sync Failed</p>
          <p className="text-sm font-medium opacity-70 mb-6">{error}</p>
          <button onClick={fetchReport} className="btn bg-rose-600 text-white hover:bg-rose-700 px-8">Retry Sync</button>
        </div>
      )}
        
      {reportData && !loading && (
        <div className="space-y-10">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard icon={Users} label="Reg. Households" value={reportData.totalRationCards} color="brand" />
            <StatCard icon={CheckCircle2} label="Active Status" value={reportData.activeCards} color="emerald" />
            <StatCard icon={AlertCircle} label="Monthly Issues" value={reportData.totalCasesThisMonth} color="rose" />
            <StatCard icon={TrendingUp} label="Resolved Intel" value={reportData.resolvedCases} color="indigo" />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
            <div className="lg:col-span-8">
              <div className="table-container border-none shadow-premium">
                <div className="card-header flex justify-between items-center">
                  <div>
                    <h3 className="font-black text-slate-900 text-lg">FPS Quality Index</h3>
                    <p className="text-xs text-slate-400 font-medium mt-0.5">Dealer performance breakdown for this cluster</p>
                  </div>
                  <div className="flex items-center gap-2 px-4 py-2 bg-slate-50 rounded-xl border border-slate-100">
                    <Calendar size={14} className="text-brand-600" />
                    <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">March 2026</span>
                  </div>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-left border-collapse">
                    <thead>
                      <tr>
                        <th className="table-header">Dealer Identity</th>
                        <th className="table-header text-center">Issues</th>
                        <th className="table-header">Resolution Rate</th>
                        <th className="table-header">Trend</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-50">
                      {reportData.fpsPerformance.map((fps) => (
                        <tr key={fps.fpsCode} className="group hover:bg-slate-50/50 transition-all cursor-pointer">
                          <td className="table-cell">
                            <span className="font-black text-slate-900 group-hover:text-brand-600 transition-colors">{fps.name}</span>
                            <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest mt-0.5">{fps.fpsCode}</p>
                          </td>
                          <td className="table-cell text-center">
                            <span className="font-black text-slate-900 text-base">{fps.complaints}</span>
                          </td>
                          <td className="table-cell">
                            <div className="flex items-center gap-4">
                              <div className="flex-1 h-2 bg-slate-100 rounded-full max-w-[100px] overflow-hidden">
                                <div className={`h-full rounded-full transition-all duration-1000 ${
                                  fps.resolutionRate >= 80 ? 'bg-emerald-500' : 'bg-orange-500'
                                }`} style={{ width: `${fps.resolutionRate}%` }}></div>
                              </div>
                              <span className="text-[11px] font-black text-slate-900">{fps.resolutionRate}%</span>
                            </div>
                          </td>
                          <td className="table-cell">
                             <div className={`flex items-center gap-1.5 text-[10px] font-black uppercase tracking-widest ${
                               fps.trend === 'Up' ? 'text-emerald-600' : 
                               fps.trend === 'Down' ? 'text-rose-600' : 'text-slate-400'
                             }`}>
                               {fps.trend}
                               {fps.trend === 'Up' && <TrendingUp size={12} />}
                               {fps.trend === 'Down' && <Activity size={12} className="rotate-180" />}
                             </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <div className="lg:col-span-4 space-y-6">
               <div className="card p-8 border-none shadow-premium bg-slate-900 text-white relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-brand-500 rounded-full -mr-16 -mt-16 opacity-20"></div>
                  <h4 className="text-xl font-black mb-4">Village Health Score</h4>
                  <div className="flex items-end gap-3 mb-6">
                    <span className="text-6xl font-black tracking-tighter">92</span>
                    <span className="text-brand-400 font-black text-sm uppercase tracking-widest mb-3">/ 100</span>
                  </div>
                  <p className="text-slate-400 text-xs font-medium leading-relaxed">
                    Based on resolution time, stock availability, and citizen satisfaction surveys in Shyamgarh.
                  </p>
                  <div className="w-full h-1 bg-white/10 mt-8 rounded-full overflow-hidden">
                    <div className="h-full bg-brand-500" style={{ width: '92%' }}></div>
                  </div>
               </div>

               <div className="card p-8 border-none shadow-premium space-y-6">
                  <h4 className="text-sm font-black text-slate-900 uppercase tracking-widest flex items-center gap-2">
                    <MapPin size={16} className="text-brand-600" />
                    Village Map Link
                  </h4>
                  <div className="aspect-video bg-slate-100 rounded-2xl overflow-hidden relative group cursor-pointer">
                    <img src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80" alt="map" className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                    <div className="absolute inset-0 bg-brand-900/10 group-hover:bg-brand-900/0 transition-colors"></div>
                    <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                      <div className="px-4 py-2 bg-white rounded-xl text-[10px] font-black uppercase tracking-widest text-slate-900 shadow-xl">Open Full Map</div>
                    </div>
                  </div>
               </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const StatCard = ({ icon: Icon, label, value, color }) => {
  const colorMap = {
    brand: 'text-brand-600 bg-brand-50',
    rose: 'text-rose-600 bg-rose-50',
    emerald: 'text-emerald-600 bg-emerald-50',
    indigo: 'text-indigo-600 bg-indigo-50',
  };
  
  return (
    <div className="card p-7 flex flex-col justify-between group">
      <div className={`w-12 h-12 rounded-2xl ${colorMap[color]} transition-transform group-hover:scale-110 duration-300 shadow-sm border border-black/5 flex items-center justify-center`}>
        <Icon size={22} />
      </div>
      <div className="mt-5">
        <p className="text-[11px] font-black text-slate-400 uppercase tracking-[0.15em] leading-none">{label}</p>
        <p className="text-3xl font-black text-slate-900 mt-2.5 tracking-tight">{value}</p>
      </div>
    </div>
  );
};

export default MyVillageReport;
