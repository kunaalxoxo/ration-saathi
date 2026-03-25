import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { 
  Search, 
  ClipboardCheck, 
  User, 
  Users, 
  Info, 
  Printer, 
  AlertTriangle, 
  Loader2, 
  ChevronRight,
  Database,
  ArrowRight,
  AlertCircle,
  ShoppingBag,
  History,
  ShieldCheck
} from 'lucide-react';

const EntitlementCheck = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  
  const [cardNumber, setCardNumber] = useState('');
  const [entitlementData, setEntitlementData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const handleCheckEntitlement = async () => {
    if (!cardNumber || cardNumber.length < 10) {
      setError('Please enter a valid 10-digit ration card number.');
      return;
    }
    
    setLoading(true);
    setError('');
    setEntitlementData(null);
    
    try {
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const dummyData = {
        cardNumber: cardNumber,
        headName: "Ram Kumar Yadav",
        members: 5,
        category: "PHH",
        fpsName: "Shri Ram Fair Price Shop (RJ-BA-001)",
        allocation: [
          { item: 'Wheat', amount: 5.0, unit: 'kg', color: 'brand' },
          { item: 'Rice', amount: 15.0, unit: 'kg', color: 'indigo' },
          { item: 'Sugar', amount: 1.0, unit: 'kg', color: 'amber' },
          { item: 'Kerosene', amount: 2.0, unit: 'L', color: 'slate' }
        ],
        month: "March 2026",
        lastTrans: "Feb 12, 2026"
      };
      
      setEntitlementData(dummyData);
    } catch (err) {
      setError('Failed to fetch entitlement details. Please check the network connection.');
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
            <span className="text-[10px] font-black text-brand-600 uppercase tracking-[0.2em]">PDS Verification Engine</span>
          </div>
          <h2 className="text-4xl font-black text-slate-900 tracking-tight">Beneficiary Lookup</h2>
          <p className="text-slate-400 font-medium mt-1">Verify citizen allocations and Fair Price Shop links</p>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="px-5 py-3 glass-card rounded-2xl flex items-center gap-3 border-slate-100">
            <Database size={18} className="text-brand-600" />
            <div className="text-left">
              <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-none">Database Status</p>
              <p className="text-sm font-bold text-slate-900 mt-1">Connected: ONORC Central</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
        {/* Search Panel */}
        <div className="lg:col-span-4 space-y-6">
          <div className="card p-8 border-none shadow-premium">
            <div className="mb-8">
              <h3 className="text-lg font-black text-slate-900 tracking-tight">Search Records</h3>
              <p className="text-xs text-slate-400 font-medium mt-1">Enter the beneficiary's unique ID</p>
            </div>
            
            <form onSubmit={(e) => { e.preventDefault(); handleCheckEntitlement(); }} className="space-y-6">
              <div>
                <label className="label">Ration Card ID</label>
                <div className="relative group">
                  <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-brand-600 transition-colors">
                    <ClipboardCheck size={20} />
                  </div>
                  <input
                    type="tel"
                    value={cardNumber}
                    onChange={(e) => setCardNumber(e.target.value.replace(/\D/g, ''))}
                    className="input pl-12 h-14 text-base font-black tracking-widest"
                    placeholder="0000000000"
                    maxLength="10"
                  />
                </div>
              </div>
              
              <button
                type="submit"
                disabled={loading || cardNumber.length !== 10}
                className="btn btn-primary w-full h-14 gap-3 text-base shadow-brand-200"
              >
                {loading ? <Loader2 className="animate-spin" size={20} /> : <>Search Database <ArrowRight size={20} /></>}
              </button>
            </form>

            {error && (
              <div className="mt-6 p-4 bg-rose-50 border border-rose-100 rounded-2xl text-rose-600 text-xs font-bold flex gap-3 animate-in slide-in-from-top-2">
                <AlertTriangle size={16} className="flex-shrink-0" />
                {error}
              </div>
            )}
          </div>

          <div className="p-8 bg-brand-900 rounded-[2.5rem] text-white relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-24 h-24 bg-white/10 rounded-full -mr-12 -mt-12 transition-transform group-hover:scale-150 duration-700"></div>
            <h4 className="font-black text-lg flex items-center gap-2 mb-3">
              <ShieldCheck size={20} className="text-brand-300" />
              Officer Note
            </h4>
            <p className="text-xs text-brand-100/80 leading-relaxed font-medium">
              Always request the physical card for verification. If the beneficiary reports a discrepancy, use the "Report Issue" action to initiate a formal grievance.
            </p>
          </div>
        </div>

        {/* Display Area */}
        <div className="lg:col-span-8">
          {!entitlementData && !loading && (
            <div className="h-[500px] border-2 border-dashed border-slate-200 rounded-[2.5rem] flex flex-col items-center justify-center text-center p-12 group transition-colors hover:border-brand-200">
              <div className="w-20 h-20 bg-slate-50 rounded-3xl flex items-center justify-center text-slate-300 mb-6 group-hover:text-brand-300 group-hover:bg-brand-50 transition-colors">
                <Database size={40} strokeWidth={1.5} />
              </div>
              <h3 className="text-xl font-black text-slate-900 tracking-tight">Awaiting Input</h3>
              <p className="text-slate-400 font-medium max-w-xs mt-2">Enter a 10-digit Ration Card ID to pull real-time data from the central servers.</p>
            </div>
          )}

          {loading && (
            <div className="h-[500px] card flex flex-col items-center justify-center space-y-6">
              <div className="relative">
                <div className="w-20 h-20 border-4 border-brand-50 rounded-full"></div>
                <div className="w-20 h-20 border-4 border-t-brand-600 rounded-full absolute top-0 left-0 animate-spin"></div>
                <Database size={32} className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-brand-600" />
              </div>
              <div className="text-center">
                <p className="text-lg font-black text-slate-900 tracking-tight">Syncing with Central DB</p>
                <p className="text-sm text-slate-400 font-medium">Authenticating via ONORC protocols...</p>
              </div>
            </div>
          )}

          {entitlementData && (
            <div className="space-y-8 animate-fade-in-up">
              <div className="card p-10 border-none shadow-premium relative overflow-hidden">
                <div className="absolute top-0 right-0 p-8">
                  <span className="badge badge-blue px-4 py-1.5 text-[11px] font-black">{entitlementData.category} Card</span>
                </div>
                
                <div className="flex flex-col md:flex-row gap-10">
                   <div className="flex-1 space-y-8">
                      <div>
                        <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1.5">Family Head</p>
                        <h3 className="text-3xl font-black text-slate-900 tracking-tight">{entitlementData.headName}</h3>
                      </div>

                      <div className="grid grid-cols-2 gap-8 pt-4">
                        <div className="space-y-1.5">
                          <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                             <Users size={12} className="text-brand-600" />
                             Reg. Members
                          </p>
                          <p className="text-lg font-black text-slate-900">{entitlementData.members} People</p>
                        </div>
                        <div className="space-y-1.5">
                          <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                             <History size={12} className="text-brand-600" />
                             Last Activity
                          </p>
                          <p className="text-lg font-black text-slate-900">{entitlementData.lastTrans}</p>
                        </div>
                      </div>
                   </div>

                   <div className="w-full md:w-[240px] p-6 bg-slate-50 rounded-3xl border border-slate-100 flex flex-col justify-between">
                      <div className="space-y-4">
                        <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center text-brand-600 shadow-sm">
                          <ShoppingBag size={20} />
                        </div>
                        <div>
                          <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-none">Linked FPS</p>
                          <p className="text-sm font-bold text-slate-900 mt-2 leading-tight">{entitlementData.fpsName}</p>
                        </div>
                      </div>
                      <button className="w-full py-3 mt-6 bg-white border border-slate-200 rounded-2xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-100 transition-colors">
                        View Shop Details
                      </button>
                   </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {entitlementData.allocation.map((item, idx) => (
                  <AllocationItem key={idx} {...item} />
                ))}
              </div>

              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <button
                  onClick={() => navigate('/lodge-complaint', { 
                    state: { 
                      cardNumber: entitlementData.cardNumber, 
                      headName: entitlementData.headName 
                    } 
                  })}
                  className="btn bg-rose-600 text-white hover:bg-rose-700 flex-1 h-14 gap-3 text-base shadow-lg shadow-rose-100"
                >
                  <AlertCircle size={22} />
                  <span>Report Anomaly</span>
                </button>
                <button
                  onClick={() => window.print()}
                  className="btn btn-secondary flex-1 h-14 gap-3 text-base"
                >
                  <Printer size={22} />
                  <span>Download Ledger</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const AllocationItem = ({ item, amount, unit, color }) => {
  const colors = {
    brand: 'text-brand-600 bg-brand-50 border-brand-100',
    indigo: 'text-indigo-600 bg-indigo-50 border-indigo-100',
    amber: 'text-amber-600 bg-amber-50 border-amber-100',
    slate: 'text-slate-600 bg-slate-50 border-slate-100',
  };

  return (
    <div className="card p-8 flex justify-between items-center group hover:border-brand-200 transition-all border-none shadow-glass">
      <div className="flex items-center gap-4">
        <div className={`w-12 h-12 rounded-2xl flex items-center justify-center font-black text-sm border ${colors[color]}`}>
          {item[0]}
        </div>
        <div>
          <h4 className="font-black text-slate-900 tracking-tight">{item}</h4>
          <p className="text-xs text-slate-400 font-medium">Monthly Quota</p>
        </div>
      </div>
      <div className="text-right">
        <span className="text-3xl font-black text-slate-900 tracking-tighter">{amount}</span>
        <span className="ml-1 text-[10px] font-black text-slate-400 uppercase tracking-widest">{unit}</span>
      </div>
    </div>
  );
};

export default EntitlementCheck;
