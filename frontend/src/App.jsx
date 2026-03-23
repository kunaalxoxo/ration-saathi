import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import EntitlementCheck from './pages/EntitlementCheck';
import LodgeComplaint from './pages/LodgeComplaint';
import CaseTracker from './pages/CaseTracker';
import MyVillageReport from './pages/MyVillageReport';
import AdminDashboard from './pages/AdminDashboard';
import { useAuth } from './lib/authContext';

function App() {
  const { user } = useAuth();

  return (
    <Routes>
      <Route path="/" element={<Navigate replace to="/login" />} />
      <Route path="/login" element={<Login />} />
      {/* Protected routes */}
      <Route
        path="/home"
        element={
          user ? <Home /> : <Navigate replace to="/login" />
        }
      />
      <Route
        path="/entitlement-check"
        element={
          user ? <EntitlementCheck /> : <Navigate replace to="/login" />
        }
      />
      <Route
        path="/lodge-complaint"
        element={
          user ? <LodgeComplaint /> : <Navigate replace to="/login" />
        }
      />
      <Route
        path="/case-tracker"
        element={
          user ? <CaseTracker /> : <Navigate replace to="/login" />
        }
      />
      <Route
        path="/my-village-report"
        element={
          user ? <MyVillageReport /> : <Navigate replace to="/login" />
        }
      />
      <Route
        path="/admin"
        element={
          user && (user.role === 'district_admin' || user.role === 'state_admin' || user.role === 'super_admin')
            ? <AdminDashboard />
            : <Navigate replace to="/home" />
        }
      />
      {/* Fallback for not found */}
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

export default App;
