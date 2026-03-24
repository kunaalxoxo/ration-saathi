import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/authContext';

const MyVillageReport = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  useEffect(() => {
    if (!user) {
      navigate('/login');
    } else {
      fetchReport();
    }
  }, [user, navigate]);
  
  const fetchReport = async () => {
    setLoading(true);
    setError('');
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const dummyData = {
        villageName: "Shyamgarh",
        totalRationCards: 120,
        activeCards: 110,
        totalCasesThisMonth: 8,
        resolvedCases: 5,
        pendingCases: 3,
        fpsPerformance: [
          { fpsCode: 'RJ-BA-001', name: 'Shri Ram FPS', complaints: 2, resolutionRate: 80 },
          { fpsCode: 'RJ-BA-002', name: 'Krishna FPS', complaints: 0, resolutionRate: 100 },
          { fpsCode: 'RJ-BA-003', name: 'Shiv Shakti FPS', complaints: 4, resolutionRate: 60 }
        ]
      };
      
      setReportData(dummyData);
    } catch (err) {
      setError('Failed to load village report.');
    } finally {
      setLoading(false);
    }
  };
  
  if (!user) return null;

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
            <h1 className="text-xl font-bold text-green-700">Village Report</h1>
          </div>
        </div>
      </header>
      
      <main className="max-w-5xl mx-auto px-4 py-8">
        {loading && <p className="text-center text-gray-500">Loading village statistics...</p>}
        {error && <div className="p-4 bg-red-50 text-red-700 rounded-md mb-6">{error}</div>}
        
        {reportData && (
          <div className="space-y-8">
            <div className="bg-white rounded-xl shadow-sm border p-6">
              <h3 className="text-lg font-bold mb-6">Overview: {reportData.villageName}</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="p-4 bg-blue-50 rounded-lg text-center">
                  <p className="text-xs text-blue-600 font-bold uppercase mb-1">Total Cards</p>
                  <p className="text-2xl font-bold text-blue-900">{reportData.totalRationCards}</p>
                </div>
                <div className="p-4 bg-green-50 rounded-lg text-center">
                  <p className="text-xs text-green-600 font-bold uppercase mb-1">Active</p>
                  <p className="text-2xl font-bold text-green-900">{reportData.activeCards}</p>
                </div>
                <div className="p-4 bg-orange-50 rounded-lg text-center">
                  <p className="text-xs text-orange-600 font-bold uppercase mb-1">Grievances</p>
                  <p className="text-2xl font-bold text-orange-900">{reportData.totalCasesThisMonth}</p>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg text-center">
                  <p className="text-xs text-purple-600 font-bold uppercase mb-1">Resolved</p>
                  <p className="text-2xl font-bold text-purple-900">{reportData.resolvedCases}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
              <h3 className="text-lg font-bold p-6 border-b">FPS Performance</h3>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 text-left">
                    <tr>
                      <th className="px-6 py-3 text-xs font-bold text-gray-500 uppercase">FPS Code</th>
                      <th className="px-6 py-3 text-xs font-bold text-gray-500 uppercase">Name</th>
                      <th className="px-6 py-3 text-xs font-bold text-gray-500 uppercase">Complaints</th>
                      <th className="px-6 py-3 text-xs font-bold text-gray-500 uppercase">Resolution</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y">
                    {reportData.fpsPerformance.map((fps) => (
                      <tr key={fps.fpsCode}>
                        <td className="px-6 py-4 text-sm font-medium text-gray-900">{fps.fpsCode}</td>
                        <td className="px-6 py-4 text-sm text-gray-600">{fps.name}</td>
                        <td className="px-6 py-4 text-sm text-gray-600">{fps.complaints}</td>
                        <td className="px-6 py-4 text-sm">
                          <span className={`px-2 py-1 rounded text-xs font-bold ${fps.resolutionRate >= 80 ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'}`}>
                            {fps.resolutionRate}%
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default MyVillageReport;
