import React from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { ClipboardCheck, MessageSquarePlus, Search, BarChart3 } from 'lucide-react';

const Home: React.FC = () => {
  const { t } = useTranslation();
  const m = [
    {
      t: 'dashboard.check_entitlement',
      i: ClipboardCheck,
      l: '/check',
      c: 'bg-blue-100 text-blue-600'
    },
    {
      t: 'dashboard.lodge_complaint',
      i: MessageSquarePlus,
      l: '/lodge',
      c: 'bg-orange-100 text-orange-600'
    },
    {
      t: 'dashboard.track_case',
      i: Search,
      l: '/track',
      c: 'bg-purple-100 text-purple-600'
    },
    {
      t: 'dashboard.village_report',
      i: BarChart3,
      l: '/admin',
      c: 'bg-green-100 text-green-600'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-4 pb-20">
      <header className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800">{t('common.app_name')}</h1>
        <p className="text-gray-500">Namaste, CSC Operator</p>
      </header>
      <div className="grid grid-cols-2 gap-4">
        {m.map((i) => (
          <Link
            key={i.l}
            to={i.l}
            className="bg-white p-6 rounded-2xl shadow-sm flex flex-col items-center text-center space-y-3 hover:shadow-md transition"
          >
            <div className={`p-4 rounded-full ${i.c}`}>
              <i.i size={32} />
            </div>
            <span className="font-semibold text-gray-700 leading-tight">{t(i.t)}</span>
          </Link>
        ))}
      </div>
      <div className="mt-8 bg-green-600 rounded-2xl p-6 text-white">
        <h2 className="text-lg font-bold mb-2">Today's Activity</h2>
        <div className="flex justify-between items-center">
          <div>
            <p className="text-green-100 text-sm">Cases Filed</p>
            <p className="text-2xl font-bold">12</p>
          </div>
          <div className="h-10 w-px bg-green-500"></div>
          <div>
            <p className="text-green-100 text-sm">Pending</p>
            <p className="text-2xl font-bold">4</p>
          </div>
          <div className="h-10 w-px bg-green-500"></div>
          <div>
            <p className="text-green-100 text-sm">Resolved</p>
            <p className="text-2xl font-bold">8</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
