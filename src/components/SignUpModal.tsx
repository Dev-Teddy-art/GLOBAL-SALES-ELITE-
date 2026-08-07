import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

export const SignUpModal: React.FC<{ isOpen: boolean; onClose: () => void }> = ({ isOpen, onClose }) => {
  const { signUp } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [referralCode, setReferralCode] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    // Automatically capture ?ref=... from URL query string
    const params = new URLSearchParams(window.location.search);
    const ref = params.get('ref');
    if (ref) {
      setReferralCode(ref);
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await signUp({ email, password, referredBy: referralCode });
      onClose();
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <form onSubmit={handleSubmit}>
        <h2>Sign Up</h2>
        {error && <p className="error">{error}</p>}
        <input 
          type="email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          placeholder="Email" 
          required 
        />
        <input 
          type="password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          placeholder="Password" 
          required 
        />
        <input 
          type="text" 
          value={referralCode} 
          onChange={(e) => setReferralCode(e.target.value)} 
          placeholder="Referral Code (Optional)" 
        />
        <button type="submit">Complete Sign Up</button>
      </form>
    </div>
  );
};
