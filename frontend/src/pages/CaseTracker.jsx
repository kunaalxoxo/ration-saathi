import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { 
  Search, 
  History, 
  Calendar, 
  MapPin, 
  Loader2, 
  ChevronRight,
  Clock,
  CheckCircle2,
  AlertCircle,
  Database,
  ArrowRight,
  ShieldCheck,
  User,
  Zap
} from 'lucide-react';

const CaseTracker = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  
  const [caseNumber, setCaseNumber] = useState('');
  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTrackCase = async () => {
    if (!caseNumber) {
      setError('Please enter a case number.');
      return;
    }
    
    setLoading(true);
    setError('');
    setCaseData(null);
    
    try {
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const dummyCase = {
        caseNumber: caseNumber,
        status: 'under_investigation',
        issueType: 'Short Supply',
        dateReported: '15 Oct 2025',
        lastUpdate: '18 Oct 2025',
        location: 'Shyamgarh Village, Block 001',
        beneficiary: 'Ram Kumar (RJ-BA-001)',
        updates: [
          { date: '18 Oct 2025', time: '10:30 AM', text: 'Block Officer Vikash Singh assigned to field investigation.', status: 'current', icon: ShieldCheck },
          { date: '16 Oct 2025', time: '02:15 PM', text: 'Grievance acknowledged. Preliminary data verified with EPDS.', status: 'past', icon: Database },
          { date: '15 Oct 2025', time: '09:00 AM', text: 'Case registered via CSC Portal.', status: 'past', icon: CheckCircle2 }
        ]
      };
      
      setCaseData(dummyCase);
    } catch (err) {
      setError('Could not find case details. Please check the reference number.');
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
            <span className="text-[10px] font-black text-brand-600 uppercase tracking-[0.2em]">Real-time Status Engine</span>
          </div>
          <h2 className="text-4xl font-black text-slate-900 tracking-tight">Case Monitoring</h2>
          <p className="text-slate-400 font-medium mt-1">Track the resolution lifecycle of submitted grievances</p>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="px-5 py-3 glass-card rounded-2xl flex items-center gap-3 border-slate-100">
            <Zap size={18} className="text-brand-600" />
            <div className="text-left">
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-none">Response SLA</p>
              <p className="text-sm font-bold text-slate-900 mt-1">48h Resolution Target</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
        {/* Search Sidebar */}
        <div className="lg:col-span-4 space-y-6">
          <div className="card p-8 border-none shadow-premium">
            <div className="mb-8">
              <h3 className="text-lg font-black text-slate-900 tracking-tight">Track Reference</h3>
              <p className="text-xs text-slate-400 font-medium mt-1">Enter your unique grievance ID</p>
            </div>
            
            <div className="space-y-6">
              <div>
                <label className="label">Reference ID</label>
                <div className="relative group">
                  <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-brand-600 transition-colors">
                    <Search size={20} />
                  </div>
                  <input
                    type="text"
                    value={caseNumber}
                    onChange={(e) => setCaseNumber(e.target.value.toUpperCase())}
                    className="input pl-12 h-14 text-base font-black tracking-widest uppercase"
                    placeholder="RS-RJ-XXXXXX"
                  />
                </div>
              </div>
              
              <button
                onClick={handleTrackCase}
                disabled={loading || !caseNumber}
                className="btn btn-primary w-full h-14 gap-3 text-base shadow-brand-200"
              >
                {loading ? <Loader2 className="animate-spin" size={20} /> : <>Sync Status <ArrowRight size={20} /></>}
              </button>
            </div>

            {error && (
              <div className="mt-6 p-4 bg-rose-50 border border-rose-100 rounded-2xl text-rose-600 text-[13px] font-bold flex gap-3 animate-in slide-in-from-top-2">
                <AlertCircle size={16} />
                {error}
              </div>
            )}
          </div>

          <div className="card overflow-hidden border-none shadow-premium">
            <div className="p-6 bg-slate-50 border-b border-slate-100 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <History size={16} className="text-brand-600" />
                <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Recent Checks</span>
              </div>
            </div>
            <div className="divide-y divide-slate-50">
              {['RS-RJ-102405', 'RS-RJ-992834'].map((h) => (
                <button key={h} onClick={() => { setCaseNumber(h); handleTrackCase(); }} className="w-full px-6 py-4 text-left hover:bg-slate-50 transition-all flex justify-between items-center group">
                  <span className="text-sm font-black text-slate-600 group-hover:text-brand-600 tracking-tight transition-colors">{h}</span>
                  <div className="w-8 h-8 rounded-lg bg-white border border-slate-100 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all">
                    <ChevronRight size={14} className="text-brand-600" />
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Tracking Details */}
        <div className="lg:col-span-8">
          {!caseData && !loading && (
            <div className="h-[500px] border-2 border-dashed border-slate-200 rounded-[2.5rem] flex flex-col items-center justify-center text-center p-12 group transition-colors hover:border-brand-200">
              <div className="w-20 h-20 bg-slate-50 rounded-3xl flex items-center justify-center text-slate-300 mb-6 group-hover:text-brand-300 group-hover:bg-brand-50 transition-colors">
                <History size={40} strokeWidth={1.5} />
              </div>
              <h3 className="text-xl font-black text-slate-900 tracking-tight">Identity Required</h3>
              <p className="text-slate-400 font-medium max-w-xs mt-2">Enter your case reference ID to pull the latest investigation updates.</p>
            </div>
          )}

          {loading && (
            <div className="h-[500px] card flex flex-col items-center justify-center space-y-6">
              <div className="relative">
                <div className="w-20 h-20 border-4 border-brand-50 rounded-full"></div>
                <div className="w-20 h-20 border-4 border-t-brand-600 rounded-full absolute top-0 left-0 animate-spin"></div>
                <Search size={32} className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-brand-600" />
              </div>
              <div className="text-center">
                <p className="text-lg font-black text-slate-900 tracking-tight">Retrieving Record</p>
                <p className="text-sm text-slate-400 font-medium tracking-wide">Scanning decentralized village nodes...</p>
              </div>
            </div>
          )}

          {caseData && (
            <div className="space-y-8 animate-fade-in-up">
              {/* Case Header Card */}
              <div className="card p-10 border-none shadow-premium relative overflow-hidden group">
                <div className="absolute top-0 right-0 w-32 h-32 bg-brand-50 rounded-full -mr-16 -mt-16 opacity-50 transition-transform group-hover:scale-110 duration-700"></div>
                
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-8 relative z-10">
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <span className="badge badge-blue px-3 py-1 font-black text-[10px] uppercase">Official Record</span>
                      <p className="text-xs font-black text-slate-400 uppercase tracking-widest">{caseData.dateReported}</p>
                    </div>
                    <h3 className="text-4xl font-black text-slate-900 tracking-tighter">{caseData.caseNumber}</h3>
                  </div>
                  
                  <div className="flex items-center gap-6 p-4 bg-white rounded-3xl border border-slate-50 shadow-sm">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-2xl bg-orange-100 flex items-center justify-center text-orange-600">
                        <Clock size={20} />
                      </div>
                      <div>
                        <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-none">Status</p>
                        <p className="text-sm font-bold text-slate-900 mt-1 uppercase tracking-tight">{caseData.status.replace('_', ' ')}</p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-10 mt-10 pt-10 border-t border-slate-50 relative z-10">
                  <InfoItem icon={AlertCircle} label="Issue Category" value={caseData.issueType} />
                  <InfoItem icon={MapPin} label="Origin Point" value={caseData.location} />
                  <InfoItem icon={User} label="Beneficiary" value={caseData.beneficiary.split(' ')[0]} />
                </div>
              </div>

              {/* Progress Timeline */}
              <div className="card p-10 border-none shadow-premium">
                <div className="flex items-center justify-between mb-12">
                   <h4 className="text-xl font-black text-slate-900 tracking-tight">Audit Trail</h4>
                   <div className="px-4 py-1.5 bg-brand-50 rounded-full text-[10px] font-black text-brand-600 uppercase tracking-widest">
                     Live Updates
                   </div>
                </div>
                
                <div className="space-y-12 relative ml-4">
                  <div className="absolute left-[23px] top-4 bottom-4 w-1 bg-slate-50 rounded-full"></div>
                  
                  {caseData.updates.map((update, idx) => (
                    <div key={idx} className="relative flex gap-10 group">
                      <div className={`w-12 h-12 rounded-2xl border-4 border-white shadow-premium flex-shrink-0 z-10 flex items-center justify-center transition-all duration-500 ${
                        update.status === 'current' ? 'bg-brand-600 text-white scale-110 shadow-brand-100' : 'bg-slate-100 text-slate-400 group-hover:bg-brand-50 group-hover:text-brand-400'
                      }`}>
                        <update.icon size={20} />
                      </div>
                      <div className="pt-1.5 flex-1">
                        <div className="flex items-center gap-3 mb-2">
                           <p className={`text-[10px] font-black uppercase tracking-[0.2em] ${
                             update.status === 'current' ? 'text-brand-600' : 'text-slate-300'
                           }`}>{update.date}</p>
                           <span className="w-1 h-1 bg-slate-200 rounded-full"></span>
                           <p className="text-[10px] font-black text-slate-300 uppercase tracking-widest">{update.time}</p>
                        </div>
                        <p className={`text-base leading-relaxed tracking-tight ${
                          update.status === 'current' ? 'text-slate-900 font-black' : 'text-slate-500 font-medium'
                        }`}>{update.text}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const InfoItem = ({ icon: Icon, label, value }) => (
  <div className="space-y-2">
    <div className="flex items-center gap-2 text-[10px] font-black text-slate-400 uppercase tracking-[0.15em]">
      <Icon size={12} className="text-brand-600" />
      <span>{label}</span>
    </div>
    <p className="text-base font-black text-slate-900 tracking-tight">{value}</p>
  </div>
);

export default CaseTracker;
