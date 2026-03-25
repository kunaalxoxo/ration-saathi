import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import EntitlementCheck from './pages/EntitlementCheck';
import LodgeComplaint from './pages/LodgeComplaint';
import CaseTracker from './pages/CaseTracker';
import MyVillageReport from './pages/MyVillageReport';
import AdminDashboard from './pages/AdminDashboard';
import Layout from './components/Layout';
import { useAuth } from './lib/authContext';

function App() {
  const { user } = useAuth();

  return (
    <Routes>
      <Route path="/" element={<Navigate replace to="/login" />} />
      <Route path="/login" element={<Login />} />
      
      {/* Protected routes wrapped in Layout */}
      <Route
        path="/home"
        element={
          user ? <Layout><Home /></Layout> : <Navigate replace to="/login" />
        }
      />
      <Route
        path="/entitlement-check"
        element={
          user ? <Layout><EntitlementCheck /></Layout> : <Navigate replace to="/login" />
        }
      />
      <Route
        path="/lodge-complaint"
        element={
          user ? <Layout><LodgeComplaint /></Layout> : <Navigate replace to="/login" />
        }
      />
      <Route
        path="/case-tracker"
        element={
          user ? <Layout><CaseTracker /></Layout> : <Navigate replace to="/login" />
        }
      />
      <Route
        path="/my-village-report"
        element={
          user ? <Layout><MyVillageReport /></Layout> : <Navigate replace to="/login" />
        }
      />
      <Route
        path="/admin"
        element={
          user && (user.role === 'district_admin' || user.role === 'state_admin' || user.role === 'super_admin')
            ? <Layout><AdminDashboard /></Layout>
            : <Navigate replace to="/home" />
        }
      />
      
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

export default App;
