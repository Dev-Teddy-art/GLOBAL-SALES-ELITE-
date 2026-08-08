import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Navbar } from './Navbar';
import { AvatarSelector } from './AvatarSelector';
import { Eye, EyeOff, Save, Check } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

export function SettingsPage() {
  const { profile, updateProfile } = useAuth();
  
  const [formData, setFormData] = useState({
    avatarUrl: profile?.avatarUrl || profile?.profileImage || '',
    bankName: profile?.bankName || '',
    bankAccountNumber: profile?.bankAccountNumber || '',
    bankAccountName: profile?.bankAccountName || '',
    newPassword: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setSaveMessage('');
    
    if (formData.newPassword && formData.newPassword !== formData.confirmPassword) {
      setErrorMsg("Passwords do not match");
      return;
    }

    setIsSaving(true);
    try {
      const res = await fetch('/api/auth/update-settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          userId: profile?._id || profile?.id,
          avatarUrl: formData.avatarUrl,
          bankName: formData.bankName,
          bankAccountNumber: formData.bankAccountNumber,
          bankAccountName: formData.bankAccountName,
          ...(formData.newPassword ? { newPassword: formData.newPassword } : {})
        })
      });

      if (res.ok) {
        const data = await res.json();
        setSaveMessage("Settings saved successfully!");
        setFormData(prev => ({ ...prev, newPassword: '', confirmPassword: '' }));
        if (data.user) {
          updateProfile({
            avatarUrl: formData.avatarUrl,
            bankName: formData.bankName,
            bankAccountNumber: formData.bankAccountNumber,
            bankAccountName: formData.bankAccountName
          });
        }
      } else {
        const data = await res.json();
        setErrorMsg(data.error || "Failed to update settings");
      }
    } catch (err: any) {
      setErrorMsg(err.message || "Network error");
    } finally {
      setIsSaving(false);
      setTimeout(() => setSaveMessage(''), 3000);
    }
  };

  return (
    <div className="w-full bg-gray-50 dark:bg-[#020617] min-h-screen text-gray-900 dark:text-gray-200 font-sans relative pb-12 transition-colors duration-300">
      <Navbar />
      
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 pb-12">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="bg-white dark:bg-[#1E293B] rounded-3xl shadow-xl border border-gray-200 dark:border-white/10 p-8">
          <h2 className="text-2xl font-black text-gray-900 dark:text-white mb-6">Profile Settings</h2>
          
          {errorMsg && (
            <div className="bg-[#EF4444]/20 text-[#EF4444] border border-[#EF4444]/30 px-4 py-3 rounded-xl text-sm mb-6">
              {errorMsg}
            </div>
          )}

          {saveMessage && (
            <div className="bg-[#10B981]/20 text-[#10B981] border border-[#10B981]/30 px-4 py-3 rounded-xl text-sm mb-6 flex items-center gap-2">
              <Check size={16} />
              {saveMessage}
            </div>
          )}

          <form onSubmit={handleSave} className="space-y-8">
            {/* Avatar Section */}
            <div className="space-y-4">
              <h3 className="text-lg font-bold text-gray-800 dark:text-gray-200 border-b border-gray-100 dark:border-white/10 pb-2">Profile Avatar</h3>
              <AvatarSelector value={formData.avatarUrl} onChange={(val) => setFormData(prev => ({...prev, avatarUrl: val}))} />
            </div>

            {/* Banking Information */}
            <div className="space-y-4">
              <h3 className="text-lg font-bold text-gray-800 dark:text-gray-200 border-b border-gray-100 dark:border-white/10 pb-2">Banking Details</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div className="flex flex-col gap-2">
                  <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">Bank Name</label>
                  <input type="text" name="bankName" value={formData.bankName} onChange={handleChange} className="w-full bg-gray-50 dark:bg-[#0F172A] border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444]" />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">Bank Account Number</label>
                  <input type="text" name="bankAccountNumber" value={formData.bankAccountNumber} onChange={handleChange} className="w-full bg-gray-50 dark:bg-[#0F172A] border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444]" />
                </div>
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">Bank Account Name</label>
                <input type="text" name="bankAccountName" value={formData.bankAccountName} onChange={handleChange} className="w-full bg-gray-50 dark:bg-[#0F172A] border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444]" />
              </div>
            </div>

            {/* Password Management */}
            <div className="space-y-4">
              <h3 className="text-lg font-bold text-gray-800 dark:text-gray-200 border-b border-gray-100 dark:border-white/10 pb-2">Security</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div className="flex flex-col gap-2">
                  <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">New Password</label>
                  <div className="relative">
                    <input type={showPassword ? "text" : "password"} name="newPassword" value={formData.newPassword} onChange={handleChange} placeholder="Leave blank to keep current" className="w-full bg-gray-50 dark:bg-[#0F172A] border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444] pr-12" />
                    <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
                      {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                  </div>
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">Confirm New Password</label>
                  <div className="relative">
                    <input type={showConfirmPassword ? "text" : "password"} name="confirmPassword" value={formData.confirmPassword} onChange={handleChange} placeholder="Confirm new password" className="w-full bg-gray-50 dark:bg-[#0F172A] border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444] pr-12" />
                    <button type="button" onClick={() => setShowConfirmPassword(!showConfirmPassword)} className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
                      {showConfirmPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-4">
              <button 
                type="submit"
                disabled={isSaving}
                className="w-full bg-[#0F172A] dark:bg-white text-white dark:text-[#0F172A] hover:bg-gray-800 dark:hover:bg-gray-100 font-bold text-lg px-8 py-4 rounded-xl shadow-lg transition-all disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {isSaving ? 'Saving...' : <><Save size={20} /> Save Changes</>}
              </button>
            </div>
          </form>
        </motion.div>
      </main>
    </div>
  );
}



