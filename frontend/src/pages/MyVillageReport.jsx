import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/authContext';

const MyVillageReport = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);
  
  useEffect(() => {
    if (user) {
      fetchReport();
    }
  }, [user]);
  
  const fetchReport = async () => {
    setLoading(true);
    setError('');
    try {
      // In a real app, we would call the backend API to get the village report
      // For now, we'll simulate with some dummy data
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const dummyData = {
        villageName: "Shyamgarh",
        totalRationCards: 120,
        activeCards: 110,
        totalCasesThisMonth: 8,
        resolvedCases: 5,
        pendingCases: 3,
        fpsPerformance: [
          { fpsCode: 'RJ-BA-001', name: 'Shri Ram FPS', complaints: 2, resolutionRate: 80 },
          { fpsCode: 'RJ-BA-002', name: 'Krishna FPS', complaints: 0, resolutionRate: 100 },
          { fpsCode: 'RJ-BA-003', name: 'Shiv Shakti FPS', complaints: 4, resolutionRate: 60 },
          { fpsCode: 'RJ-BA-004', name: 'Mahalakshmi FPS', complaints: 1, resolutionRate: 90 },
          { fpsCode: 'RJ-BA-005', name: 'Hanuman FPS', complaints: 1, resolutionRate: 70 }
        ]
      };
      
      setReportData(dummyData);
    } catch (err) {
      setError(t('common.error'));
    } finally {
      setLoading(false);
    }
  };
  
  if (!user) {
    return null; // Redirect handled by useEffect
  }
  
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0">
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
                onClick={() => navigate('/home')}
                className="px-3 py-2 bg-white text-sm font-medium text-gray-500 rounded-md hover:text-gray-700 hover:bg-gray-50"
              >
                {t('common.back')}
              </button>
            </div>
          </div>
        </div>
      </header>
      
      <main className="py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              {t('home.myVillageReport')}
            </h2>
          </div>
          
          {loading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              <p className="mt-4 text-gray-500">{t('common.loading')}</p>
            </div>
          )}
          
          {error && (
            <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 mb-6">
              {error}
            </div>
          )}
          
          {!loading && !error && reportData && (
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  {t('home.villageReportTitle', { villageName: reportData.villageName })}
                </h3>
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 text-center">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-sm font-medium text-gray-500">
                      {t('home.totalRationCards')}
                    </p>
                    <p className="text-2xl font-bold text-gray-900">
                      {reportData.totalRationCards}
                    </p>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-sm font-medium text-gray-500">
                      {t('home.activeCards')}
                    </p>
                    <p className="text-2xl font-bold text-success-600">
                      {reportData.activeCards}
                    </p>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-sm font-medium text-gray-500">
                      {t('home.totalCasesThisMonth')}
                    </p>
                    <p className="text-2xl font-bold text-warning-600">
                      {reportData.totalCasesThisMonth}
                    </p>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-sm font-medium text-gray-500">
                      {t('home.resolvedCases')}
                    </p>
                    <p className="text-2xl font-bold text-success-600">
                      {reportData.resolvedCases}
                    </p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  {t('home.fpsPerformance')}
                </h3>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          {t('admin.fpsRiskTable.fpsCode')}
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          {t('admin.fpsRiskTable.fpsName')}
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          {t('admin.fpsRiskTable.complaints30d')}
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          {t('admin.fpsRiskTable.resolutionRate')}
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {reportData.fpsPerformance.map((fps, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                            {fps.fpsCode}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                            {fps.name}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                            {fps.complaints}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                            {fps.resolutionRate}%
                         
