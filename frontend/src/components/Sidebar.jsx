import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  ClipboardCheck, 
  MessageSquarePlus, 
  Search, 
  BarChart3,
  ShieldCheck,
  Settings,
  HelpCircle,
  ChevronRight,
  LogOut,
  User
} from 'lucide-react';
import { useAuth } from '../lib/authContext';

const Sidebar = () => {
  const { user, logout } = useAuth();
  
  const navItems = [
    { name: 'Dashboard', path: '/home', icon: LayoutDashboard },
    { name: 'Entitlement', path: '/entitlement-check', icon: ClipboardCheck },
    { name: 'Lodge Grievance', path: '/lodge-complaint', icon: MessageSquarePlus },
    { name: 'Track Cases', path: '/case-tracker', icon: Search },
    { name: 'Village Report', path: '/my-village-report', icon: BarChart3 },
  ];

  if (user && (user.role === 'district_admin' || user.role === 'state_admin' || user.role === 'super_admin')) {
    navItems.push({ name: 'Admin Control', path: '/admin', icon: ShieldCheck });
  }

  return (
    <aside className="fixed left-0 top-0 h-full w-[280px] bg-white border-r border-slate-100 z-50 flex flex-col shadow-[4px_0_24px_rgba(0,0,0,0.02)]">
      <div className="p-8 mb-4">
        <div className="flex items-center gap-3.5">
          <div className="w-11 h-11 bg-brand-600 rounded-2xl flex items-center justify-center shadow-lg shadow-brand-100 ring-4 ring-brand-50">
            <ShieldCheck size={24} className="text-white" />
          </div>
          <div>
            <h1 className="font-black text-slate-900 leading-none tracking-tight text-lg">Ration Saathi</h1>
            <p className="text-[9px] text-brand-600 font-black uppercase tracking-[0.2em] mt-1.5">PDS Unified Portal</p>
          </div>
        </div>
      </div>
      
      <nav className="flex-1 px-4 space-y-1.5 overflow-y-auto custom-scrollbar">
        <p className="px-5 text-[10px] font-black text-slate-300 uppercase tracking-[0.2em] mb-4 mt-2">Systems</p>
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) => 
              `flex items-center justify-between group px-5 py-3.5 rounded-2xl text-[13px] font-bold transition-all duration-300 ${
                isActive 
                  ? 'bg-brand-600 text-white shadow-lg shadow-brand-100' 
                  : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
              }`
            }
          >
            <div className="flex items-center gap-3.5">
              <item.icon size={20} className="transition-transform duration-300 group-hover:scale-110" />
              <span className="tracking-wide">{item.name}</span>
            </div>
            <ChevronRight size={14} className={`opacity-0 group-hover:opacity-100 transition-all transform translate-x-0 group-hover:translate-x-1 ${isActive ? 'text-white/50' : 'text-slate-300'}`} />
          </NavLink>
        ))}

        <p className="px-5 text-[10px] font-black text-slate-300 uppercase tracking-[0.2em] mb-4 mt-10">Governance</p>
        <button className="w-full flex items-center gap-3.5 px-5 py-3.5 rounded-2xl text-[13px] font-bold text-slate-500 hover:bg-slate-50 hover:text-slate-900 transition-all group">
          <Settings size={20} className="text-slate-400 group-hover:rotate-45 transition-transform duration-500" />
          <span className="tracking-wide">Portal Settings</span>
        </button>
        <button className="w-full flex items-center gap-3.5 px-5 py-3.5 rounded-2xl text-[13px] font-bold text-slate-500 hover:bg-slate-50 hover:text-slate-900 transition-all group">
          <HelpCircle size={20} className="text-slate-400" />
          <span className="tracking-wide">Documentation</span>
        </button>
      </nav>
      
      <div className="p-6">
        <div className="p-4 bg-slate-50 rounded-[2rem] border border-slate-100 relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-20 h-20 bg-brand-100/30 rounded-full -mr-10 -mt-10 transition-transform group-hover:scale-150 duration-700"></div>
          <div className="relative z-10 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white flex items-center justify-center border border-slate-200 shadow-sm overflow-hidden p-0.5">
              <img 
                src={`https://ui-avatars.com/api/?name=${encodeURIComponent(user?.name || 'User')}&background=4767ff&color=fff&bold=true`} 
                alt="avatar" 
                className="w-full h-full rounded-lg object-cover"
              />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-[12px] font-black text-slate-900 truncate leading-tight">{user?.name || 'Guest User'}</p>
              <p className="text-[9px] text-brand-600 font-black uppercase tracking-widest mt-0.5">{user?.role?.replace('_', ' ')}</p>
            </div>
            <button 
              onClick={logout}
              className="p-2 text-slate-400 hover:text-rose-500 hover:bg-rose-50 rounded-lg transition-all"
              title="Logout"
            >
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
