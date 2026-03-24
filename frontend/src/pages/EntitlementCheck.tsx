import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { entitlementApi } from '../lib/api';
import { ArrowLeft, User, Users, Calendar } from 'lucide-react';
import { Link } from 'react-router-dom';

const EntitlementCheck: React.FC = () => {
  const { t } = useTranslation();
  const [cn, setCn] = useState('');
  const [res, setRes] = useState<any>(null);
  const [l, setL] = useState(false);

  const hC = async () => {
    setL(true);
    try {
      const { data } = await entitlementApi.check(cn);
      setRes(data.data);
    } catch {
      setRes('NOT_FOUND');
    } finally {
      setL(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <Link to="/" className="inline-flex items-center text-gray-500 mb-6">
        <ArrowLeft size={20} className="mr-2" /> {t('common.back')}
      </Link>
      <h1 className="text-2xl font-bold mb-6">{t('entitlement.title')}</h1>
      <div className="bg-white rounded-2xl p-6 shadow-sm mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">{t('entitlement.input_label')}</label>
        <div className="flex space-x-2">
          <input
            type="text"
            value={cn}
            onChange={(e) => setCn(e.target.value)}
            className="flex-1 p-4 border rounded-xl focus:ring-2 focus:ring-green-500 outline-none"
            placeholder="RCXXXXXXXXXX"
          />
          <button onClick={hC} disabled={l} className="bg-green-600 text-white px-6 rounded-xl font-bold">
            {l ? '...' : 'Go'}
          </button>
        </div>
      </div>
      {res && res !== 'NOT_FOUND' && (
        <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4">
          <div className="bg-white rounded-2xl p-6 shadow-sm">
            <div className="flex items-center mb-4">
              <div className="p-3 bg-green-50 rounded-full mr-4 text-green-600">
                <User size={24} />
              </div>
              <div>
                <p className="text-sm text-gray-500">Head of Household</p>
                <p className="text-xl font-bold">{res.head_name}</p>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-gray-50 rounded-xl">
                <p className="text-xs text-gray-500 mb-1">Members</p>
                <p className="font-bold flex items-center">
                  <Users size={16} className="mr-2" /> {res.total_members}
                </p>
              </div>
              <div className="p-4 bg-gray-50 rounded-xl">
                <p className="text-xs text-gray-500 mb-1">Category</p>
                <p className="font-bold text-orange-600">{res.category}</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-2xl p-6 shadow-sm border-t-4 border-green-600">
            <h3 className="font-bold mb-4 flex items-center text-gray-800">
              <Calendar size={18} className="mr-2" /> {t('entitlement.allocated')}
            </h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center p-4 border rounded-xl bg-gray-50">
                <span className="font-medium">{t('entitlement.wheat')}</span>
                <span className="text-xl font-bold text-green-700">{res.allocation.wheat} KG</span>
              </div>
              <div className="flex justify-between items-center p-4 border rounded-xl bg-gray-50">
                <span className="font-medium">{t('entitlement.rice')}</span>
                <span className="text-xl font-bold text-green-700">{res.allocation.rice} KG</span>
              </div>
            </div>
          </div>
          <Link
            to={`/lodge?card=${cn}`}
            className="block w-full text-center bg-orange-50 text-orange-600 p-4 rounded-xl font-bold border border-orange-200"
          >
            Kam mila? Shikayat karein
          </Link>
        </div>
      )}
    </div>
  );
};

export default EntitlementCheck;
