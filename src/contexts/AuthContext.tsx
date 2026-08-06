import React, { createContext, useContext, useEffect, useState } from 'react';

export interface UserProfile {
  _id: string;
  email: string;
  displayName: string;
  role: 'admin' | 'user';
  sponsorId: string;
  referralCode: string;
  createdAt: string;
  isAdmin?: boolean;
  firstName?: string;
  lastName?: string;
  address?: string;
  bankAccountNumber?: string;
  bankAccountName?: string;
  bankName?: string;
  lft?: number;
  rgt?: number;
  lastLoginAt?: string;
  profileImage?: string;
  avatarUrl?: string;
  notifications?: { id: string; message: string; read: boolean; createdAt: string; }[];
}

interface AuthContextType {
  user: any | null;
  profile: UserProfile | null;
  loading: boolean;
  signUpWithEmail: (password: string, extraData: Partial<UserProfile>) => Promise<void>;
  signInWithEmail: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  updateProfile: (updates: Partial<UserProfile>) => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  profile: null,
  loading: true,
  signUpWithEmail: async () => {},
  signInWithEmail: async () => {},
  signOut: async () => {},
});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<any | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUserId = localStorage.getItem('userId');
    if (storedUserId) {
      fetch(`/api/auth/me?id=${storedUserId}`)
        .then(res => res.json())
        .then(data => {
          if (data.user) {
            setUser({ uid: data.user._id, email: data.user.email });
            setProfile(data.user);
          } else {
            localStorage.removeItem('userId');
          }
        })
        .catch(err => console.error(err))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const signUpWithEmail = async (password: string, extraData: Partial<UserProfile>) => {
    const res = await fetch('/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password, extraData })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to sign up');
    
    localStorage.setItem('userId', data.user._id);
    setUser({ uid: data.user._id, email: data.user.email });
    setProfile(data.user);
  };

  const signInWithEmail = async (email: string, password: string) => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to sign in');

    localStorage.setItem('userId', data.user._id);
    setUser({ uid: data.user._id, email: data.user.email });
    setProfile(data.user);
  };

  const updateProfile = (updates: Partial<UserProfile>) => {
    setProfile(prev => prev ? { ...prev, ...updates } : null);
  };

  const signOut = async () => {
    localStorage.removeItem('userId');
    setUser(null);
    setProfile(null);
  };

  return (
    <AuthContext.Provider value={{ user, profile, loading, signUpWithEmail, signInWithEmail, signOut, updateProfile }}>
      {children}
    </AuthContext.Provider>
  );
};
