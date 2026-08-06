import re

with open('src/contexts/AuthContext.tsx', 'r') as f:
    content = f.read()

new_content = """import React, { createContext, useContext, useEffect, useState } from 'react';
import { sanityClient } from '../lib/sanity';
import bcrypt from 'bcryptjs';

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
}

interface AuthContextType {
  user: any | null;
  profile: UserProfile | null;
  loading: boolean;
  signUpWithEmail: (password: string, extraData: Partial<UserProfile>) => Promise<void>;
  signInWithEmail: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
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
      sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: storedUserId })
        .then(userDoc => {
          if (userDoc) {
            setUser({ uid: userDoc._id, email: userDoc.email });
            setProfile(userDoc);
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
    // 1. Check if email exists
    const existing = await sanityClient.fetch(`*[_type == "user" && email == $email][0]`, { email: extraData.email });
    if (existing) {
      throw new Error("An account with this email already exists. Please log in.");
    }

    const salt = bcrypt.genSaltSync(10);
    const passwordHash = bcrypt.hashSync(password, salt);

    let finalRole = 'user';
    let finalSponsorId = extraData.sponsorId || 'admin';

    if (extraData.email === 'mypropteeapp@gmail.com') {
      finalRole = 'admin';
      finalSponsorId = 'admin';
    }

    let parentRgt = 0;
    let newLft = 1;
    let newRgt = 2;

    if (finalSponsorId !== 'admin') {
      const parentUser = await sanityClient.fetch(`*[_type == "user" && referralCode == $code][0]`, { code: finalSponsorId });
      if (parentUser) {
        parentRgt = parentUser.rgt || 0;
      } else {
        const parentById = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: finalSponsorId });
        if (parentById) {
          parentRgt = parentById.rgt || 0;
        } else {
           const maxRgtUser = await sanityClient.fetch(`*[_type == "user"] | order(rgt desc)[0]`);
           if (maxRgtUser) {
             parentRgt = (maxRgtUser.rgt || 0) + 1;
           }
        }
      }
    } else {
      const maxRgtUser = await sanityClient.fetch(`*[_type == "user"] | order(rgt desc)[0]`);
      if (maxRgtUser) {
        parentRgt = (maxRgtUser.rgt || 0) + 1;
      }
    }

    if (parentRgt > 0) {
      newLft = parentRgt;
      newRgt = parentRgt + 1;

      // Update nested set for existing nodes
      const shiftLftQuery = await sanityClient.fetch(`*[_type == "user" && lft > $rgt]`, { rgt: parentRgt });
      const shiftRgtQuery = await sanityClient.fetch(`*[_type == "user" && rgt >= $rgt]`, { rgt: parentRgt });
      
      const transaction = sanityClient.transaction();
      
      shiftLftQuery.forEach((doc: any) => {
         transaction.patch(doc._id, p => p.inc({ lft: 2 }));
      });
      
      shiftRgtQuery.forEach((doc: any) => {
         transaction.patch(doc._id, p => p.inc({ rgt: 2 }));
      });
      
      await transaction.commit();
    }

    const newUserDoc = {
      _type: 'user',
      email: extraData.email,
      passwordHash,
      displayName: `${extraData.firstName || ''} ${extraData.lastName || ''}`.trim() || '',
      role: finalRole,
      isAdmin: finalRole === 'admin',
      sponsorId: finalSponsorId,
      referralCode: Math.random().toString(36).substring(2, 8).toUpperCase(),
      createdAt: new Date().toISOString(),
      lastLoginAt: new Date().toISOString(),
      lft: newLft,
      rgt: newRgt,
      firstName: extraData.firstName || '',
      lastName: extraData.lastName || '',
      address: extraData.address || '',
      bankAccountNumber: extraData.bankAccountNumber || '',
      bankAccountName: extraData.bankAccountName || '',
      bankName: extraData.bankName || '',
    };

    const createdDoc = await sanityClient.create(newUserDoc);
    
    // Set local session
    localStorage.setItem('userId', createdDoc._id);
    setUser({ uid: createdDoc._id, email: createdDoc.email });
    setProfile(createdDoc as UserProfile);
  };

  const signInWithEmail = async (email: string, password: string) => {
    const userDoc = await sanityClient.fetch(`*[_type == "user" && email == $email][0]`, { email });
    if (!userDoc) {
      throw new Error("Invalid email or password.");
    }
    
    const isValid = bcrypt.compareSync(password, userDoc.passwordHash || '');
    if (!isValid) {
      throw new Error("Invalid email or password.");
    }
    
    // Update last login
    await sanityClient.patch(userDoc._id).set({ lastLoginAt: new Date().toISOString() }).commit();

    localStorage.setItem('userId', userDoc._id);
    setUser({ uid: userDoc._id, email: userDoc.email });
    setProfile(userDoc as UserProfile);
  };

  const signOut = async () => {
    localStorage.removeItem('userId');
    setUser(null);
    setProfile(null);
  };

  return (
    <AuthContext.Provider value={{ user, profile, loading, signUpWithEmail, signInWithEmail, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};
"""

with open('src/contexts/AuthContext.tsx', 'w') as f:
    f.write(new_content)
