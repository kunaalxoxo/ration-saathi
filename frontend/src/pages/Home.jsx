import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/authContext';
import { 
  Users, 
  FileText, 
  CheckCircle2, 
  Clock, 
  ArrowRight,
  TrendingUp,
  AlertCircle,
  Search,
  Activity,
  Calendar,
  Zap,
  ChevronRight
} from 'lucide-react';

const Home = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [stats] = useState({
    totalCards: 1240,
    pendingCases: 8,
    resolvedCases: 156,
    avgDays: 2.4
  });

  const recentCases = [
    { id: 'RS-1024', card: 'RJ-BA-001', type: 'Short Supply', date: '2 hours ago', status: 'Pending', priority: 'High' },
    { id: 'RS-1023', card: 'RJ-BA-056', type: 'Quality Issue', date: '5 hours ago', status: 'Resolved', priority: 'Medium' },
    { id: 'RS-1022', card: 'RJ-BA-112', type: 'Denial', date: 'Yesterday', status: 'In Progress', priority: 'High' },
    { id: 'RS-1021', card: 'RJ-BA-098', type: 'Payment Error', date: '2 days ago', status: 'Resolved', priority: 'Low' },
  ];

  return (
    <div className="space-y-10 animate-fade-in-up">
      {/* Premium Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="w-2 h-2 bg-brand-500 rounded-full animate-ping"></span>
            <span className="text-[10px] font-black text-brand-600 uppercase tracking-[0.2em]">{t('home.operationalDashboard')}</span>
          </div>
          <h2 className="text-4xl font-black text-slate-900 tracking-tight">
            {t('home.welcome')}, <span className="gradient-text">{user?.name?.split(' ')[0] || 'Officer'}</span>
          </h2>
          <p className="text-slate-400 font-medium mt-1">{t('home.systemStatusOptimal')} <span className="text-slate-900 font-bold">{stats.pendingCases} {t('home.pendingCases')}</span> {t('home.toReview')}</p>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="px-5 py-3 glass-card rounded-2xl flex items-center gap-3 border-slate-100">
            <Calendar size={18} className="text-brand-600" />
            <div className="text-left">
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-none">{t('home.currentPeriod')}</p>
              <p className="text-sm font-bold text-slate-900 mt-1">March 2026</p>
            </div>
          </div>
          <button className="btn btn-primary shadow-brand-200 gap-2">
            <Zap size={18} />
            <span>{t('home.quickReport')}</span>
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard icon={Users} label="Beneficiaries" value={stats.totalCards.toLocaleString()} trend="+12.5%" color="brand" />
        <StatCard icon={Clock} label="Pending Review" value={stats.pendingCases} trend="-2.4%" color="amber" />
        <StatCard icon={CheckCircle2} label="Resolution Rate" value="94.2%" trend="+4.1%" color="emerald" />
        <StatCard icon={Activity} label="Avg. Response" value={`${stats.avgDays}h`} trend="-12min" color="indigo" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Main Content: Recent Cases */}
        <div className="lg:col-span-8 space-y-6">
          <div className="table-container border-none">
            <div className="card-header flex justify-between items-center">
              <div>
                <h3 className="font-black text-slate-900 text-lg">Live Case Feed</h3>
                <p className="text-xs text-slate-400 font-medium mt-0.5">Real-time grievance monitoring from your block</p>
              </div>
              <button onClick={() => navigate('/case-tracker')} className="btn btn-secondary px-4 py-2 text-xs rounded-xl">View Archive</button>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr>
                    <th className="table-header">Reference</th>
                    <th className="table-header">Beneficiary</th>
                    <th className="table-header">Issue Category</th>
                    <th className="table-header">Priority</th>
                    <th className="table-header">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-50">
                  {recentCases.map((c) => (
                    <tr key={c.id} className="group hover:bg-slate-50/50 transition-all cursor-pointer">
                      <td className="table-cell">
                        <span className="font-black text-slate-900">{c.id}</span>
                        <p className="text-[10px] text-slate-400 mt-0.5">{c.date}</p>
                      </td>
                      <td className="table-cell font-bold text-slate-700">{c.card}</td>
                      <td className="table-cell font-medium text-slate-600">{c.type}</td>
                      <td className="table-cell">
                        <span className={`text-[10px] font-black uppercase tracking-widest ${
                          c.priority === 'High' ? 'text-rose-500' : 
                          c.priority === 'Medium' ? 'text-amber-500' : 'text-emerald-500'
                        }`}>
                          {c.priority}
                        </span>
                      </td>
                      <td className="table-cell">
                        <span className={`badge ${
                          c.status === 'Resolved' ? 'badge-green' : 
                          c.status === 'Pending' ? 'badge-red' : 'badge-blue'
                        }`}>
                          {c.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Sidebar: Quick Actions & Intelligence */}
        <div className="lg:col-span-4 space-y-6">
          <div className="card bg-brand-900 border-none p-8 text-white relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16 transition-transform group-hover:scale-150 duration-700"></div>
            <div className="relative z-10 space-y-6">
              <div>
                <h4 className="text-xl font-black">AI Assistance</h4>
                <p className="text-brand-200 text-sm mt-1 leading-relaxed">Let our system help you prioritize and draft responses to grievances.</p>
              </div>
              <button className="w-full py-4 bg-white text-brand-900 rounded-2xl font-black text-xs uppercase tracking-widest shadow-lg shadow-black/20 hover:bg-brand-50 transition-colors flex items-center justify-center gap-2">
                <span>Open Copilot</span>
                <ChevronRight size={16} />
              </button>
            </div>
          </div>

          <div className="space-y-4">
             <h3 className="text-sm font-black text-slate-900 uppercase tracking-widest ml-1">System Core</h3>
             <ActionItem 
                icon={CheckCircle2} 
                title="Entitlement Engine" 
                desc="Verify monthly allocations" 
                onClick={() => navigate('/entitlement-check')}
                color="brand"
             />
             <ActionItem 
                icon={AlertCircle} 
                title="Grievance Intake" 
                desc="Record new citizen issue" 
                onClick={() => navigate('/lodge-complaint')}
                color="rose"
             />
             <ActionItem 
                icon={Search} 
                title="Advanced Lookup" 
                desc="Search global database" 
                onClick={() => navigate('/case-tracker')}
                color="slate"
             />
          </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon: Icon, label, value, trend, color }) => {
  const colorMap = {
    brand: 'text-brand-600 bg-brand-50',
    amber: 'text-amber-600 bg-amber-50',
    emerald: 'text-emerald-600 bg-emerald-50',
    indigo: 'text-indigo-600 bg-indigo-50',
    rose: 'text-rose-600 bg-rose-50',
  };
  
  return (
    <div className="card p-7 flex flex-col justify-between group">
      <div className="flex justify-between items-start">
        <div className={`p-3.5 rounded-2xl ${colorMap[color]} transition-transform group-hover:scale-110 duration-300`}>
          <Icon size={22} />
        </div>
        <div className={`flex items-center gap-1 text-[10px] font-black ${trend.startsWith('+') ? 'text-emerald-600' : 'text-rose-600'} bg-white px-2.5 py-1 rounded-full border border-slate-100 shadow-sm`}>
          <TrendingUp size={12} className={trend.startsWith('-') ? 'rotate-180' : ''} />
          {trend}
        </div>
      </div>
      <div className="mt-5">
        <p className="text-[11px] font-black text-slate-400 uppercase tracking-[0.15em] leading-none">{label}</p>
        <p className="text-3xl font-black text-slate-900 mt-2.5 tracking-tight">{value}</p>
      </div>
    </div>
  );
};

const ActionItem = ({ icon: Icon, title, desc, onClick, color }) => {
  const colorMap = {
    brand: 'text-brand-600 bg-brand-50',
    rose: 'text-rose-600 bg-rose-50',
    slate: 'text-slate-600 bg-slate-50',
  };

  return (
    <button 
      onClick={onClick}
      className="w-full card p-5 flex items-center gap-4 hover:border-brand-200 group transition-all text-left"
    >
      <div className={`p-3 rounded-xl ${colorMap[color]} transition-transform group-hover:scale-110`}>
        <Icon size={20} />
      </div>
      <div className="flex-1">
        <h4 className="font-bold text-slate-900 text-sm tracking-tight">{title}</h4>
        <p className="text-xs text-slate-400 font-medium">{desc}</p>
      </div>
      <ChevronRight size={16} className="text-slate-300 group-hover:text-brand-600 group-hover:translate-x-1 transition-all" />
    </button>
  );
};

export default Home;
