import React, { useState } from 'react';
import { Logo } from './Logo';
import { Bell, LogOut, LayoutDashboard, Crown } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { ThemeToggle } from './ThemeToggle';

export function Navbar() {
  const { profile, signOut } = useAuth();
  const navigate = useNavigate();
  const [showNotifications, setShowNotifications] = useState(false);

  const notifications = profile?.notifications || [];
  const unreadCount = notifications.filter((n: any) => !n.read).length;

  const handleOpenNotifications = async () => {
    setShowNotifications(!showNotifications);
    if (!showNotifications && unreadCount > 0 && profile) {
      try {
        await fetch('/api/notifications/read', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userId: profile._id || profile.id })
        });
      } catch (err) {
        console.error("Error marking notifications as read", err);
      }
    }
  };

  const [showProfileMenu, setShowProfileMenu] = useState(false);

  const handleSignOut = async () => {
    await signOut();
    navigate('/');
  };

  return (
    <header className="bg-white dark:bg-[#0F172A] border-b border-gray-200 dark:border-white/10 shadow-sm relative z-50 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        <div className="flex items-center gap-4 cursor-pointer" onClick={() => navigate('/dashboard')}>
          <Logo className="h-10 w-auto bg-gray-100 dark:bg-white/10 rounded px-2" />
          <h1 className="text-xl font-bold tracking-wider hidden sm:block text-gray-900 dark:text-white">PORTAL</h1>
        </div>
        
        <div className="flex items-center gap-4 relative">
          {(profile?.role === 'admin' || profile?.isAdmin) && (
            <button 
              onClick={() => navigate('/admin')}
              className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/10 p-2 rounded-xl transition-colors flex items-center gap-2 text-sm font-bold"
            >
              <Crown size={18} className="text-[#EF4444]" />
              <span className="hidden md:inline">Admin</span>
            </button>
          )}

          <ThemeToggle className="text-gray-600 dark:text-gray-300 mr-2" />
          
          <button onClick={handleOpenNotifications} className="relative p-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/10 rounded-xl transition-colors">
            <Bell size={20} />
            {unreadCount > 0 && (
              <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-[#EF4444] rounded-full border-2 border-white dark:border-[#0F172A]" />
            )}
          </button>
          
          {showNotifications && (
            <div className="absolute right-0 top-full mt-2 w-80 bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden z-50">
              <div className="px-4 py-3 border-b border-gray-100 flex justify-between items-center bg-gray-50">
                <h3 className="font-bold text-gray-900 text-sm">Notifications</h3>
              </div>
              <div className="max-h-80 overflow-y-auto">
                {notifications.length === 0 ? (
                  <div className="p-6 text-center text-sm text-gray-600 dark:text-gray-400">No new notifications.</div>
                ) : (
                  notifications.map((n: any, idx: number) => (
                    <div key={idx} className="p-4 border-b border-gray-50 hover:bg-gray-50 transition-colors">
                      <p className="text-sm text-gray-800">{n.message}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{new Date(n.createdAt).toLocaleDateString()}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          <div className="relative">
            <button 
              onClick={() => setShowProfileMenu(!showProfileMenu)}
              className="w-10 h-10 rounded-full bg-gray-100 dark:bg-white/10 border-2 border-gray-200 dark:border-white/20 flex items-center justify-center font-bold text-gray-900 dark:text-white overflow-hidden focus:outline-none focus:ring-2 focus:ring-[#EF4444] transition-all"
            >
               {profile?.profileImage || profile?.avatarUrl ? (
                 <img src={profile.profileImage || profile.avatarUrl} alt="Profile" className="w-full h-full object-cover" />
               ) : (
                 profile?.displayName?.charAt(0).toUpperCase() || 'U'
               )}
            </button>
            {showProfileMenu && (
              <div className="absolute right-0 top-full mt-2 w-48 bg-white dark:bg-[#1E293B] rounded-2xl shadow-xl border border-gray-200 dark:border-white/10 overflow-hidden z-50">
                <button 
                  onClick={() => { setShowProfileMenu(false); navigate('/settings'); }}
                  className="w-full text-left px-4 py-3 text-sm font-bold text-gray-900 dark:text-white hover:bg-gray-50 dark:hover:bg-white/5 transition-colors"
                >
                  Settings
                </button>
                <button 
                  onClick={() => { setShowProfileMenu(false); handleSignOut(); }}
                  className="w-full text-left px-4 py-3 text-sm font-bold text-[#EF4444] hover:bg-gray-50 dark:hover:bg-white/5 transition-colors border-t border-gray-100 dark:border-white/5"
                >
                  Sign Out
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
