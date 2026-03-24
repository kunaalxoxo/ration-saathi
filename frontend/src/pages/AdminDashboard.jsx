import React from 'react';
import { useTranslation } from 'react-i18next';

const AdminDashboard = () => {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">
        {t('admin.dashboardTitle', { defaultValue: 'Admin Dashboard' })}
      </h1>
      <div className="bg-white shadow rounded-lg p-6">
        <p className="text-gray-600">
          Welcome to the Administrative Dashboard. Detailed analytics and case management tools will be available here.
        </p>
      </div>
    </div>
  );
};

export default AdminDashboard;
