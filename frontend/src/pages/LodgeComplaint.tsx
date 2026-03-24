import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { casesApi } from '../lib/api';
import { ArrowLeft, CheckCircle } from 'lucide-react';
import { Link, useSearchParams } from 'react-router-dom';

const LodgeComplaint: React.FC = () => {
  const { t } = useTranslation();
  const [sP] = useSearchParams();
  const [fD, setFD] = useState({
    card_number: sP.get('card') || '',
    issue_type: 'short_supply',
    received_wheat: '',
    received_rice: '',
    phone: ''
  });
  const [suc, setSuc] = useState<string | null>(null);

  const hS = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const { data } = await casesApi.create(fD);
      setSuc(data.case_number);
    } catch {
      alert(t('error'));
    }
  };

  if (suc) {
    return (
      <div className="min-h-screen flex items-center justify-center p-6 bg-white">
        <div className="text-center space-y-6">
          <div className="flex justify-center">
            <CheckCircle size={80} className="text-green-500" />
          </div>
          <h1 className="text-2xl font-bold text-gray-800">{t('complaint.success')}</h1>
          <div className="bg-gray-100 p-6 rounded-2xl border-2 border-dashed border-gray-300">
            <p className="text-sm text-gray-500 mb-1">Reference Number</p>
            <p className="text-3xl font-black text-green-700 tracking-tight">{suc}</p>
          </div>
          <Link to="/" className="block w-full bg-green-600 text-white p-4 rounded-xl font-bold">
            Done
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <Link to="/" className="inline-flex items-center text-gray-500 mb-6">
        <ArrowLeft size={20} className="mr-2" /> {t('common.back')}
      </Link>
      <h1 className="text-2xl font-bold mb-6">{t('complaint.title')}</h1>
      <form onSubmit={hS} className="space-y-6">
        <div className="bg-white p-6 rounded-2xl shadow-sm space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Card Number</label>
            <input
              type="text"
              required
              value={fD.card_number}
              onChange={(e) => setFD({ ...fD, card_number: e.target.value })}
              className="w-full p-4 border rounded-xl outline-none"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
            <input
              type="tel"
              required
              value={fD.phone}
              onChange={(e) => setFD({ ...fD, phone: e.target.value })}
              className="w-full p-4 border rounded-xl outline-none"
            />
          </div>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm">
          <label className="block text-sm font-medium text-gray-700 mb-4">{t('complaint.issue_type')}</label>
          <div className="grid grid-cols-2 gap-3">
            {['short_supply', 'denial', 'quality', 'weighing'].map((ty) => (
              <button
                key={ty}
                type="button"
                onClick={() => setFD({ ...fD, issue_type: ty })}
                className={`p-4 rounded-xl text-sm font-medium border-2 ${
                  fD.issue_type === ty ? 'border-green-600 bg-green-50' : 'border-gray-100 bg-gray-50'
                }`}
              >
                {t(`complaint.${ty}`)}
              </button>
            ))}
          </div>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Wheat (KG)</label>
            <input
              type="number"
              required
              value={fD.received_wheat}
              onChange={(e) => setFD({ ...fD, received_wheat: e.target.value })}
              className="w-full p-4 border rounded-xl outline-none"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Rice (KG)</label>
            <input
              type="number"
              required
              value={fD.received_rice}
              onChange={(e) => setFD({ ...fD, received_rice: e.target.value })}
              className="w-full p-4 border rounded-xl outline-none"
            />
          </div>
        </div>
        <button type="submit" className="w-full bg-green-600 text-white p-5 rounded-2xl font-bold text-lg">
          Lodge Grievance
        </button>
      </form>
    </div>
  );
};

export default LodgeComplaint;
