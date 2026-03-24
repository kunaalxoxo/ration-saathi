import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';

const CaseTracker = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  
  const [caseNumber, setCaseNumber] = useState('');
  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTrackCase = async () => {
    if (!caseNumber) {
      setError('Please enter a case number.');
      return;
    }
    
    setLoading(true);
    setError('');
    setCaseData(null);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      const dummyCase = {
        caseNumber: caseNumber,
        status: 'under_investigation',
        issueType: 'Short Supply',
        dateReported: '2025-10-15',
        lastUpdate: '2025-10-18',
        updates: [
          { date: '2025-10-18', text: 'Official assigned to investigate the FPS.' },
          { date: '2025-10-15', text: 'Grievance registered and sent to Block Officer.' }
        ]
      };
      
      setCaseData(dummyCase);
    } catch (err) {
      setError('Could not find case details. Please check the number.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'open': return 'bg-blue-100 text-blue-700';
      case 'under_investigation': return 'bg-orange-100 text-orange-700';
      case 'resolved': return 'bg-green-100 text-green-700';
      default: return 'bg-gray-100 text-gray-700';
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
            <h1 className="text-xl font-bold text-green-700">Track Grievance</h1>
          </div>
        </div>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-sm border p-6">
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-1">Case Number</label>
            <div className="flex space-x-2">
              <input
                type="text"
                value={caseNumber}
                onChange={(e) => setCaseNumber(e.target.value.toUpperCase())}
                className="flex-1 px-4 py-2 border rounded-md outline-none focus:ring-2 focus:ring-green-500"
                placeholder="e.g. RS-RJ-123456"
              />
              <button
                onClick={handleTrackCase}
                disabled={loading || !caseNumber}
                className="px-6 py-2 bg-green-600 text-white font-bold rounded-md hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? 'Tracking...' : 'Track'}
              </button>
            </div>
          </div>

          {error && <div className="p-4 bg-red-50 text-red-700 rounded-md mb-6">{error}</div>}

          {caseData && (
            <div className="space-y-6">
              <div className="flex justify-between items-start border-b pb-4">
                <div>
                  <h3 className="text-lg font-bold">{caseData.caseNumber}</h3>
                  <p className="text-sm text-gray-500">Reported on {caseData.dateReported}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${getStatusColor(caseData.status)}`}>
                  {caseData.status.replace('_', ' ')}
                </span>
              </div>

              <div>
                <h4 className="font-bold mb-3">Timeline</h4>
                <div className="relative pl-8 space-y-6">
                  <div className="absolute left-3 top-0 bottom-0 w-0.5 bg-gray-200"></div>
                  {caseData.updates.map((update, idx) => (
                    <div key={idx} className="relative">
                      <div className="absolute -left-8 top-1.5 w-4 h-4 rounded-full bg-green-500 border-4 border-white"></div>
                      <p className="text-xs text-gray-400 font-medium mb-1">{update.date}</p>
                      <p className="text-sm text-gray-700">{update.text}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default CaseTracker;
