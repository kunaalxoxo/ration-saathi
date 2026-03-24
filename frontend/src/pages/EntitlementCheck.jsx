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
  
  const handleCheckEntitlement = async () => {
    if (!cardNumber || cardNumber.length < 10) {
      setError('Please enter a valid 10-digit ration card number.');
      return;
    }
    
    setLoading(true);
    setError('');
    setEntitlementData(null);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
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
      setError('Failed to fetch entitlement details. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 h-16 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <button onClick={() => navigate('/home')} className="text-gray-500 hover:text-green-600">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
            </button>
            <h1 className="text-xl font-bold text-green-700">Check Entitlement</h1>
          </div>
        </div>
      </header>
      
      <main className="max-w-3xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-sm border p-6">
          <form onSubmit={(e) => { e.preventDefault(); handleCheckEntitlement(); }}>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Ration Card Number
              </label>
              <input
                type="tel"
                value={cardNumber}
                onChange={(e) => setCardNumber(e.target.value.replace(/\D/g, ''))}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 outline-none"
                placeholder="Enter 10 digit number"
                maxLength="10"
              />
            </div>
            <button
              type="submit"
              disabled={loading || cardNumber.length !== 10}
              className="w-full py-2 bg-green-600 text-white font-bold rounded-md hover:bg-green-700 disabled:opacity-50"
            >
              {loading ? 'Searching...' : 'Check Entitlement'}
            </button>
          </form>

          {error && (
            <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-md border border-red-100">
              {error}
            </div>
          )}

          {entitlementData && (
            <div className="mt-8 border-t pt-6">
              <h3 className="text-lg font-bold mb-4">Entitlement Details - {entitlementData.month}</h3>
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-gray-50 p-3 rounded">
                  <p className="text-xs text-gray-500">Household Head</p>
                  <p className="font-bold">{entitlementData.headName}</p>
                </div>
                <div className="bg-gray-50 p-3 rounded">
                  <p className="text-xs text-gray-500">Members</p>
                  <p className="font-bold">{entitlementData.members}</p>
                </div>
              </div>
              
              <div className="space-y-3">
                <div className="flex justify-between items-center p-3 border rounded">
                  <span className="font-medium text-gray-700">Wheat (Gehu)</span>
                  <span className="font-bold text-green-700">{entitlementData.allocation.wheat} kg</span>
                </div>
                <div className="flex justify-between items-center p-3 border rounded">
                  <span className="font-medium text-gray-700">Rice (Chawal)</span>
                  <span className="font-bold text-green-700">{entitlementData.allocation.rice} kg</span>
                </div>
                <div className="flex justify-between items-center p-3 border rounded">
                  <span className="font-medium text-gray-700">Sugar (Cheeni)</span>
                  <span className="font-bold text-green-700">{entitlementData.allocation.sugar} kg</span>
                </div>
              </div>

              <div className="mt-8 space-y-3">
                <button
                  onClick={() => navigate('/lodge-complaint', { state: { cardNumber: entitlementData.cardNumber, headName: entitlementData.headName } })}
                  className="w-full py-3 bg-orange-500 text-white font-bold rounded-md hover:bg-orange-600"
                >
                  I Received Less Ration
                </button>
                <button
                  onClick={() => window.print()}
                  className="w-full py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200"
                >
                  Print Slip
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default EntitlementCheck;
