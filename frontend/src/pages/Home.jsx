import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/authContext';

const Home = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  
  const [stats, setStats] = useState({
    casesToday: 0,
    pendingCases: 0,
    resolvedCases: 0,
    avgResolutionTime: 0
  });
  
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Fetch stats from the backend
    const fetchStats = async () => {
      try {
        // In a real app, we would make an API call to get the stats
        // For now, we'll simulate with some dummy data
        setStats({
          casesToday: 12,
          pendingCases: 5,
          resolvedCases: 45,
          avgResolutionTime: 2.5
        });
      } catch (err) {
        console.error('Failed to fetch stats:', err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchStats();
  }, []);
  
  if (!user) {
    navigate('/login');
    return null;
  }
  
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <h1 className="text-xl font-semibold text-gray-900">
                  {t('appName')}
                </h1>
              </div>
              <div className="hidden md:block">
                <div className="ml-10 flex items-baseline space-x-4">
                  <a href="#" className="px-3 py-2 rounded-md text-sm font-medium text-gray-500 hover:text-gray-700 hover:bg-gray-50">
                    {t('home.welcome', { name: user.name || 'User' })}
                  </a>
                </div>
              </div>
            </div>
            <div className="flex-shrink-0 flex items-center">
              <button
                onClick={logout}
                className="px-3 py-2 bg-white text-sm font-medium text-gray-500 rounded-md hover:text-gray-700 hover:bg-gray-50"
              >
                {t('common.logout')}
              </button>
            </div>
          </div>
        </div>
      </header>
      
      <main className="py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              {t('home.welcome', { name: user.name || 'User' })}
            </h2>
            <p className="mt-1 text-sm text-gray-500">
              {t('home.role', { role: user.role })}
            </p>
          </div>
          
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {/* Action Cards */}
            <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer"
                 onClick={() => navigate('/entitlement-check')}>
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <svg className="h-8 w-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m2 0a2 2 0 100-4 2 2 0 000 4zm-9 3a2 2 0 110-4 2 2 0 010 4zm9-6a2 2 0 100-4 2 2 0 000 4v2m0 6a2 2 0 110-4 2 2 0 010 4zm5.657-2.343a2 2 0 10-2.828-2.828 2 2 0 002.828 2.828zm-2.828 0a2 2 0 112.828 2.828 2 2 0 01-2.828-2.828z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">
                    {t('home.checkEntitlement')}
                  </h3>
                  <p className="mt-1 text-sm text-gray-500">
                    {t('home.lessReceived')}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer"
                 onClick={() => navigate('/lodge-complaint')}>
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <svg className="h-8 w-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2zm0 10c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z" />
                  </svg>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">
                    {t('home.lodgeComplaint')}
                  </h3>
                  <p className="mt-1 text-sm text-gray-500">
                    {t('home.trackCase')}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer"
                 onClick={() => navigate('/case-tracker')}>
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <svg className="h-8 w-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7H3m8 4H3m-4 8h12a2 2 0 002-2V9a2 2 0 00-2-2H6a2 2 0 00-2 2v2m6-4l-2 2L4 15" />
                  </svg>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">
                    {t('home.trackCase')}
                  </h3>
                  <p className="mt-1 text-sm text-gray-500">
                    {t('home.caseTracker')}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer"
                 onClick={() => navigate('/my-village-report')}>
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <svg className="h-8 w-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 00-2 2m14 0v2a2 2 0 01-2 2" />
                  </svg>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900">
                    {t('home.myVillageReport')}
                  </h3>
                  <p className="mt-1 text-sm text-gray-500">
                    {t('home.villageReportDesc')}
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          {/* Statistics Cards */}
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div className="bg-white rounded-lg shadow-md p-6 text-center">
              <h3 className="text-lg font-medium text-gray-900">
                {t('home.stats.casesToday')}
              </h3>
              <p className="mt-2 text-2xl font-bold text-primary-600">
                {stats.casesToday}
              </p>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6 text-center">
              <h3 className="text-lg font-medium text-gray-900">
                {t('home.stats.pendingCases')}
              </h3>
              <p className="mt-2 text-2xl font-bold text-warning-500">
                {stats.pendingCases}
              </p>
            </div>
            
            <div className="bg-white rounded-lg shadow-md p-6 text-center">
              <h3 className="text-lg font-medium text-gray-
