import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../lib/authContext';

const LodgeComplaint = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();
  
  const [step, setStep] = useState(1); // 1: confirm card, 2: issue type, 3: quantities, 4: fps selection, 5: submit
  const [cardNumber, setCardNumber] = useState('');
  const [headName, setHeadName] = useState('');
  const [issueType, setIssueType] = useState(''); // 'wheat', 'rice', 'both'
  const [expectedWheat, setExpectedWheat] = useState(0);
  const [expectedRice, setExpectedRice] = useState(0);
  const [receivedQuantity, setReceivedQuantity] = useState('');
  const [fpsOptions, setFpsOptions] = useState([]);
  const [selectedFps, setSelectedFps] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(null);
  
  // Pre-fill card number from location state (if coming from EntitlementCheck)
  React.useEffect(() => {
    if (location.state && location.state.cardNumber) {
      setCardNumber(location.state.cardNumber);
      setHeadName(location.state.headName || '');
      // We would normally fetch the entitlement data to get expected quantities
      // For now, we'll set some dummy values
      setExpectedWheat(5.0);
      setExpectedRice(5.0);
      setStep(1);
    }
  }, [location]);
  
  const handleConfirmCard = (isCorrect) => {
    if (isCorrect) {
      setStep(2);
    } else {
      // Go back to entitlement check to re-enter card number
      navigate('/entitlement-check');
    }
  };
  
  const handleNextToQuantities = (selectedIssueType) => {
    setIssueType(selectedIssueType);
    setStep(3);
  };
  
  const handleNextToFPS = () => {
    if (!receivedQuantity || isNaN(parseFloat(receivedQuantity))) {
      setError(t('lodgeComplaint.error.invalidInput'));
      return;
    }
    setStep(4);
    // In a real app, we would fetch FPS options based on the user's location
    // For now, we'll use dummy data
    setFpsOptions([
      { code: 'RJ-BA-001', name: 'Shri Ram FPS' },
      { code: 'RJ-BA-002', name: 'Krishna FPS' },
      { code: 'RJ-BA-003', name: 'Shiv Shakti FPS' },
      { code: 'RJ-BA-004', name: 'Mahalakshmi FPS' },
      { code: 'RJ-BA-005', name: 'Hanuman FPS' }
    ]);
  };
  
  const handleSubmit = async () => {
    if (!selectedFps) {
      setError('Please select an FPS');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      // In a real app, we would call the backend to create the grievance case
      // For now, we'll simulate
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Generate a dummy case number
      const caseNumber = `RS-RJ-2025-${Math.floor(Math.random() * 9000 + 1000).toString().padStart(4, '0')}`;
      
      setSuccess({
        caseNumber,
        // We would also store the details for the success screen
      });
      setStep(5);
    } catch (err) {
      setError(t('lodgeComplaint.error.submitFailed'));
    } finally {
      setLoading(false);
    }
  };
  
  const handlePrintSlip = () => {
    // In a real app, we would generate a printable slip
    window.print();
  };
  
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
          {step === 1 && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                {t('lodgeComplaint.step1')}
              </h2>
              <div className="mt-4">
                <p className="text-gray-700">
                  {t('lodgeComplaint.confirmCard')}
                </p>
                <p className="font-medium mt-2">
                  {t('lodgeComplaint.cardNumber')}: {cardNumber}
                </p>
                <p className="font-medium mt-2">
                  {t('lodgeComplaint.headName')}: {headName || '---'}
                </p>
                <div className="mt-6 flex space-x-4">
                  <button
                    onClick={() => handleConfirmCard(true)}
                    className="flex-1 px-4 py-2 bg-success-500 text-white font-medium rounded-md hover:bg-success-600 transition-colors"
                  >
                    {t('lodgeComplaint.correct')}
                  </button>
                  <button
                    onClick={() => handleConfirmCard(false)}
                    className="flex-1 px-4 py-2 bg-error-500 text-white font-medium rounded-md hover:bg-error-600 transition-colors"
                  >
                    {t('lodgeComplaint.incorrect')}
                  </button>
                </div>
              </div>
            </div>
          )}
          
          {step === 2 && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                {t('lodgeComplaint.step2')}
              </h2>
              <div className="mt-4 space-y-4">
                <p className="text-gray-700">
                  {t('lodgeComplaint.issueType')}
                </p>
                <div className="grid gap-4 sm:grid-cols-3">
                  <button
                    onClick={() => handleNextToQuantities('wheat')}
                    className="px-4 py-3 border border-gray-300 rounded-md hover:border-primary-500 hover:bg-primary-50"
                  >
                    {t('lodgeComplaint.shortSupply')}
                  </button>
                  <button
                    onClick={() => handleNextToQuantities('rice')}
                    className="px-4 py-3 border border-gray-300 rounded-md hover:border-primary-500 hover:bg-primary-50"
                  >
                    {t('lodgeComplaint.denial')}
                  </button>
                  <button
                    onClick={() => handleNextToQuantities('both')}
                    className="px-4 py-3 border border-gray-300 rounded-md hover:border-primary-500 hover:bg-primary-50"
                  >
                    {t('lodgeComplaint.quality')}
                  </button>
                  {/* We have only three options in the IVR, but we can add more here if needed */}
                </div>
              </div>
            </div>
          )}
          
          {step === 3 && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                {t('lodgeComplaint.step3')}
              </h2>
              <div className="mt-4">
                <p className="text-gray-700 mb-2">
                  {t('lodgeComplaint.expectedQuantity')}
        
