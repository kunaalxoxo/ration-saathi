import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/authContext';
import { ShieldCheck, Phone, ArrowRight, Loader2, Landmark, CheckCircle2, Globe, Lock } from 'lucide-react';

const Login = () => {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const { login } = useAuth();
  
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState(1); 
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGetOtp = async () => {
    setLoading(true);
    setError('');
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      setStep(2);
    } catch (err) {
      setError('Failed to send OTP. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async () => {
    setLoading(true);
    setError('');
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      login({
        id: '1',
        name: 'Vikram Singh',
        phone: phoneNumber,
        role: 'csc_operator',
        district_code: 'RJ-BA',
        block_code: 'RJ-BA-001'
      });
      navigate('/home');
    } catch (err) {
      setError('Invalid OTP. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const toggleLanguage = () => {
    const nextLng = i18n.language === 'hi' ? 'en' : 'hi';
    i18n.changeLanguage(nextLng);
  };

  return (
    <div className="min-h-screen bg-gov-ash flex items-center justify-center p-6 relative overflow-hidden font-sans">
      {/* Dynamic Background */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-[-10%] right-[-10%] w-[60%] h-[60%] bg-brand-100/50 rounded-full blur-[120px] animate-pulse-soft"></div>
        <div className="absolute bottom-[-10%] left-[-10%] w-[50%] h-[50%] bg-indigo-100/40 rounded-full blur-[100px]"></div>
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-[0.03]"></div>
      </div>

      <div className="w-full max-w-[1100px] grid lg:grid-cols-2 gap-12 items-center relative z-10">
        {/* Left Side: Branding & Info */}
        <div className="hidden lg:flex flex-col space-y-8 animate-fade-in">
          <div className="space-y-4">
            <div className="inline-flex items-center gap-3 px-4 py-2 bg-white/80 backdrop-blur-md rounded-full border border-white/50 shadow-glass text-[11px] font-bold text-brand-600 uppercase tracking-widest">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-600"></span>
              </span>
              Digital India Initiative
            </div>
            <h1 className="text-6xl font-black text-slate-900 leading-[1.1] tracking-tight">
              Empowering <br />
              <span className="gradient-text">Citizens</span> through <br />
              Smart Governance.
            </h1>
            <p className="text-lg text-slate-500 max-w-md font-medium leading-relaxed">
              Access the Unified Public Distribution System portal for seamless entitlement management and grievance redressal.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-6 pt-4">
            {[
              { icon: ShieldCheck, title: "Secure Access", desc: "Multi-factor authentication" },
              { icon: CheckCircle2, title: "ONORC Enabled", desc: "Nation-wide portability" }
            ].map((item, i) => (
              <div key={i} className="p-5 glass-card rounded-2xl space-y-3">
                <div className="w-10 h-10 bg-brand-50 rounded-xl flex items-center justify-center text-brand-600">
                  <item.icon size={22} />
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 text-sm">{item.title}</h3>
                  <p className="text-xs text-slate-500 font-medium">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Side: Login Card */}
        <div className="flex justify-center lg:justify-end">
          <div className="w-full max-w-[440px] animate-fade-in-up">
            <div className="bg-white rounded-[2.5rem] shadow-premium p-10 md:p-12 relative overflow-hidden border border-white/40">
              {/* Card Accent */}
              <div className="absolute top-0 right-0 w-32 h-32 bg-brand-50 rounded-full -mr-16 -mt-16 opacity-50"></div>
              
              <div className="relative z-10">
                <div className="flex justify-between items-start mb-10">
                  <div className="w-14 h-14 bg-brand-600 rounded-2xl flex items-center justify-center shadow-lg shadow-brand-200">
                    <ShieldCheck size={28} className="text-white" />
                  </div>
                  <button 
                    onClick={toggleLanguage}
                    className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-slate-100 hover:bg-slate-50 transition-all font-bold text-[10px] uppercase tracking-wider text-slate-500"
                  >
                    <Globe size={14} />
                    {i18n.language === 'hi' ? 'हिंदी' : 'English'}
                  </button>
                </div>

                <div className="mb-8">
                  <h2 className="text-2xl font-black text-slate-900 tracking-tight">Portal Sign In</h2>
                  <p className="text-sm text-slate-400 font-medium mt-1">Please enter your registered mobile number</p>
                </div>

                <div className="space-y-6">
                  {step === 1 ? (
                    <div className="space-y-5">
                      <div>
                        <label className="label">Mobile Number</label>
                        <div className="relative group">
                          <div className="absolute left-5 top-1/2 -translate-y-1/2 flex items-center gap-2 text-slate-400 border-r border-slate-100 pr-3 transition-colors group-focus-within:text-brand-600">
                            <Phone size={16} />
                            <span className="text-xs font-bold">+91</span>
                          </div>
                          <input
                            type="tel"
                            value={phoneNumber}
                            onChange={(e) => setPhoneNumber(e.target.value.replace(/\D/g, ''))}
                            className="input pl-20 h-[56px] text-base"
                            placeholder="98765 43210"
                            maxLength="10"
                          />
                        </div>
                      </div>
                      <button
                        onClick={handleGetOtp}
                        disabled={loading || phoneNumber.length !== 10}
                        className="btn btn-primary w-full h-[56px] gap-3 text-base"
                      >
                        {loading ? <Loader2 className="animate-spin" /> : <>Get Verification Code <ArrowRight size={18} /></>}
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-5">
                      <div className="p-4 bg-brand-50/50 rounded-2xl border border-brand-100/50 flex justify-between items-center mb-2">
                        <div className="flex flex-col">
                          <span className="text-[9px] uppercase font-bold text-brand-400 tracking-widest">Verify identity for</span>
                          <span className="text-sm text-brand-700 font-bold">+91 {phoneNumber}</span>
                        </div>
                        <button onClick={() => setStep(1)} className="text-[10px] text-brand-600 font-bold hover:text-brand-800 underline underline-offset-4 uppercase tracking-wider">Edit</button>
                      </div>
                      <div>
                        <label className="label">Enter 6-Digit OTP</label>
                        <div className="relative group">
                          <div className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-400 transition-colors group-focus-within:text-brand-600">
                            <Lock size={18} />
                          </div>
                          <input
                            type="text"
                            value={otp}
                            onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
                            className="input pl-14 h-[60px] text-center text-2xl tracking-[0.3em] font-black"
                            placeholder="000000"
                            maxLength="6"
                            autoFocus
                          />
                        </div>
                      </div>
                      <button
                        onClick={handleVerifyOtp}
                        disabled={loading || otp.length !== 6}
                        className="btn btn-primary w-full h-[60px] text-base shadow-brand-200"
                      >
                        {loading ? <Loader2 className="animate-spin" /> : 'Enter Dashboard'}
                      </button>
                      <div className="text-center">
                        <p className="text-xs text-slate-400 font-medium">Didn't receive code? <button className="text-brand-600 font-bold hover:underline">Resend OTP</button></p>
                      </div>
                    </div>
                  )}

                  {error && (
                    <div className="p-4 bg-rose-50 border border-rose-100 rounded-2xl text-rose-600 text-[13px] font-bold flex gap-3 items-center animate-in fade-in zoom-in-95 duration-200">
                      <div className="w-1.5 h-1.5 bg-rose-500 rounded-full animate-pulse"></div>
                      {error}
                    </div>
                  )}
                </div>
                
                <div className="mt-12 pt-8 border-t border-slate-50">
                   <div className="flex items-center gap-4">
                     <div className="flex -space-x-3">
                        {[1, 2, 3].map(i => (
                          <div key={i} className="w-8 h-8 rounded-full border-2 border-white bg-slate-100 flex items-center justify-center overflow-hidden">
                            <img src={`https://i.pravatar.cc/100?u=${i}`} alt="user" />
                          </div>
                        ))}
                     </div>
                     <p className="text-[11px] text-slate-400 font-medium">Joined by <span className="text-slate-900 font-bold">2.4k+</span> officials today</p>
                   </div>
                </div>
              </div>
            </div>
            
            <p className="mt-8 text-center text-slate-400 text-[10px] font-bold uppercase tracking-[0.3em]">
              Ministry of Consumer Affairs
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
