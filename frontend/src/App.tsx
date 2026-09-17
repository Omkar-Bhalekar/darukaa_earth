import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from '@/auth/ProtectedRoute';
import { AuthProvider } from '@/auth/AuthContext';
import { Login } from '@/pages/Login';
import { Register } from '@/pages/Register';
import { Dashboard } from '@/pages/Dashboard';
import { ProjectCreate } from '@/pages/ProjectCreate';
import { ProjectDetail } from '@/pages/ProjectDetail';
import { MapExplorer } from '@/pages/MapExplorer';
import { SiteDetail } from '@/pages/SiteDetail';

const AppRoutes = () => (
  <Routes>
    <Route path="/" element={<Navigate to="/dashboard" replace />} />
    <Route path="/login" element={<Login />} />
    <Route path="/register" element={<Register />} />
    <Route element={<ProtectedRoute />}>
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/projects/new" element={<ProjectCreate />} />
      <Route path="/projects/:id" element={<ProjectDetail />} />
      <Route path="/map" element={<MapExplorer />} />
      <Route path="/sites/:id" element={<SiteDetail />} />
    </Route>
  </Routes>
);

export const App = () => (
  <AuthProvider>
    <AppRoutes />
  </AuthProvider>
);

export default App;
