import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../lib/authContext';

const CaseTracker = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [caseNumber, setCaseNumber] = useState('');
  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);
  
  const handleTrackCase = async () => {
    if (!caseNumber) {
      setError(t('caseTracker.error.invalidInput'));
      return;
    }
    
    // Simple validation: case number format RS-XX-2025-XXXX
    const caseNumberRegex = /^RS-[A-Z]{2}-2025-\d{4}$/;
    if (!caseNumberRegex.test(caseNumber)) {
      setError(t('caseTracker.error.invalidInput'));
      return;
    }
    
    setLoading(true);
    setError('');
    setCaseData(null);
    
    try {
      // In a real app, we would call the backend API to get the case details
      // For now, we'll simulate with some dummy data
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Simulate fetching case data
      const dummyData = {
        caseNumber: caseNumber,
        status: 'under_investigation', // open, acknowledged, under_investigation, resolved, closed
        filedOn: new Date('2025-10-15'),
        timeline: [
          { stage: t('common.created'), date: new Date('2025-10-15'), notes: t('common.caseFiledNote') },
          { stage: t('common.acknowledged'), date: new Date('2025-10-16'), notes: t('common.caseAcknowledgedNote') },
          { stage: t('common.underInvestigation'), date: new Date('2025-10-20'), notes: t('common.investigationNote') }
        ],
        resolution: t('caseTracker.notResolved')
      };
      
      // If the status is resolved, we can add a resolution note
      if (dummyData.status === 'resolved' || dummyData.status === 'closed') {
        dummyData.resolution = t('caseTracker.resolutionNote', { 
          action: t('common.actionTaken'), 
          amount: '2.5' 
        });
      }
      
      setCaseData(dummyData);
    } catch (err) {
      setError(t('caseTracker.error.apiError'));
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
              {t('caseTracker.title')}
            </h2>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <form onSubmit={(e) => {
              e.preventDefault();
              handleTrackCase();
            }} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('caseTracker.caseNumberLabel')}
                </label>
                <input
                  type="text"
                  value={caseNumber}
                  onChange={(e) => setCaseNumber(e.target.value.replace(/[^A-Z0-9\-]/g, '').toUpperCase())}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder={t('caseTracker.caseNumberPlaceholder')}
                  maxLength="15"
                />
                {error && (
                  <p className="mt-2 text-sm text-red-500">
                    {error}
                  </p>
                )}
              </div>
              <button
                type="submit"
                disabled={loading || !caseNumber}
                className="w-full px-4 py-2 bg-primary-600 text-white font-medium rounded-md disabled:opacity-50 hover:bg-primary-700 transition-colors"
              >
                {loading ? t('common.loading') : t('caseTracker.trackButton')}
              </button>
            </form>
            
            {caseData && (
              <div className="mt-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  {t('caseTracker.result.title')}
                </h3>
                <div className="space-y-4 text-gray-700">
                  <p>
                    <span className="font-medium">{t('caseTracker.result.caseNumber')}:</span> 
                    {caseData.caseNumber}
                  </p>
                  <p>
                    <span className="font-medium">{t('caseTracker.result.status')}:</span> 
                    { 
                      // Map status to translation
                      statusMap = {
                        'open': t('common.statusOpen'),
                        'acknowledged': t('common.statusAcknowledged'),
                        'under_investigation': t('common.statusUnderInvestigation'),
                        'resolved': t('common.statusResolved'),
                        'closed': t('common.statusClosed')
                      };
                      statusMap[caseData.status] || caseData.status
                    }
                  </p>
                  <p>
                    <span className="font-medium">{t('caseTracker.result.filedOn')}:</span> 
                    {caseData.filedOn.toLocaleDateString()}
                  </p>
                  
                  <div className="mt-4">
                    <h4 className="text-lg font-medium text-gray-900 mb-2">
                      {t('caseTracker.result.timeline')}
                    </h4>
                    <div className="space-y-3">
                      {caseData.timeline.map((item, index) => (
                        <div key={index} className="flex items-start space-x-3">
                          <div className="flex-shrink-0">
                            <div className="h-2.5 w-2.5 bg-primary-500 rounded-full"/>
                          </div>
                          <div className="flex-1">
                            <p className="text-sm font-medium text-gray-700">
                              {item.stage}
                            </p>
                            <p className="text-xs text-gray-500">
                              {item.date.toLocaleDateString()}
                            </p>
                            {item.notes && (
                              <p className="text-xs text-gray-400 mt-0.5">
                                {item.notes}
                              </p>
                            )}
                          </div>
                        >
                      ))}
                    </div>
                  </d
