import React, { createContext, useContext, useEffect, useState } from 'react';
import { User } from '@/types';
import { api } from '@/api/endpoints';

type Credentials = { email: string; password: string };
type Registration = Credentials & { name: string };

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (data: Credentials) => Promise<void>;
  register: (data: Registration) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      try {
        const userData = await api.auth.getMe();
        setUser(userData);
      } catch (error) {
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };
    initAuth();
  }, []);

  const login = async (data: Credentials) => {
    await api.auth.login(data);
    const userData = await api.auth.getMe();
    setUser(userData);
  };

  const register = async (data: Registration) => {
    await api.auth.register(data);
    const userData = await api.auth.getMe();
    setUser(userData);
  };

  const logout = async () => {
    await api.auth.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, isAuthenticated: !!user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
