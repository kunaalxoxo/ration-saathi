import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState(1); // 1: enter phone, 2: enter OTP
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGetOtp = async () => {
    // In a real app, we would call the backend to send OTP
    // For now, we'll simulate
    setLoading(true);
    setError('');
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      // If successful, go to OTP step
      setStep(2);
    } catch (err) {
      setError('Failed to send OTP. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async () => {
    // In a real app, we would verify the OTP with the backend
    setLoading(true);
    setError('');
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      // If successful, navigate to home
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
          {t('appName')}
        </h2>
        <p className="text-center text-gray-600">{t('tagline')}</p>
        
        {step === 1 && (
          <>
            <div className="space-y-4">
              <label className="block text-sm font-medium text-gray-700">
                {t('login.phoneNumber')}
              </label>
              <input
                type="tel"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value.replace(/\D/g, ''))}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder={t('login.phoneNumber')}
                maxLength="10"
              />
            </div>
            <button
              onClick={handleGetOtp}
              disabled={loading || !phoneNumber || phoneNumber.length !== 10}
              className="w-full px-4 py-2 bg-primary-600 text-white font-medium rounded-md disabled:opacity-50 hover:bg-primary-700 transition-colors"
            >
              {loading ? t('common.loading') : t('login.getOtp')}
            </button>
          </>
        )}
        
        {step === 2 && (
          <>
            <p className="text-center text-gray-600">
              {t('login.otp')} {/* We assume there's an OTP sent message */}
            </p>
            <div className="space-y-4">
              <label className="block text-sm font-medium text-gray-700">
                {t('login.otp')}
              </label>
              <input
                type="text"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="______"
                maxLength="6"
              />
            </div>
            <button
              onClick={handleVerifyOtp}
              disabled={loading || otp.length !== 6}
              className="w-full px-4 py-2 bg-primary-600 text-white font-medium rounded-md disabled:opacity-50 hover:bg-primary-700 transition-colors"
            >
              {loading ? t('common.loading') : t('login.verify')}
            </button>
            <p className="text-xs text-gray-500 text-center">
              {t('login.dontHaveAccount')} 
              <span className="text-primary-600 cursor-pointer" onClick={() => navigate('/signup')}>
                {t('login.signUp')}
              </span>
            </p>
          </>
        )}
        
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 mb-4">
            {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default Login;
