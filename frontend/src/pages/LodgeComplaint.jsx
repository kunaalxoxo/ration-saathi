import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../lib/authContext';

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
      setError('Please enter the quantity you actually received.');
      return;
    }
    
    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));
      const caseNumber = `RS-RJ-${Math.floor(100000 + Math.random() * 900000)}`;
      setCaseDetails({ caseNumber });
      setStep(4);
    } catch (err) {
      setError('Failed to submit complaint. Please try again.');
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
            <h1 className="text-xl font-bold text-green-700">Lodge Complaint</h1>
          </div>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-sm border p-6">
          {step === 1 && (
            <div>
              <h2 className="text-lg font-bold mb-4">Step 1: Confirm Details</h2>
              <div className="space-y-4 mb-6">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-500">Ration Card</p>
                  <p className="font-bold">{cardNumber || 'Not provided'}</p>
                </div>
                {headName && (
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-500">Head of Household</p>
                    <p className="font-bold">{headName}</p>
                  </div>
                )}
              </div>
              <button 
                onClick={() => setStep(2)}
                disabled={!cardNumber}
                className="w-full py-3 bg-green-600 text-white font-bold rounded-md"
              >
                Confirm & Continue
              </button>
            </div>
          )}

          {step === 2 && (
            <div>
              <h2 className="text-lg font-bold mb-4">Step 2: Select Issue</h2>
              <div className="grid gap-4">
                {['Short Supply', 'Quality Issue', 'Overcharging', 'Denied Service'].map(issue => (
                  <button
                    key={issue}
                    onClick={() => { setIssueType(issue); setStep(3); }}
                    className="p-4 text-left border rounded-lg hover:border-green-500 hover:bg-green-50"
                  >
                    {issue}
                  </button>
                ))}
              </div>
            </div>
          )}

          {step === 3 && (
            <div>
              <h2 className="text-lg font-bold mb-4">Step 3: Quantity Details</h2>
              <p className="text-sm text-gray-600 mb-4">How much did you actually receive?</p>
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-1">Quantity (in kg)</label>
                <input
                  type="number"
                  value={receivedQuantity}
                  onChange={(e) => setReceivedQuantity(e.target.value)}
                  className="w-full px-4 py-2 border rounded-md"
                  placeholder="Enter kg received"
                />
              </div>
              {error && <p className="text-red-600 text-sm mb-4">{error}</p>}
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="w-full py-3 bg-green-600 text-white font-bold rounded-md disabled:opacity-50"
              >
                {loading ? 'Submitting...' : 'Submit Complaint'}
              </button>
            </div>
          )}

          {step === 4 && (
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Complaint Registered!</h2>
              <p className="text-gray-600 mb-6">Your case number is <span className="font-bold text-gray-900">{caseDetails.caseNumber}</span></p>
              <div className="space-y-3">
                <button
                  onClick={() => window.print()}
                  className="w-full py-2 border border-gray-300 rounded-md"
                >
                  Download Receipt
                </button>
                <button
                  onClick={() => navigate('/home')}
                  className="w-full py-2 bg-green-600 text-white font-bold rounded-md"
                >
                  Return Home
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default LodgeComplaint;
