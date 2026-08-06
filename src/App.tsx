/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useSearchParams, useNavigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import { ThemeToggle } from './components/ThemeToggle';
import { motion, AnimatePresence } from 'motion/react';
import { sanityClient } from './lib/sanity';
import { Logo } from './components/Logo';
import { AvatarSelector } from './components/AvatarSelector';
import { Globe, Users, UserPlus, Network, LogOut, ChevronRight, ChevronDown, Copy, Check, Facebook, Twitter, Instagram, Crown, Shield, ShieldCheck, Eye, EyeOff, DollarSign, Activity, Waypoints, TrendingUp, Banknote } from 'lucide-react';
import { SettingsPage } from './components/SettingsPage';
import { Dashboard } from './components/Dashboard';
import { Footer } from './components/Footer';
import { AdminConsolePage } from './components/AdminConsolePage';



function FAQItem({ question, answer }: { question: string, answer: string }) {
  const [isOpen, setIsOpen] = React.useState(false);
  return (
    <div className="border-b border-gray-200 dark:border-white/10 pb-4">
      <button 
        onClick={() => setIsOpen(!isOpen)} 
        className="w-full flex justify-between items-center py-4 text-left font-bold text-gray-900 dark:text-white"
      >
        {question}
        <ChevronDown size={20} className={`transform transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ height: 0, opacity: 0 }} 
            animate={{ height: 'auto', opacity: 1 }} 
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden text-gray-600 dark:text-gray-400 text-sm leading-relaxed"
          >
            <p className="pb-4">{answer}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function EarningsCalculator() {
  const [directReferrals, setDirectReferrals] = React.useState(5);
  const [teamDepth, setTeamDepth] = React.useState(3);

  const calculateEarnings = () => {
    const baseValue = 50000; // 50,000 NGN
    const directBonus = directReferrals * (baseValue * 0.05);
    const indirectBonus = (Math.pow(2, teamDepth) - 2) * (baseValue * 0.02);
    return directBonus + indirectBonus;
  };

  return (
    <div className="flex flex-col gap-8 relative z-10">
      <div>
        <div className="flex justify-between mb-2">
          <label className="text-white font-bold text-sm">Direct Referrals</label>
          <span className="text-[#EF4444] font-black">{directReferrals}</span>
        </div>
        <input 
          type="range" 
          min="1" max="50" 
          value={directReferrals} 
          onChange={e => setDirectReferrals(parseInt(e.target.value))}
          className="w-full accent-[#EF4444] h-2 bg-gray-200 dark:bg-black/40 rounded-lg appearance-none cursor-pointer"
        />
      </div>
      
      <div>
        <div className="flex justify-between mb-2">
          <label className="text-white font-bold text-sm">Average Team Depth</label>
          <span className="text-[#EF4444] font-black">Level {teamDepth}</span>
        </div>
        <input 
          type="range" 
          min="1" max="10" 
          value={teamDepth} 
          onChange={e => setTeamDepth(parseInt(e.target.value))}
          className="w-full accent-[#EF4444] h-2 bg-gray-200 dark:bg-black/40 rounded-lg appearance-none cursor-pointer"
        />
      </div>

      <div className="bg-white dark:bg-black/30 border border-gray-200 dark:border-white/10 rounded-2xl p-6 mt-4 flex items-center justify-between">
        <div>
          <div className="text-xs text-gray-600 dark:text-gray-400 font-bold uppercase tracking-wider mb-1">Projected Weekly Income</div>
          <div className="text-3xl font-black text-gray-900 dark:text-white">₦{calculateEarnings().toLocaleString()}</div>
        </div>
        <div className="w-12 h-12 rounded-full bg-[#0F172A]/20 flex items-center justify-center">
          <Banknote className="text-[#0F172A] dark:text-white" size={24} />
        </div>
      </div>
    </div>
  );
}

function LandingPage() {
  const { user, loading, signInWithEmail } = useAuth();
  const navigate = useNavigate();
  const [isSigningIn, setIsSigningIn] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState('');
  const [networkSize, setNetworkSize] = React.useState<number | null>(null);
  
  React.useEffect(() => {
    sanityClient.fetch('count(*[_type == "user"])').then(count => {
      setNetworkSize(count);
    }).catch(console.error);
  }, []);

  const [showLoginModal, setShowLoginModal] = React.useState(false);
  const [loginEmail, setLoginEmail] = React.useState('');
  const [loginPassword, setLoginPassword] = React.useState('');
  const [showLoginPassword, setShowLoginPassword] = React.useState(false);

  const [modalMode, setModalMode] = React.useState<'login' | 'forgot'>('login');
  const [resetEmail, setResetEmail] = React.useState('');
  const [resetPassword, setResetPassword] = React.useState('');
  const [resetSuccess, setResetSuccess] = React.useState(false);

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!resetEmail || !resetPassword) return;
    setIsSigningIn(true);
    setErrorMsg('');
    setResetSuccess(false);
    try {
      const res = await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: resetEmail, newPassword: resetPassword })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to reset password');
      setResetSuccess(true);
      setModalMode('login');
      setLoginEmail(resetEmail);
      setLoginPassword('');
    } catch(err: any) {
      setErrorMsg(err.message || String(err));
    } finally {
      setIsSigningIn(false);
    }
  };


  if (loading) return <div className="min-h-screen bg-gray-50 dark:bg-[#0B0F19] flex items-center justify-center text-gray-900 dark:text-white">Loading...</div>;
  if (user) return <Navigate to="/dashboard" replace />;

  const handleLogin = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!loginEmail || !loginPassword) return;
    
    setIsSigningIn(true);
    setErrorMsg('');
    try {
      await signInWithEmail(loginEmail, loginPassword);
    } catch (err: any) {
      setErrorMsg(err.message || String(err));
      console.error("SANITY DB ERROR:", err);
    } finally {
      setIsSigningIn(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#0B0F19] flex flex-col font-sans selection:bg-[#EF4444] selection:text-gray-900 dark:text-white overflow-hidden relative">
      {/* Dynamic Background */}
      <div className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] bg-[#0F172A]/10 dark:bg-[#0F172A]/30 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40vw] h-[40vw] bg-[#EF4444]/10 dark:bg-[#EF4444]/20 rounded-full blur-[150px] pointer-events-none" />
      
      {/* Floating Header */}
      <header className="fixed top-4 left-0 right-0 z-50 w-full max-w-7xl mx-auto px-4">
        <motion.div 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="flex justify-between items-center bg-white dark:bg-white/5 backdrop-blur-lg border border-gray-200 dark:border-white/10 p-4 rounded-2xl shadow-xl"
        >
          <div className="flex items-center gap-6">
            <Logo />
          </div>
          <div className="flex items-center gap-4">
            <ThemeToggle />
            <button onClick={() => { setShowLoginModal(true); setModalMode('login'); setResetSuccess(false); }} className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:text-white font-semibold text-sm transition-colors">
              Login
            </button>
            <button onClick={() => navigate('/signup')} className="bg-[#EF4444] hover:bg-[#EF4444] text-white font-bold text-sm px-5 py-2.5 rounded-xl shadow-[0_0_15px_rgba(239,68,68,0.4)] transition-all transform hover:scale-105">
              Get Started
            </button>
          </div>
        </motion.div>
      </header>

      {/* Main Hero Section */}
      <section className="relative z-10 flex flex-col lg:flex-row items-center justify-between max-w-7xl mx-auto w-full px-6 pt-32 pb-20 min-h-screen">
        
        {/* Left Copy */}
        <motion.div 
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={{
            hidden: {},
            visible: { transition: { staggerChildren: 0.1 } }
          }}
          className="flex-1 flex flex-col items-start gap-6 pt-10"
        >
          <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }} className="inline-flex items-center gap-2 bg-[#EF4444]/10 border border-[#EF4444]/30 px-3 py-1.5 rounded-full">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#EF4444] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#EF4444]"></span>
            </span>
            <span className="text-[#EF4444] text-xs font-bold tracking-wider uppercase">Become An Elite Today</span>
          </motion.div>
          
          <motion.h1 
            variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
            className="text-5xl md:text-7xl font-black text-gray-900 dark:text-white leading-[1.1] tracking-tight"
          >
            Redefine<br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-white via-gray-200 to-gray-500">Uppscale</span><br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#EF4444] to-[#EF4444]">Mastery</span>
          </motion.h1>
          
          <motion.p 
            variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
            className="text-lg text-gray-600 dark:text-gray-400 max-w-lg leading-relaxed font-medium"
          >
            Join the Global Sales Elite platform. Earn multi-tier commissions, and track your global downline in real-time.
          </motion.p>
          
          <motion.div 
            variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
            className="flex items-center gap-4 mt-4"
          >
            <button onClick={() => navigate('/signup')} className="bg-[#EF4444] hover:bg-[#EF4444] text-white font-bold text-lg px-8 py-4 rounded-xl shadow-[0_0_20px_rgba(239,68,68,0.3)] transition-all transform hover:scale-105 flex items-center gap-2">
              Join the Network <ChevronRight size={20} />
            </button>
          </motion.div>
        </motion.div>

        {/* Right Live Preview Graphic */}
        <motion.div 
          initial={{ opacity: 0, x: 40, rotateY: 10 }}
          animate={{ opacity: 1, x: 0, rotateY: 0 }}
          transition={{ type: "spring", stiffness: 50, delay: 0.2 }}
          className="flex-1 w-full max-w-lg mt-16 lg:mt-0 relative"
          style={{ perspective: '1000px' }}
        >
          <div className="bg-white/90 dark:bg-[#0B1120] dark:bg-opacity-80 backdrop-blur-2xl border border-gray-200 dark:border-white/10 rounded-3xl p-6 shadow-2xl relative">
            <div className="flex items-center justify-between mb-8 border-b border-gray-200 dark:border-white/10 pb-4">
              <h3 className="text-gray-900 dark:text-white font-bold flex items-center gap-2">
                <Waypoints className="text-[#0F172A] dark:text-white" size={18}/> Live Refferal Tree
              </h3>
              <div className="flex gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-[#EF4444]" />
                <div className="w-2.5 h-2.5 rounded-full bg-[#EF4444]" />
                <div className="w-2.5 h-2.5 rounded-full bg-[#0F172A]" />
              </div>
            </div>
            
            {/* Mock Binary Tree Animation */}
            <div className="flex flex-col items-center gap-6 relative pt-4">
              <motion.div 
                animate={{ y: [0, -5, 0] }} 
                transition={{ repeat: Infinity, duration: 3, ease: "easeInOut" }}
                className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#0F172A] to-[#0F172A] border border-[#0F172A]/30 flex items-center justify-center text-white font-bold shadow-[0_0_15px_rgba(15,23,42,0.5)] z-10"
              >
                YOU
              </motion.div>
              
              {/* Lines */}
              <svg className="absolute top-16 left-0 w-full h-32 pointer-events-none" preserveAspectRatio="none">
                <path d="M 230 0 C 230 40, 100 40, 100 80" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="2" />
                <path d="M 230 0 C 230 40, 360 40, 360 80" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="2" />
              </svg>

              <div className="flex gap-20 w-full justify-center">
                <motion.div 
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 1 }}
                  className="w-12 h-12 rounded-full bg-white dark:bg-[#1E293B] border border-[#0F172A]/30 flex items-center justify-center text-[#0F172A] dark:text-white font-bold text-xs shadow-[0_0_10px_rgba(16,185,129,0.2)] z-10"
                >
                  L1
                </motion.div>
                <motion.div 
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 2.5 }}
                  className="w-12 h-12 rounded-full bg-white dark:bg-[#1E293B] border border-[#EF4444]/30 flex items-center justify-center text-[#EF4444] font-bold text-xs shadow-[0_0_10px_rgba(239,68,68,0.2)] z-10 relative"
                >
                  <motion.div 
                    initial={{ scale: 2, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ delay: 2.3 }}
                    className="absolute -top-3 -right-3 bg-[#EF4444] text-white text-[9px] font-bold px-1.5 py-0.5 rounded"
                  >
                    NEW
                  </motion.div>
                  R1
                </motion.div>
              </div>
              
              {/* Stats Ticker */}
              <div className="w-full bg-gray-200 dark:bg-black/40 rounded-xl p-4 mt-4 flex justify-between items-center border border-gray-100 dark:border-white/5">
                <div className="text-center">
                  <div className="text-[10px] text-gray-600 dark:text-gray-400 uppercase font-bold tracking-wider">Total Volume</div>
                  <div className="text-[#0F172A] dark:text-white font-mono font-bold">{networkSize !== null ? `₦${((networkSize) * 50000).toLocaleString()}` : "..."}</div>
                </div>
                <div className="h-6 w-px bg-white/10" />
                <div className="text-center">
                  <div className="text-[10px] text-gray-600 dark:text-gray-400 uppercase font-bold tracking-wider">Network Size</div>
                  <div className="text-[#0F172A] dark:text-white font-mono font-bold">{networkSize !== null ? networkSize : "..."}</div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Value Prop Grid */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-24">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-black text-gray-900 dark:text-white mb-4">Engineered for Growth</h2>
          <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto font-medium">Our system is designed to reward active builders while ensuring sustainable payouts through advanced matrix mechanics.</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="bg-white dark:bg-white/5 backdrop-blur-md border border-gray-200 dark:border-white/10 hover:border-[#EF4444]/50 transition-all rounded-3xl p-8 flex flex-col gap-4 group"
          >
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#EF4444] to-[#EF4444] flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
              <Waypoints size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mt-2">2-Leg Spillover Matrix</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">
              Every node has exactly two spots. Additional recruits automatically "spill over" to the next available spot in your downline, helping your team grow faster.
            </p>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="bg-white dark:bg-white/5 backdrop-blur-md border border-gray-200 dark:border-white/10 hover:border-[#0F172A]/50 transition-all rounded-3xl p-8 flex flex-col gap-4 group"
          >
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#0F172A] to-[#0F172A] flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
              <Banknote size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mt-2">Tiered Commissions</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">
              Earn 15% on direct referrals, and 3% on second level. A robust compensation plan built for massive scaling.
            </p>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="bg-white dark:bg-white/5 backdrop-blur-md border border-gray-200 dark:border-white/10 hover:border-[#0F172A]/50 transition-all rounded-3xl p-8 flex flex-col gap-4 group"
          >
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#0F172A] to-[#0F172A] flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
              <TrendingUp size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mt-2">Instant Payout Approvals</h3>
            <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">
              Direct integration with local banks allows for rapid commission clearance. Track pending approvals directly from your dashboard.
            </p>
          </motion.div>
        </div>
      </section>

      
      {/* Earnings Calculator Section */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-24 border-t border-gray-100 dark:border-white/5">
        <div className="flex flex-col lg:flex-row gap-16 items-center">
          <div className="flex-1 text-left">
            <h2 className="text-3xl md:text-5xl font-black text-gray-900 dark:text-white mb-6">Calculate Your Potential</h2>
            <p className="text-gray-600 dark:text-gray-400 font-medium text-lg leading-relaxed mb-8 max-w-xl">
              Use our interactive slider to project your estimated weekly earnings based on active network referrals and system spillover. 
            </p>
            <div className="flex items-center gap-4">
              <div className="flex -space-x-4">
                {[1,2,3,4].map(i => (
                  <div key={i} className={`w-12 h-12 rounded-full border-2 border-[#0B0F19] bg-gradient-to-br from-[#EF4444] to-[#EF4444] flex items-center justify-center font-bold text-gray-900 dark:text-white text-xs z-${10-i}`}>
                    +{i}k
                  </div>
                ))}
              </div>
              <span className="text-gray-600 dark:text-gray-400 text-sm font-bold uppercase tracking-widest">Active Earners</span>
            </div>
          </div>
          
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="flex-1 w-full bg-white dark:bg-white/5 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-3xl p-8 lg:p-12 shadow-2xl relative"
          >
            {/* Ambient Glow */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-[#EF4444]/10 rounded-full blur-[80px] pointer-events-none" />
            
            <EarningsCalculator />
          </motion.div>
        </div>
      </section>
      {/* Detailed Compensation Plan */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-24 border-t border-gray-100 dark:border-white/5 text-center">
        <h2 className="text-3xl md:text-5xl font-black text-gray-900 dark:text-white mb-6">Unrivaled Compensation Plan</h2>
        <p className="text-gray-600 dark:text-gray-400 font-medium text-lg leading-relaxed mb-12 max-w-2xl mx-auto">
          We built our payouts to maximize earning potential for both direct effort and team building.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="bg-[#EF4444]/10 dark:bg-[#EF4444]/5 border border-[#EF4444]/20 rounded-3xl p-8 flex flex-col items-center justify-center">
            <h3 className="text-4xl font-black text-[#EF4444] mb-2">15%</h3>
            <p className="text-gray-900 dark:text-white font-bold text-lg">Direct Referral</p>
            <p className="text-gray-600 dark:text-gray-400 text-sm mt-2 text-center">Earn 15% immediately for anyone who signs up directly using your link.</p>
          </div>
          <div className="bg-white dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-3xl p-8 flex flex-col items-center justify-center">
            <h3 className="text-4xl font-black text-gray-900 dark:text-white mb-2">3%</h3>
            <p className="text-gray-900 dark:text-white font-bold text-lg">Indirect Level 2</p>
            <p className="text-gray-600 dark:text-gray-400 text-sm mt-2 text-center">Earn 3% for the direct referrals made by your Level 1 network.</p>
          </div>
          <div className="bg-white dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-3xl p-8 flex flex-col items-center justify-center relative overflow-hidden">
            <div className="absolute top-4 right-4"><Crown size={16} className="text-yellow-500" /></div>
            <h3 className="text-4xl font-black text-gray-900 dark:text-white mb-2">Grow a power Team</h3>
            <p className="text-gray-900 dark:text-white font-bold text-lg text-center"><br/><span className="text-sm font-normal text-gray-500">(Everyone)</span></p>
            <p className="text-gray-600 dark:text-gray-400 text-sm mt-2 text-center">Stand a chance to grow, learn, and maximize your ptential as a profitable Realtor.. Cheers Global Elite! </p>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-24 border-t border-gray-100 dark:border-white/5">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-black text-gray-900 dark:text-white mb-4">Success Stories</h2>
          <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto font-medium">Hear from top earners who are already scaling their network in our global matrix.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 p-8 rounded-3xl">
            <div className="flex gap-1 text-yellow-400 mb-4">★★★★★</div>
            <p className="text-gray-600 dark:text-gray-400 italic mb-6 leading-relaxed">
              "The 15% direct commission and immediate withdrawals changed the game for my agency. The visual network tree makes it so easy to see where spillover is happening."
            </p>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gray-200 rounded-full bg-[url('https://i.pravatar.cc/150?img=33')] bg-cover" />
              <div>
                <p className="font-bold text-gray-900 dark:text-white">Sarah O.</p>
                <p className="text-xs text-gray-600 dark:text-gray-400">Executive Director</p>
              </div>
            </div>
          </div>
          <div className="bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 p-8 rounded-3xl">
            <div className="flex gap-1 text-yellow-400 mb-4">★★★★★</div>
            <p className="text-gray-600 dark:text-gray-400 italic mb-6 leading-relaxed">
              "I've built teams in three different systems before, but GSE's dual-leg matrix ensures my team actually benefits from my over-recruiting. Highly recommended."
            </p>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gray-200 rounded-full bg-[url('https://i.pravatar.cc/150?img=11')] bg-cover" />
              <div>
                <p className="font-bold text-gray-900 dark:text-white">David K.</p>
                <p className="text-xs text-gray-600 dark:text-gray-400">Diamond Rank Earner</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="relative z-10 max-w-3xl mx-auto px-6 py-24 border-t border-gray-100 dark:border-white/5">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-black text-gray-900 dark:text-white mb-4">Frequently Asked Questions</h2>
        </div>
        <div className="space-y-2">
          <FAQItem 
            question="How do I get paid?" 
            answer="Commissions are instantly credited to your GSE dashboard. You can request a withdrawal to your registered local bank account at any time. Our admin team processes payouts usually within 24 hours."
          />
          <FAQItem 
            question="What happens if I recruit more than 2 people?" 
            answer="Because GSE uses a 2-leg binary matrix, your 3rd recruit will automatically 'spill over' into the downline of your first two recruits. This helps your team grow and motivates everyone!"
          />
          <FAQItem 
            question="Is there a limit to how deep I can earn?" 
            answer="Direct (15%) and Level 2 (3%) are uncapped in volume. Deep network bonuses (4%) are strictly reserved for the Admin owner, ensuring the platform scales sustainably."
          />
        </div>
      </section>

{/* Footer */}
      

      {/* Login Modal */}
      <AnimatePresence>
        {showLoginModal && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center px-4">
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-black/60 backdrop-blur-sm"
              onClick={() => setShowLoginModal(false)}
            />
            <motion.div 
              initial={{ scale: 0.95, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.95, opacity: 0, y: 20 }}
              className="bg-white dark:bg-[#1E293B]/90 backdrop-blur-xl border border-gray-200 dark:border-white/10 p-8 rounded-3xl shadow-2xl w-full max-w-md relative z-10"
            >
              <button 
                onClick={() => setShowLoginModal(false)}
                className="absolute top-4 right-4 w-8 h-8 flex items-center justify-center rounded-full bg-white dark:bg-white/5 hover:bg-white/10 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:text-white transition-colors"
              >
                ✕
              </button>
              
              <div className="text-center mb-8">
                <div className="mx-auto bg-[#EF4444] p-3 rounded-2xl w-max mb-4 shadow-lg">
                  <ShieldCheck size={24} className="text-white" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  {modalMode === 'login' ? 'Welcome Back' : 'Reset Password'}
                </h2>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  {modalMode === 'login' ? 'Sign in to access your network dashboard' : 'Enter your email and new password to reset'}
                </p>
              </div>

              {errorMsg && (
                <div className="bg-[#EF4444]/20 text-[#EF4444] border border-[#EF4444]/30 px-4 py-3 rounded-xl text-sm mb-6">
                  {errorMsg}
                </div>
              )}
              {resetSuccess && (
                <div className="bg-green-500/20 text-green-600 dark:text-green-400 border border-green-500/30 px-4 py-3 rounded-xl text-sm mb-6">
                  Password reset successfully. Please log in.
                </div>
              )}
              
              {modalMode === 'login' ? (
                <form onSubmit={handleLogin} className="flex flex-col gap-4">
                  <input 
                    type="email" 
                    placeholder="Email Address" 
                    value={loginEmail}
                    onChange={(e) => setLoginEmail(e.target.value)}
                    className="w-full bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:border-[#EF4444] focus:ring-1 focus:ring-[#EF4444] transition-all"
                    required
                  />
                  <div className="relative">
                    <input 
                      type={showLoginPassword ? "text" : "password"} 
                      placeholder="Password" 
                      value={loginPassword}
                      onChange={(e) => setLoginPassword(e.target.value)}
                      className="w-full bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:border-[#EF4444] focus:ring-1 focus:ring-[#EF4444] transition-all pr-12"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowLoginPassword(!showLoginPassword)}
                      className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 transition-colors"
                    >
                      {showLoginPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                  
                  <div className="text-right">
                    <button 
                      type="button" 
                      onClick={() => { setModalMode('forgot'); setErrorMsg(''); setResetSuccess(false); }}
                      className="text-sm text-gray-600 dark:text-gray-400 hover:text-[#EF4444] transition-colors"
                    >
                      Forgot Password?
                    </button>
                  </div>

                  <button 
                    type="submit"
                    disabled={isSigningIn}
                    className="w-full bg-[#EF4444] hover:bg-[#EF4444] text-white font-bold py-3.5 rounded-xl shadow-[0_0_15px_rgba(239,68,68,0.3)] transition-all mt-2 disabled:opacity-50"
                  >
                    {isSigningIn ? 'Authenticating...' : 'Sign In'}
                  </button>
                </form>
              ) : (
                <form onSubmit={handleResetPassword} className="flex flex-col gap-4">
                  <input 
                    type="email" 
                    placeholder="Email Address" 
                    value={resetEmail}
                    onChange={(e) => setResetEmail(e.target.value)}
                    className="w-full bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:border-[#EF4444] focus:ring-1 focus:ring-[#EF4444] transition-all"
                    required
                  />
                  <div className="relative">
                    <input 
                      type={showLoginPassword ? "text" : "password"} 
                      placeholder="New Password" 
                      value={resetPassword}
                      onChange={(e) => setResetPassword(e.target.value)}
                      className="w-full bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:border-[#EF4444] focus:ring-1 focus:ring-[#EF4444] transition-all pr-12"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowLoginPassword(!showLoginPassword)}
                      className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 transition-colors"
                    >
                      {showLoginPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </div>
                  
                  <button 
                    type="submit"
                    disabled={isSigningIn}
                    className="w-full bg-[#EF4444] hover:bg-[#EF4444] text-white font-bold py-3.5 rounded-xl shadow-[0_0_15px_rgba(239,68,68,0.3)] transition-all mt-4 disabled:opacity-50"
                  >
                    {isSigningIn ? 'Resetting...' : 'Reset Password'}
                  </button>
                  <button 
                    type="button"
                    onClick={() => { setModalMode('login'); setErrorMsg(''); }}
                    className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors mt-2"
                  >
                    Back to Login
                  </button>
                </form>
              )}
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
function SignUpPage() {
  const { user, loading, signUpWithEmail, signOut } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [searchParams] = useSearchParams();
  const rawRef = searchParams.get('ref') || '';
  const refCode = rawRef.includes('-') ? rawRef.split('-').pop() : rawRef;
  
  // If a logged-in user visits signup directly (with or without ref),
  // we log them out automatically so they can register a new account.
  React.useEffect(() => {
    const checkInitialAuth = async () => {
      const storedUserId = localStorage.getItem('userId');
      if (storedUserId) {
         await signOut();
      }
    };
    checkInitialAuth();
  }, []);

  const [isSigningIn, setIsSigningIn] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState('');
  const [networkSize, setNetworkSize] = React.useState<number | null>(null);
  
  React.useEffect(() => {
    sanityClient.fetch('count(*[_type == "user"])').then(count => {
      setNetworkSize(count);
    }).catch(console.error);
  }, []);
  
  const oauthEmail = location.state?.email || '';
  const oauthDisplayName = location.state?.displayName || '';
  const defaultFirstName = oauthDisplayName ? oauthDisplayName.split(' ')[0] : '';
  const defaultLastName = oauthDisplayName ? oauthDisplayName.split(' ').slice(1).join(' ') : '';
  
  const [showSignUpPassword, setShowSignUpPassword] = React.useState(false);
  const [formData, setFormData] = React.useState({
    sponsorId: refCode,
    firstName: defaultFirstName,
    lastName: defaultLastName,
    email: oauthEmail,
    password: '',
    address: '',
    bankAccountNumber: '',
    bankAccountName: '',
    bankName: '',
    avatarUrl: 'https://api.dicebear.com/9.x/avataaars-neutral/svg?seed=Felix&backgroundColor=e2e8f0'
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  if (loading) return <div className="min-h-screen bg-gray-50 dark:bg-[#0F172A] flex items-center justify-center text-gray-900 dark:text-white">Loading...</div>;
  if (user) return <div className="min-h-screen bg-gray-50 dark:bg-[#0F172A] flex items-center justify-center text-gray-900 dark:text-white">Signing out current session...</div>;

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.firstName || !formData.lastName || !formData.email || !formData.password || !formData.address || !formData.bankAccountNumber || !formData.bankAccountName || !formData.bankName) {
      setErrorMsg('Please fill out all required fields.');
      return;
    }

    setIsSigningIn(true);
    setErrorMsg('');
    try {
      await signUpWithEmail(formData.password, formData);
      navigate('/dashboard', { replace: true });
    } catch (err: any) {
      setErrorMsg(err.message || String(err));
      console.error("SANITY DB ERROR:", err);
    } finally {
      setIsSigningIn(false);
    }
  };



  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#0F172A] flex flex-col items-center p-6 pt-24 pb-12 relative font-sans overflow-y-auto">
       <button onClick={() => navigate('/')} className="absolute top-8 left-8 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:text-white flex items-center gap-2 transition-colors z-40">
         <ChevronRight className="rotate-180" size={20} /> Back to Home
       </button>
       
       <div className="bg-white dark:bg-white/10 backdrop-blur-md p-8 md:p-10 rounded-3xl border border-gray-200 dark:border-white/20 w-full max-w-2xl shadow-2xl flex flex-col gap-6 relative z-30">
          <div className="text-center mb-2">
            <div className="mx-auto bg-[#EF4444] p-3 rounded-2xl w-max mb-4 shadow-lg">
              <UserPlus size={24} className="text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Create an Account</h2>
            <p className="text-gray-600 dark:text-gray-400 mt-2 text-sm">Join the Global Sales Elite network.</p>
          </div>

          {errorMsg && (
            <div className="bg-[#EF4444]/20 text-[#EF4444] border border-[#EF4444]/30 px-4 py-3 rounded-xl text-sm text-left">
              {errorMsg}
            </div>
          )}

          <form onSubmit={handleSignUp} className="flex flex-col gap-5">
            <div className="flex flex-col gap-2 text-left">
              <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">Sponsor Referral Code (Optional)</label>
              <input 
                type="text" 
                name="sponsorId"
                value={formData.sponsorId}
                onChange={handleChange}
                readOnly={!!refCode}
                placeholder="Enter sponsor's referral code"
                className={`w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/20 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-[#EF4444] transition-all ${!!refCode ? 'opacity-70 cursor-not-allowed bg-white/10' : ''}`}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div className="flex flex-col gap-2 text-left">
                <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">First Name *</label>
                <input required type="text" name="firstName" value={formData.firstName} onChange={handleChange} className="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/20 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444]" />
              </div>
              <div className="flex flex-col gap-2 text-left">
                <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">Last Name *</label>
                <input required type="text" name="lastName" value={formData.lastName} onChange={handleChange} className="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/20 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444]" />
              </div>
            </div>

            <div className="flex flex-col gap-2 text-left">
              <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">Email Address *</label>
              <input 
                required 
                type="email" 
                name="email" 
                value={formData.email} 
                onChange={handleChange} 
                className="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/20 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444] transition-all"
              />
            </div>

            <div className="flex flex-col gap-2 text-left">
              <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">House Address *</label>
              <input required type="text" name="address" value={formData.address} onChange={handleChange} className="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/20 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444]" />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div className="flex flex-col gap-2 text-left">
                <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">Bank Name *</label>
                <input required type="text" name="bankName" value={formData.bankName} onChange={handleChange} className="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/20 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444]" />
              </div>
              <div className="flex flex-col gap-2 text-left">
                <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">Bank Account Number *</label>
                <input required type="text" name="bankAccountNumber" value={formData.bankAccountNumber} onChange={handleChange} className="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/20 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444]" />
              </div>
            </div>

            <div className="flex flex-col gap-2 text-left">
              <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">Bank Account Name *</label>
              <input required type="text" name="bankAccountName" value={formData.bankAccountName} onChange={handleChange} className="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/20 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444]" />
            </div>
            <div className="flex flex-col gap-2 text-left mb-2">
              <AvatarSelector value={formData.avatarUrl} onChange={(val) => setFormData(prev => ({...prev, avatarUrl: val}))} />
            </div>

            <div className="flex flex-col gap-2 text-left">
              <label className="text-gray-600 dark:text-gray-400 text-sm font-medium pl-1">Password *</label>
              <div className="relative">
                <input required type={showSignUpPassword ? "text" : "password"} name="password" value={formData.password} onChange={handleChange} className="w-full bg-gray-50 dark:bg-white/5 border border-gray-200 dark:border-white/20 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#EF4444] pr-12" />
                <button
                  type="button"
                  onClick={() => setShowSignUpPassword(!showSignUpPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-600 dark:text-gray-400 hover:text-gray-600 dark:text-gray-400 transition-colors"
                >
                  {showSignUpPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            <button 
              type="submit"
              disabled={isSigningIn}
              className="w-full bg-[#EF4444] hover:bg-[#EF4444] text-white font-black text-lg px-8 py-4 rounded-xl shadow-xl transition-all disabled:opacity-50 uppercase tracking-wider mt-4"
            >
              {isSigningIn ? 'Submitting...' : 'Sign Up / Submit'}
            </button>
          </form>


        </div>
    </div>
  );
}

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="min-h-screen flex items-center justify-center bg-gray-50 text-[#0F172A] dark:text-white font-bold text-xl">Loading...</div>;
  if (!user) return <Navigate to="/" replace />;
  return <>{children}</>;
}

function AdminRoute({ children }: { children: React.ReactNode }) {
  const { user, profile, loading } = useAuth();
  if (loading) return <div className="min-h-screen flex items-center justify-center bg-gray-50 text-[#0F172A] dark:text-white font-bold text-xl">Loading...</div>;
  if (!user) return <Navigate to="/" replace />;
  if (!profile || (profile.role !== 'admin' && !profile.isAdmin)) return <Navigate to="/dashboard" replace />;
  return <>{children}</>;
}

export default function App() {
  return (
    <ThemeProvider>
    <AuthProvider>
      <BrowserRouter>
        <div className="flex flex-col min-h-screen">
          <div className="flex-1">
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/signup" element={<SignUpPage />} />
              <Route path="/dashboard" element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              } />
              <Route path="/settings" element={
                <PrivateRoute>
                  <SettingsPage />
                </PrivateRoute>
              } />
              <Route path="/admin" element={
                <AdminRoute>
                  <AdminConsolePage />
                </AdminRoute>
              } />
            </Routes>
          </div>
          <Footer />
        </div>
      </BrowserRouter>
    </AuthProvider>
    </ThemeProvider>
  );
}