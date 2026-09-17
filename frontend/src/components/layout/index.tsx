import React from 'react';

// Simplified layout files
export const TopBar: React.FC = () => (
  <header className="h-16 bg-white border-b border-sage-light/20 flex items-center justify-between px-6 sticky top-0 z-20">
    <div className="text-sm text-sage font-medium">Dashboard</div>
    <div className="flex items-center gap-3">
      <div className="h-8 w-8 rounded-full bg-forest-green text-off-white flex items-center justify-center text-sm font-semibold">U</div>
    </div>
  </header>
);

export const Sidebar: React.FC = () => (
  <aside className="w-64 bg-forest-green text-off-white flex flex-col hidden md:flex min-h-screen">
    <div className="h-16 flex items-center px-6 font-heading font-bold text-xl tracking-tight border-b border-white/10">
      Darukaa.Earth
    </div>
    <nav className="flex-1 px-4 py-6 flex flex-col gap-2">
      <a href="/dashboard" className="px-4 py-2 bg-sage/40 rounded-lg font-medium">Dashboard</a>
      <a href="/map" className="px-4 py-2 hover:bg-sage/20 rounded-lg font-medium smooth-transition">Map Explorer</a>
    </nav>
  </aside>
);

export const PageShell: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="flex h-screen overflow-hidden bg-off-white">
    <Sidebar />
    <div className="flex-1 flex flex-col overflow-hidden">
      <TopBar />
      <main className="flex-1 overflow-y-auto p-6">
        {children}
      </main>
    </div>
  </div>
);
