import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../lib/authContext';
import { 
  CheckCircle2, 
  ChevronRight, 
  AlertCircle, 
  FileText, 
  Store, 
  Scale,
  Printer,
  ArrowLeft,
  Loader2,
  Search,
  Users,
  ArrowRight,
  Coins,
  ShieldCheck,
  ClipboardList,
  MessageSquare,
  Zap
} from 'lucide-react';

const LodgeComplaint = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();
  
  const [step, setStep] = useState(1); 
  const [cardNumber, setCardNumber] = useState('');
  const [headName, setHeadName] = useState('');
  const [issueType, setIssueType] = useState('');
  const [receivedQuantity, setReceivedQuantity] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [caseDetails, setCaseDetails] = useState(null);

  useEffect(() => {
    if (location.state && location.state.cardNumber) {
      setCardNumber(location.state.cardNumber);
      setHeadName(location.state.headName || '');
    }
  }, [location]);

  const handleSubmit = async () => {
    if (!receivedQuantity) {
      setError('Please enter the quantity actually received.');
      return;
    }
    
    setLoading(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      const caseNumber = `RS-RJ-${Math.floor(100000 + Math.random() * 900000)}`;
      setCaseDetails({ caseNumber });
      setStep(4);
    } catch (err) {
      setError('Submission failed. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  const steps = [
    { n: 1, label: 'Identify', icon: Search },
    { n: 2, label: 'Issue', icon: AlertCircle },
    { n: 3, label: 'Details', icon: Scale },
    { n: 4, label: 'Status', icon: CheckCircle2 },
  ];

  return (
    <div className="space-y-10 animate-fade-in-up">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="w-2 h-2 bg-rose-500 rounded-full animate-pulse"></span>
            <span className="text-[10px] font-black text-rose-600 uppercase tracking-[0.2em]">Grievance Intake System</span>
          </div>
          <h2 className="text-4xl font-black text-slate-900 tracking-tight">Record Grievance</h2>
          <p className="text-slate-400 font-medium mt-1">Formal registration of PDS distribution anomalies</p>
        </div>
        
        {/* Modern Stepper */}
        <div className="flex items-center gap-2 p-2 bg-white rounded-3xl border border-slate-100 shadow-glass">
          {steps.map((s, i) => (
            <React.Fragment key={s.n}>
              <div className={`flex items-center gap-2.5 px-4 py-2.5 rounded-2xl transition-all duration-500 ${
                step === s.n ? 'bg-brand-600 text-white shadow-lg shadow-brand-100' : 
                step > s.n ? 'bg-emerald-50 text-emerald-600' : 'text-slate-300'
              }`}>
                <div className={`w-6 h-6 rounded-lg flex items-center justify-center transition-colors ${
                  step === s.n ? 'bg-white/20' : step > s.n ? 'bg-emerald-100' : 'bg-slate-50'
                }`}>
                  {step > s.n ? <CheckCircle2 size={14} /> : <s.icon size={14} />}
                </div>
                <span className="text-xs font-black uppercase tracking-widest">{s.label}</span>
              </div>
              {i < steps.length - 1 && <div className="w-4 h-px bg-slate-100 mx-1"></div>}
            </React.Fragment>
          ))}
        </div>
      </div>

      <div className="max-w-4xl mx-auto">
        <div className="card border-none shadow-premium overflow-visible">
          {step === 1 && (
            <div className="p-10 space-y-10">
              <div className="space-y-6 text-center">
                 <div className="w-16 h-16 bg-brand-50 rounded-2xl flex items-center justify-center text-brand-600 mx-auto shadow-sm border border-brand-100">
                    <ClipboardList size={28} />
                 </div>
                 <div className="space-y-1">
                    <h3 className="text-2xl font-black text-slate-900 tracking-tight">Verify Beneficiary</h3>
                    <p className="text-sm text-slate-400 font-medium">Confirm the details before proceeding to record an issue</p>
                 </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <DetailBox label="Ration Card ID" value={cardNumber || 'Not Provided'} icon={FileText} />
                <DetailBox label="Household Head" value={headName || 'Not Provided'} icon={Users} />
              </div>

              {!cardNumber ? (
                <div className="p-8 bg-amber-50 rounded-[2rem] border border-amber-100 flex gap-5 items-center">
                  <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center text-amber-500 flex-shrink-0 shadow-sm">
                    <AlertCircle size={24} />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-black text-amber-900">Identification Required</p>
                    <p className="text-xs text-amber-700/80 mt-1 font-medium leading-relaxed">System requires a valid Ration Card ID to pull shop links and entitlements.</p>
                  </div>
                  <button onClick={() => navigate('/entitlement-check')} className="btn bg-amber-500 text-white hover:bg-amber-600 px-6 h-12 text-xs">
                    Find Beneficiary
                  </button>
                </div>
              ) : (
                <div className="flex gap-4 pt-6">
                  <button onClick={() => navigate('/entitlement-check')} className="btn btn-secondary flex-1 h-14 text-sm font-black uppercase tracking-widest">
                    Incorrect ID
                  </button>
                  <button onClick={() => setStep(2)} className="btn btn-primary flex-1 h-14 gap-3 text-sm font-black uppercase tracking-widest">
                    Confirm & Continue <ArrowRight size={20} />
                  </button>
                </div>
              )}
            </div>
          )}

          {step === 2 && (
            <div className="p-10 space-y-8">
              <div className="flex items-center gap-4 mb-4">
                <button onClick={() => setStep(1)} className="p-3 bg-slate-50 hover:bg-slate-100 rounded-xl transition-all text-slate-400 hover:text-slate-900 group">
                  <ArrowLeft size={20} className="group-hover:-translate-x-1 transition-transform" />
                </button>
                <div>
                  <h3 className="text-2xl font-black text-slate-900 tracking-tight">Select Category</h3>
                  <p className="text-xs text-slate-400 font-medium mt-0.5">Categorizing helps in faster resolution</p>
                </div>
              </div>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <IssueButton 
                  title="Short Supply" 
                  desc="Entitlement mismatch in distribution" 
                  icon={Scale} 
                  active={issueType === 'Short Supply'}
                  onClick={() => { setIssueType('Short Supply'); setStep(3); }} 
                />
                <IssueButton 
                  title="Quality Issue" 
                  desc="Food unfit for human consumption" 
                  icon={Zap} 
                  active={issueType === 'Quality Issue'}
                  onClick={() => { setIssueType('Quality Issue'); setStep(3); }} 
                />
                <IssueButton 
                  title="Price Fraud" 
                  desc="Charging more than MSP rates" 
                  icon={Coins} 
                  active={issueType === 'Overcharging'}
                  onClick={() => { setIssueType('Overcharging'); setStep(3); }} 
                />
                <IssueButton 
                  title="Shop Closed" 
                  desc="Dealer unavailable during working hours" 
                  icon={Store} 
                  active={issueType === 'Service Denial'}
                  onClick={() => { setIssueType('Service Denial'); setStep(3); }} 
                />
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="p-10 space-y-10">
              <div className="flex items-center gap-4">
                <button onClick={() => setStep(2)} className="p-3 bg-slate-50 hover:bg-slate-100 rounded-xl transition-all text-slate-400 hover:text-slate-900 group">
                  <ArrowLeft size={20} className="group-hover:-translate-x-1 transition-transform" />
                </button>
                <div>
                  <h3 className="text-2xl font-black text-slate-900 tracking-tight">Grievance Specifics</h3>
                  <p className="text-xs text-slate-400 font-medium mt-0.5">Provide detailed metrics for the investigation</p>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-10 items-center">
                 <div className="space-y-6">
                    <div className="p-8 bg-slate-50 rounded-[2.5rem] border border-slate-100 shadow-inner group">
                      <label className="label mb-4">Actual Quantity Received</label>
                      <div className="relative">
                        <input
                          type="number"
                          step="0.1"
                          value={receivedQuantity}
                          onChange={(e) => setReceivedQuantity(e.target.value)}
                          className="w-full bg-transparent border-none p-0 text-5xl font-black focus:ring-0 placeholder:text-slate-200 tracking-tighter"
                          placeholder="0.0"
                          autoFocus
                        />
                        <span className="absolute right-0 bottom-2 text-xl font-black text-slate-300">KG</span>
                      </div>
                      <div className="w-full h-1 bg-slate-200 mt-6 rounded-full overflow-hidden">
                        <div className="h-full bg-brand-600 transition-all duration-500" style={{ width: receivedQuantity ? `${Math.min(100, (parseFloat(receivedQuantity)/15)*100)}%` : '0%' }}></div>
                      </div>
                      <p className="mt-6 text-xs text-slate-400 font-medium italic">Benchmarked against system entitlement of 15.0 KG</p>
                    </div>
                 </div>

                 <div className="space-y-6">
                    <div className="p-8 bg-brand-50 rounded-[2.5rem] border border-brand-100 flex gap-5">
                       <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center text-brand-600 shadow-sm flex-shrink-0">
                          <ShieldCheck size={24} />
                       </div>
                       <div className="space-y-2">
                          <h4 className="font-black text-brand-900 tracking-tight">Evidence System</h4>
                          <p className="text-xs text-brand-700/70 font-medium leading-relaxed">
                            This data will be cross-referenced with FPS sale logs and weighing scale telemetry (if available).
                          </p>
                       </div>
                    </div>
                    <button
                      onClick={handleSubmit}
                      disabled={loading || !receivedQuantity}
                      className="btn btn-primary w-full h-16 text-base gap-3 shadow-brand-200 uppercase tracking-widest font-black"
                    >
                      {loading ? <Loader2 className="animate-spin" size={20} /> : <>Commit Record <MessageSquare size={20} /></>}
                    </button>
                 </div>
              </div>

              {error && (
                <div className="p-4 bg-rose-50 border border-rose-100 rounded-2xl text-rose-600 text-[13px] font-bold flex gap-3 animate-in slide-in-from-top-2">
                  <AlertCircle size={16} />
                  {error}
                </div>
              )}
            </div>
          )}

          {step === 4 && (
            <div className="p-16 text-center space-y-10 animate-fade-in">
              <div className="relative mx-auto w-32 h-32">
                <div className="absolute inset-0 bg-emerald-100 rounded-full animate-pulse opacity-50"></div>
                <div className="absolute inset-4 bg-emerald-500 text-white rounded-[2rem] flex items-center justify-center shadow-lg shadow-emerald-200">
                  <CheckCircle2 size={48} />
                </div>
              </div>
              
              <div className="space-y-2">
                <h2 className="text-4xl font-black text-slate-900 tracking-tight">Record Sealed</h2>
                <p className="text-slate-400 font-medium max-w-sm mx-auto">Grievance has been successfully transmitted to the Regional Vigilance Committee.</p>
              </div>

              <div className="bg-slate-50 border border-slate-100 rounded-[2.5rem] p-10 max-w-md mx-auto relative overflow-hidden group">
                <div className="absolute top-0 right-0 w-24 h-24 bg-brand-50 rounded-full -mr-12 -mt-12 opacity-50 transition-transform group-hover:scale-150 duration-700"></div>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.3em] mb-3">Master Case Reference</p>
                <p className="text-4xl font-black text-brand-600 tracking-tighter">{caseDetails.caseNumber}</p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4 max-w-lg mx-auto pt-6">
                <button onClick={() => window.print()} className="btn btn-secondary flex-1 h-14 gap-3 text-xs font-black uppercase tracking-widest">
                  <Printer size={20} /> Digital Copy
                </button>
                <button onClick={() => navigate('/home')} className="btn btn-primary flex-1 h-14 text-xs font-black uppercase tracking-widest">
                  Main Dashboard
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const DetailBox = ({ label, value, icon: Icon }) => (
  <div className="p-6 bg-slate-50/50 rounded-3xl border border-slate-100 flex items-center gap-5 transition-all hover:bg-white hover:border-brand-100 group">
    <div className="w-12 h-12 bg-white rounded-2xl border border-slate-100 text-slate-300 flex items-center justify-center shadow-sm group-hover:text-brand-600 group-hover:bg-brand-50 transition-colors">
      <Icon size={22} />
    </div>
    <div className="min-w-0">
      <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-0.5">{label}</p>
      <p className="font-bold text-slate-900 truncate tracking-tight">{value}</p>
    </div>
  </div>
);

const IssueButton = ({ title, desc, icon: Icon, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`p-8 rounded-[2.5rem] border-2 text-left transition-all duration-300 group relative overflow-hidden ${
      active ? 'border-brand-600 bg-brand-50' : 'border-slate-50 bg-white hover:border-brand-100 shadow-glass'
    }`}
  >
    <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mb-6 transition-all duration-500 ${
      active ? 'bg-brand-600 text-white rotate-6' : 'bg-slate-50 text-slate-300 group-hover:bg-brand-50 group-hover:text-brand-600 group-hover:rotate-6'
    }`}>
      <Icon size={28} />
    </div>
    <h4 className={`font-black text-xl tracking-tight ${active ? 'text-brand-900' : 'text-slate-900'}`}>{title}</h4>
    <p className={`text-xs mt-2 font-medium leading-relaxed ${active ? 'text-brand-700/70' : 'text-slate-400'}`}>{desc}</p>
    
    {active && (
      <div className="absolute top-8 right-8 text-brand-600">
        <CheckCircle2 size={24} />
      </div>
    )}
  </button>
);

export default LodgeComplaint;
