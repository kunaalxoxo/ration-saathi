import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/authContext';

const Login = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { login } = useAuth();
  
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState(1); // 1: enter phone, 2: enter OTP
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGetOtp = async () => {
    setLoading(true);
    setError('');
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      setStep(2);
    } catch (err) {
      setError('Failed to send OTP. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async () => {
    setLoading(true);
    setError('');
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Call login from authContext to persist user
      login({
        id: '1',
        name: 'CSC Operator',
        phone: phoneNumber,
        role: 'csc_operator',
        district_code: 'RJ-BA',
        block_code: 'RJ-BA-001'
      });
      
      navigate('/home');
    } catch (err) {
      setError('Invalid OTP. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md space-y-6 p-6 bg-white rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center text-gray-800">
          {t('appName', { defaultValue: 'Ration Saathi' })}
        </h2>
        <p className="text-center text-gray-600">
          {t('tagline', { defaultValue: 'Your Voice for Ration Entitlements' })}
        </p>
        
        {step === 1 && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                {t('login.phoneNumber', { defaultValue: 'Phone Number' })}
              </label>
              <input
                type="tel"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value.replace(/\D/g, ''))}
                className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                placeholder="10 digit mobile number"
                maxLength="10"
              />
            </div>
            <button
              onClick={handleGetOtp}
              disabled={loading || !phoneNumber || phoneNumber.length !== 10}
              className="w-full px-4 py-2 bg-green-600 text-white font-medium rounded-md disabled:opacity-50 hover:bg-green-700 transition-colors"
            >
              {loading ? t('common.loading', { defaultValue: 'Loading...' }) : t('login.getOtp', { defaultValue: 'Get OTP' })}
            </button>
          </div>
        )}
        
        {step === 2 && (
          <div className="space-y-4">
            <p className="text-sm text-center text-gray-600">
              OTP sent to {phoneNumber}
            </p>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                {t('login.otp', { defaultValue: 'Enter OTP' })}
              </label>
              <input
                type="text"
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
                className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
                placeholder="6 digit OTP"
                maxLength="6"
              />
            </div>
            <button
              onClick={handleVerifyOtp}
              disabled={loading || otp.length !== 6}
              className="w-full px-4 py-2 bg-green-600 text-white font-medium rounded-md disabled:opacity-50 hover:bg-green-700 transition-colors"
            >
              {loading ? t('common.loading', { defaultValue: 'Loading...' }) : t('login.verify', { defaultValue: 'Verify & Login' })}
            </button>
            <button 
              onClick={() => setStep(1)}
              className="w-full text-sm text-gray-500 hover:text-gray-700"
            >
              Change Phone Number
            </button>
          </div>
        )}
        
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 mt-4">
            {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default Login;
