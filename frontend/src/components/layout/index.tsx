import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '@/auth/AuthContext';

export const TopBar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const onLogout = async () => {
    await logout();
    navigate('/login');
  };

  const initial = (user?.name || user?.email || 'U').charAt(0).toUpperCase();

  return (
    <header className="h-16 bg-white border-b border-sage-light/20 flex items-center justify-between px-6 sticky top-0 z-20">
      <div className="text-sm text-sage font-medium">
        Carbon and biodiversity operations
      </div>
      <div className="flex items-center gap-3">
        <span className="hidden sm:block text-sm text-charcoal/70">
          {user?.name}
        </span>
        <div className="h-8 w-8 rounded-full bg-forest-green text-off-white flex items-center justify-center text-sm font-semibold">
          {initial}
        </div>
        <button
          type="button"
          onClick={onLogout}
          className="text-sm text-charcoal/70 hover:text-forest-green"
        >
          Log out
        </button>
      </div>
    </header>
  );
};

const navClass = ({ isActive }: { isActive: boolean }) =>
  `px-4 py-2 rounded-lg font-medium smooth-transition ${isActive ? 'bg-sage/40' : 'hover:bg-sage/20'}`;

export const Sidebar: React.FC = () => (
  <aside className="w-64 bg-forest-green text-off-white flex-col hidden md:flex min-h-screen">
    <div className="h-16 flex items-center px-6 font-heading font-bold text-xl tracking-tight border-b border-white/10">
      Darukaa.Earth
    </div>
    <nav className="flex-1 px-4 py-6 flex flex-col gap-2">
      <NavLink to="/dashboard" className={navClass}>
        Dashboard
      </NavLink>
      <NavLink to="/map" className={navClass}>
        Map Explorer
      </NavLink>
      <NavLink to="/projects/new" className={navClass}>
        New project
      </NavLink>
    </nav>
  </aside>
);

export const PageShell: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => (
  <div className="flex h-screen overflow-hidden bg-off-white">
    <Sidebar />
    <div className="flex-1 flex flex-col overflow-hidden">
      <TopBar />
      <main className="flex-1 overflow-y-auto p-6">{children}</main>
    </div>
  </div>
);
