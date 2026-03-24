import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { authApi } from '../lib/api';
import { useNavigate } from 'react-router-dom';

const Login: React.FC = () => {
  const { t } = useTranslation();
  const nav = useNavigate();
  const [p, setP] = useState('');
  const [o, setO] = useState('');
  const [s, setS] = useState<'phone' | 'otp'>('phone');
  const [e, setE] = useState('');

  const hReq = async (ev: React.FormEvent) => {
    ev.preventDefault();
    try {
      await authApi.requestOtp(p);
      setS('otp');
      setE('');
    } catch {
      setE(t('error'));
    }
  };

  const hVer = async (ev: React.FormEvent) => {
    ev.preventDefault();
    try {
      const { data } = await authApi.verifyOtp(p, o);
      localStorage.setItem('token', data.token);
      nav('/');
    } catch {
      setE(t('error'));
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-green-600">{t('common.app_name')}</h1>
          <p className="text-gray-500 mt-2">{t('login.title')}</p>
        </div>
        {e && <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">{e}</div>}
        <form onSubmit={s === 'phone' ? hReq : hVer}>
          {s === 'phone' ? (
            <div className="space-y-4">
              <label className="block text-sm font-medium text-gray-700">{t('login.phone_label')}</label>
              <input
                type="tel"
                value={p}
                onChange={(ev) => setP(ev.target.value)}
                className="w-full p-4 border rounded-xl focus:ring-2 focus:ring-green-500 outline-none text-lg"
                placeholder="99XXXXXXXX"
                required
              />
              <button className="w-full bg-green-600 text-white p-4 rounded-xl font-bold text-lg hover:bg-green-700 transition">
                {t('login.get_otp')}
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <label className="block text-sm font-medium text-gray-700">{t('login.otp_label')}</label>
              <input
                type="text"
                value={o}
                onChange={(ev) => setO(ev.target.value)}
                className="w-full p-4 border rounded-xl focus:ring-2 focus:ring-green-500 outline-none text-center text-2xl tracking-widest"
                maxLength={6}
                required
              />
              <button className="w-full bg-green-600 text-white p-4 rounded-xl font-bold text-lg hover:bg-green-700 transition">
                {t('login.verify_otp')}
              </button>
            </div>
          )}
        </form>
      </div>
    </div>
  );
};

export default Login;
