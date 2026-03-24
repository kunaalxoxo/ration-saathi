import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/authContext';

const Home = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  
  const [stats, setStats] = useState({
    casesToday: 12,
    pendingCases: 5,
    resolvedCases: 45,
    avgResolutionTime: 2.5
  });
  
  const [loading, setLoading] = useState(false);
  
  if (!user) {
    return null;
  }
  
  const actions = [
    {
      title: t('home.checkEntitlement', { defaultValue: 'Check Entitlement' }),
      desc: t('home.checkEntitlementDesc', { defaultValue: 'Verify what you should receive' }),
      path: '/entitlement-check',
      icon: (
        <svg className="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      )
    },
    {
      title: t('home.lodgeComplaint', { defaultValue: 'Lodge Complaint' }),
      desc: t('home.lodgeComplaintDesc', { defaultValue: 'File a grievance for short supply' }),
      path: '/lodge-complaint',
      icon: (
        <svg className="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      )
    },
    {
      title: t('home.trackCase', { defaultValue: 'Track Case' }),
      desc: t('home.trackCaseDesc', { defaultValue: 'Check the status of your complaint' }),
      path: '/case-tracker',
      icon: (
        <svg className="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      )
    },
    {
      title: t('home.myVillageReport', { defaultValue: 'Village Report' }),
      desc: t('home.villageReportDesc', { defaultValue: 'See statistics for your area' }),
      path: '/my-village-report',
      icon: (
        <svg className="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      )
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 h-16 flex justify-between items-center">
          <h1 className="text-xl font-bold text-green-700">Ration Saathi</h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">
              {user.name} ({user.role})
            </span>
            <button
              onClick={logout}
              className="text-sm font-medium text-gray-500 hover:text-red-600"
            >
              {t('common.logout', { defaultValue: 'Logout' })}
            </button>
          </div>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900">
            {t('home.welcome', { name: user.name, defaultValue: `Welcome, ${user.name}!` })}
          </h2>
        </div>
        
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {actions.map((action) => (
            <div 
              key={action.path}
              onClick={() => navigate(action.path)}
              className="bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow cursor-pointer"
            >
              <div className="mb-4">{action.icon}</div>
              <h3 className="text-lg font-bold text-gray-900 mb-1">{action.title}</h3>
              <p className="text-sm text-gray-500">{action.desc}</p>
            </div>
          ))}
        </div>
        
        <div className="mt-12">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Area Overview</h3>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div className="bg-white rounded-lg border p-6">
              <p className="text-sm text-gray-500 mb-1">Cases Today</p>
              <p className="text-2xl font-bold text-green-600">{stats.casesToday}</p>
            </div>
            <div className="bg-white rounded-lg border p-6">
              <p className="text-sm text-gray-500 mb-1">Pending</p>
              <p className="text-2xl font-bold text-orange-500">{stats.pendingCases}</p>
            </div>
            <div className="bg-white rounded-lg border p-6">
              <p className="text-sm text-gray-500 mb-1">Resolved</p>
              <p className="text-2xl font-bold text-blue-600">{stats.resolvedCases}</p>
            </div>
            <div className="bg-white rounded-lg border p-6">
              <p className="text-sm text-gray-500 mb-1">Avg Resolution (Days)</p>
              <p className="text-2xl font-bold text-purple-600">{stats.avgResolutionTime}</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;
