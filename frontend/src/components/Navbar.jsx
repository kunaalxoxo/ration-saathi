import React from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../lib/authContext';
import { Search, LogOut, Globe, Bell, Menu, LayoutGrid } from 'lucide-react';

const Navbar = () => {
  const { t, i18n } = useTranslation();
  const { logout } = useAuth();
  
  const toggleLanguage = () => {
    const nextLng = i18n.language === 'hi' ? 'en' : 'hi';
    i18n.changeLanguage(nextLng);
  };

  return (
    <header className="fixed top-0 right-0 left-[280px] h-20 bg-white/80 backdrop-blur-md border-b border-slate-100 z-40 px-10 flex items-center justify-between">
      <div className="flex-1 max-w-xl">
        <div className="relative group">
          <Search size={18} className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-brand-600 transition-colors" />
          <input 
            type="text" 
            placeholder="Search cases, cards, or reports..." 
            className="w-full pl-14 pr-6 py-3.5 bg-slate-50 border-transparent focus:bg-white focus:border-brand-500 focus:ring-4 focus:ring-brand-50 rounded-[1.25rem] outline-none transition-all text-[13px] font-medium"
          />
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <button 
          onClick={toggleLanguage}
          className="flex items-center gap-2.5 px-5 py-2.5 rounded-2xl border border-slate-100 hover:bg-slate-50 transition-all font-black text-[10px] uppercase tracking-widest text-slate-500"
        >
          <Globe size={16} className="text-brand-600" />
          <span>{i18n.language === 'hi' ? 'हिंदी' : 'English'}</span>
        </button>
        
        <div className="relative group">
          <button className="p-3 text-slate-400 hover:text-brand-600 hover:bg-brand-50 rounded-2xl transition-all relative">
            <Bell size={20} />
            <span className="absolute top-3 right-3 w-2 h-2 bg-rose-500 rounded-full border-2 border-white ring-2 ring-rose-100 animate-pulse"></span>
          </button>
        </div>
        
        <button className="p-3 text-slate-400 hover:text-brand-600 hover:bg-brand-50 rounded-2xl transition-all">
          <LayoutGrid size={20} />
        </button>
        
        <div className="w-px h-8 bg-slate-100 mx-2"></div>
        
        <button 
          onClick={logout}
          className="flex items-center gap-2.5 px-5 py-2.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-2xl transition-all font-black text-[10px] uppercase tracking-widest"
        >
          <LogOut size={18} />
          <span>Logout</span>
        </button>
      </div>
    </header>
  );
};

export default Navbar;
