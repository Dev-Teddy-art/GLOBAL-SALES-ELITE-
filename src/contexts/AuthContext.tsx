import React, { createContext, useContext, useState, useEffect } from 'react';
import { sanityClient } from '../lib/sanity';

export interface UserProfile {
  id?: string;
  email?: string;
  name?: string;
  role?: string;
  avatarUrl?: string;
  [key: string]: any;
}

interface AuthContextType {
  user: any;
  profile: UserProfile | null;
  login: (email: string, pass: string) => Promise<any>;
  signIn: (email: string, pass: string) => Promise<any>;
  signInWithEmail: (email: string, pass: string) => Promise<any>;
  signup: (...args: any[]) => Promise<any>;
  signUp: (...args: any[]) => Promise<any>;
  signUpWithEmail: (...args: any[]) => Promise<any>;
  register: (...args: any[]) => Promise<any>;
  createAccount: (...args: any[]) => Promise<any>;
  logout: () => void;
  signOut: () => void;
  updateProfile: (updatedData: Partial<UserProfile>) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('gse_user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (e) {
        localStorage.removeItem('gse_user');
      }
    }
  }, []);

  const authenticateUser = async (email: string, pass: string) => {
    try {
      const query = `*[_type == "user" && email == $email][0]`;
      const foundUser = await sanityClient.fetch(query, { email: email.toLowerCase() });

      if (!foundUser) {
        throw new Error('No user account found with this email address.');
      }

      if (foundUser.password && foundUser.password !== pass) {
        throw new Error('Invalid email or password.');
      }

      setUser(foundUser);
      localStorage.setItem('gse_user', JSON.stringify(foundUser));
      return foundUser;
    } catch (err: any) {
      throw new Error(err.message || 'Authentication failed');
    }
  };

  const registerUser = async (...args: any[]) => {
    try {
      let userData: any = {};
      if (typeof args[0] === 'object' && args[0] !== null) {
        userData = args[0];
      } else {
        const [email, password, name, referralCode] = args;
        userData = { email, password, name, referralCode };
      }

      const newUserDoc = {
        _type: 'user',
        ...userData,
        createdAt: new Date().toISOString(),
      };

      const createdUser = await sanityClient.create(newUserDoc);
      setUser(createdUser);
      localStorage.setItem('gse_user', JSON.stringify(createdUser));
      return createdUser;
    } catch (err: any) {
      throw new Error(err.message || 'Registration failed');
    }
  };

  const updateProfile = async (updatedData: Partial<UserProfile>) => {
    const updated = { ...user, ...updatedData };
    setUser(updated);
    localStorage.setItem('gse_user', JSON.stringify(updated));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('gse_user');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        profile: user,
        login: authenticateUser,
        signIn: authenticateUser,
        signInWithEmail: authenticateUser,
        signup: registerUser,
        signUp: registerUser,
        signUpWithEmail: registerUser,
        register: registerUser,
        createAccount: registerUser,
        logout,
        signOut: logout,
        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
