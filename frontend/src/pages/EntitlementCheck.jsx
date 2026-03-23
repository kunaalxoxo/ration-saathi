import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/authContext';

const EntitlementCheck = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [cardNumber, setCardNumber] = useState('');
  const [entitlementData, setEntitlementData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);
  
  const handleCheckEntitlement = async () => {
    if (!cardNumber || cardNumber.length < 10) {
      setError(t('entitlementCheck.error.invalidInput'));
      return;
    }
    
    setLoading(true);
    setError('');
    setEntitlementData(null);
    
    try {
      // In a real app, we would call the backend API
      // For now, we'll simulate with some dummy data
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Simulate fetching entitlement data
      const dummyData = {
        cardNumber: cardNumber,
        headName: "Ram Kumar",
        members: 5,
        allocation: {
          wheat: 5.0,
          rice: 5.0,
          sugar: 0.5
        },
        month: "October 2025"
      };
      
      setEntitlementData(dummyData);
    } catch (err) {
      setError(t('entitlementCheck.error.apiError'));
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
              {t('entitlementCheck.title')}
            </h2>
          </div>
          
          <div className="bg-white rounded-lg shadow-md p-6">
            <form onSubmit={(e) => {
              e.preventDefault();
              handleCheckEntitlement();
            }} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {t('entitlementCheck.cardNumberLabel')}
                </label>
                <input
                  type="tel"
                  value={cardNumber}
                  onChange={(e) => setCardNumber(e.target.value.replace(/\D/g, ''))}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder={t('entitlementCheck.cardNumberPlaceholder')}
                  maxLength="10"
                />
              </div>
              <button
                type="submit"
                disabled={loading || !cardNumber || cardNumber.length !== 10}
                className="w-full px-4 py-2 bg-primary-600 text-white font-medium rounded-md disabled:opacity-50 hover:bg-primary-700 transition-colors"
              >
                {loading ? t('common.loading') : t('entitlementCheck.checkButton')}
              </button>
            </form>
            
            {error && (
              <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 mt-4">
                {error}
              </div>
            )}
            
            {entitlementData && (
              <div className="mt-6">
                <h3 className="text-xl font-bold text-gray-900 mb-4">
                  {t('entitlementCheck.result.title')}
                </h3>
                <div className="space-y-4 text-gray-700">
                  <p>
                    <span className="font-medium">{t('entitlementCheck.result.cardNumber')}:</span> 
                    {entitlementData.cardNumber}
                  </p>
                  <p>
                    <span className="font-medium">{t('entitlementCheck.result.headName')}:</span> 
                    {entitlementData.headName}
                  </p>
                  <p>
                    <span className="font-medium">{t('entitlementCheck.result.members')}:</span> 
                    {entitlementData.members}
                  </p>
                  <div className="mt-2">
                    <span className="font-medium">{t('entitlementCheck.result.allocation')}:</span>
                    <div className="mt-2 space-y-2">
                      <p>
                        <span className="font-medium">{t('entitlementCheck.result.wheat')}:</span> 
                        {entitlementData.allocation.wheat} kg
                      </p>
                      <p>
                        <span className="font-medium">{t('entitlementCheck.result.rice')}:</span> 
                        {entitlementData.allocation.rice} kg
                      </p>
                      <p>
                        <span className="font-medium">{t('entitlementCheck.result.sugar')}:</span> 
                        {entitlementData.allocation.sugar} kg
                      </p>
                    </div>
                  </div>
                  <div className="mt-4">
                    <button
                      onClick={() => navigate(`/lodge-complaint?cardNumber=${entitlementData.cardNumber}`)}
                      className="w-full px-4 py-2 bg-warning-500 text-white font-medium rounded-md hover:bg-warning-600 transition-colors"
                    >
                      {t('entitlementCheck.result.lessReceived')}
                    </button>
                    <button
                      onClick={() => window.print()}
                      className="w-full mt-2 px-4 py-2 bg-gray-200 text-gray-800 font-medium rounded-md hover:bg-gray-300 transition-colors"
                    >
                      {t('entitlementCheck.result.printSlip')}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default EntitlementCheck;
