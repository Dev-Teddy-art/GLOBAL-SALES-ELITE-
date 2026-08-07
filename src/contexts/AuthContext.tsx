import React, { createContext, useContext, useState, useEffect } from 'react';
import { sanityClient } from '../lib/sanity';

export interface UserProfile {
  _id?: string;
  id?: string;
  email?: string;
  name?: string;
  firstName?: string;
  lastName?: string;
  role?: string;
  avatarUrl?: string;
  [key: string]: any;
}

interface AuthContextType {
  user: any;
  profile: UserProfile | null;
  isNewUser: boolean;
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
  const [isNewUser, setIsNewUser] = useState<boolean>(false);

  const formatUserData = (userData: any) => {
    if (!userData) return null;
    const computedName =
      userData.name ||
      (userData.firstName && userData.lastName
        ? `${userData.firstName} ${userData.lastName}`
        : userData.firstName || userData.lastName || userData.email?.split('@')[0] || 'Member');

    return {
      ...userData,
      name: computedName,
      firstName: userData.firstName || computedName.split(' ')[0] || '',
      lastName: userData.lastName || computedName.split(' ')[1] || '',
    };
  };

  useEffect(() => {
    const storedUser = localStorage.getItem('gse_user');
    if (storedUser) {
      try {
        const parsed = JSON.parse(storedUser);
        setUser(formatUserData(parsed));
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

      const formatted = formatUserData(foundUser);
      setIsNewUser(false);
      setUser(formatted);
      localStorage.setItem('gse_user', JSON.stringify(formatted));
      return formatted;
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
        const [email, password, firstName, lastName, referralCode] = args;
        userData = { email, password, firstName, lastName, referralCode };
      }

      const computedName =
        userData.name ||
        (userData.firstName && userData.lastName
          ? `${userData.firstName} ${userData.lastName}`
          : userData.firstName || userData.email?.split('@')[0]);

      const newUserDoc = {
        _type: 'user',
        ...userData,
        name: computedName,
        createdAt: new Date().toISOString(),
      };

      const createdUser = await sanityClient.create(newUserDoc);
      const formatted = formatUserData(createdUser);
      setIsNewUser(true);
      setUser(formatted);
      localStorage.setItem('gse_user', JSON.stringify(formatted));
      return formatted;
    } catch (err: any) {
      throw new Error(err.message || 'Registration failed');
    }
  };

  const updateProfile = async (updatedData: Partial<UserProfile>) => {
    try {
      const targetId = user?._id || user?.id;
      const mergedLocal = formatUserData({ ...user, ...updatedData });

      if (targetId) {
        await sanityClient
          .patch(targetId)
          .set({ ...updatedData, name: mergedLocal.name })
          .commit();
      }

      setUser(mergedLocal);
      localStorage.setItem('gse_user', JSON.stringify(mergedLocal));
    } catch (err: any) {
      const mergedLocal = formatUserData({ ...user, ...updatedData });
      setUser(mergedLocal);
      localStorage.setItem('gse_user', JSON.stringify(mergedLocal));
    }
  };

  const logout = () => {
    setUser(null);
    setIsNewUser(false);
    localStorage.removeItem('gse_user');
  };

  const activeUser = formatUserData(user);

  return (
    <AuthContext.Provider
      value={{
        user: activeUser,
        profile: activeUser,
        isNewUser,
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
