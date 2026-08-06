import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, UserProfile } from '../contexts/AuthContext';
import { sanityClient } from '../lib/sanity';
import { LogOut, Copy, Users, Network, Link as LinkIcon, Share2, Crown, Shield, Calculator, BarChart as BarChartIcon, Bell, DollarSign, Wallet, Target, Award, TrendingUp, Waypoints, Banknote, Check, History } from 'lucide-react';
import { Logo } from './Logo';
import { Navbar } from './Navbar';
import { ProfilePhotoUpload } from './ProfilePhotoUpload';
import { ReferralTree } from './ReferralTree';
import { motion, AnimatePresence } from 'motion/react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';




const confettiParticles = Array.from({ length: 50 }).map((_, i) => ({
  id: i,
  color: ['bg-[#10B981]', 'bg-[#EF4444]', 'bg-blue-500', 'bg-yellow-400', 'bg-purple-500'][Math.floor(Math.random() * 5)],
  angle: Math.random() * Math.PI * 2,
  velocity: 15 + Math.random() * 30,
  size: 6 + Math.random() * 8
}));

function SuccessAnimation({ show, message }: { show: boolean, message?: string }) {
  return (
    <AnimatePresence>
      {show && (
        <div className="fixed inset-0 pointer-events-none z-[200] flex items-center justify-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.5, y: 50 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: -20 }}
            className="absolute bg-white dark:bg-[#1E293B] px-8 py-5 rounded-2xl shadow-2xl flex items-center gap-4 border border-[#10B981]/20 z-10"
          >
            <div className="bg-[#10B981] p-2 rounded-full text-white shadow-md">
              <Check size={24} />
            </div>
            <span className="font-bold text-lg text-gray-900 dark:text-white">{message || "Success!"}</span>
          </motion.div>
          {confettiParticles.map((p) => (
            <motion.div
              key={p.id}
              initial={{ opacity: 1, x: 0, y: 0, scale: 0 }}
              animate={{
                opacity: 0,
                x: Math.cos(p.angle) * p.velocity * 15,
                y: Math.sin(p.angle) * p.velocity * 15 + 150,
                scale: 1,
                rotate: Math.random() * 360
              }}
              transition={{ duration: 2, ease: "easeOut" }}
              className={`absolute rounded-sm shadow-sm ${p.color}`}
              style={{ width: p.size, height: p.size }}
            />
          ))}
        </div>
      )}
    </AnimatePresence>
  );
}

function SalesLogger() {
  const { profile } = useAuth();
  const [amount, setAmount] = useState<number | ''>('');
  const [propertyName, setPropertyName] = useState('');
  const [dateSold, setDateSold] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!amount || amount <= 0 || !propertyName || !dateSold || !profile) return;
    
    setSubmitting(true);
    try {
      const res = await fetch('/api/sales', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: profile._id || profile.id, amount, propertyName, dateSold })
      });
      if (res.ok) {
        setShowSuccess(true);
        setTimeout(() => setShowSuccess(false), 2500);
        setAmount('');
        setPropertyName('');
        setDateSold('');
      } else {
        alert("Failed to log sale.");
      }
    } catch (err) {
      console.error(err);
      alert("Error logging sale.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.4 }} className="bg-white dark:bg-[#0F172A] rounded-3xl shadow-lg border border-gray-200 dark:border-white/10 p-6 md:p-8 relative overflow-hidden">
      <SuccessAnimation show={showSuccess} message="Commission Requested!" />
      <div className="flex items-center gap-4 mb-6 relative z-10">
        <div className="bg-gradient-to-br from-[#10B981] to-[#047857] p-3 rounded-2xl shadow-md text-white">
          <Banknote size={24} />
        </div>
        <div>
          <h3 className="text-xl font-black text-gray-900 dark:text-white tracking-tight">
            Log a Sale
          </h3>
          <p className="text-gray-600 dark:text-gray-400 text-sm font-medium">Record sales to automatically request commissions</p>
        </div>
      </div>
      
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex-1 w-full">
            <label className="block text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest mb-2">Property Name</label>
            <input 
              type="text" 
              value={propertyName}
              onChange={(e) => setPropertyName(e.target.value)}
              placeholder="e.g. Seaside Villa"
              className="w-full bg-gray-50 dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 text-gray-900 dark:text-white rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#10B981] focus:border-transparent outline-none transition-all font-bold"
              required
            />
          </div>
          <div className="flex-1 w-full">
            <label className="block text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest mb-2">Amount Sold (₦)</label>
            <input 
              type="number" 
              min="0"
              value={amount}
              onChange={(e) => setAmount(Number(e.target.value) || '')}
              placeholder="e.g. 5000000"
              className="w-full bg-gray-50 dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 text-gray-900 dark:text-white rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#10B981] focus:border-transparent outline-none transition-all font-mono font-bold"
              required
            />
          </div>
          <div className="flex-1 w-full">
            <label className="block text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest mb-2">Date Sold</label>
            <input 
              type="date" 
              value={dateSold}
              onChange={(e) => setDateSold(e.target.value)}
              className="w-full bg-gray-50 dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 text-gray-900 dark:text-white rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#10B981] focus:border-transparent outline-none transition-all font-bold"
              required
            />
          </div>
        </div>
        <div className="flex justify-end mt-2">
          <button 
            type="submit" 
            disabled={submitting || !amount || !propertyName || !dateSold}
            className="bg-[#10B981] hover:bg-[#059669] disabled:opacity-50 text-white px-8 py-3 rounded-xl font-bold shadow-lg transition-all w-full sm:w-auto"
          >
            {submitting ? 'Submitting...' : 'Log Sale'}
          </button>
        </div>
      </form>
    </motion.div>
  );
}

function CommissionCalculator({ role, defaultL1 = 0, defaultL2 = 0, defaultL3 = 0 }: { role: 'admin' | 'user', defaultL1?: number, defaultL2?: number, defaultL3?: number }) {
  const [l1Count, setL1Count] = useState<number>(defaultL1);
  const [l2Count, setL2Count] = useState<number>(defaultL2);
  const [l3Count, setL3Count] = useState<number>(defaultL3);
  const [avgSaleValue, setAvgSaleValue] = useState<number>(1000);

  useEffect(() => {
    setL1Count(defaultL1);
    setL2Count(defaultL2);
    setL3Count(defaultL3);
  }, [defaultL1, defaultL2, defaultL3]);

  // Commission rates
  const l1Rate = 0.15; // 15%
  const l2Rate = 0.03; // 3%
  const l3Rate = 0.04; // 4%

  const totalEarnings = (l1Count * avgSaleValue * l1Rate) + (l2Count * avgSaleValue * l2Rate) + (role === 'admin' ? l3Count * avgSaleValue * l3Rate : 0);

  const currencyFormatter = new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN' });



  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }} className="bg-white dark:bg-[#0F172A] rounded-3xl shadow-lg border border-gray-200 dark:border-white/10 p-8 md:p-10 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-[#0F172A]/5 dark:from-transparent to-transparent opacity-50 pointer-events-none" />
      <div className="flex items-center gap-4 mb-8 relative z-10">
        <div className="bg-gradient-to-br from-[#0F172A] to-[#0F172A] p-3.5 rounded-2xl shadow-md text-white">
          <Calculator size={28} />
        </div>
        <div>
          <h3 className="text-2xl font-black text-gray-900 dark:text-white tracking-tight">
            Potential Earnings
          </h3>
          <p className="text-gray-600 dark:text-gray-400 text-sm font-medium">Model your network commissions</p>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 relative z-10">
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">Average Sale Value (₦)</label>
            <div className="relative">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 dark:text-gray-400 font-bold">₦</span>
              <input 
                type="number" 
                min="0"
                value={avgSaleValue || ''}
                onChange={(e) => setAvgSaleValue(Math.max(0, parseInt(e.target.value) || 0))}
                placeholder="1000"
                className="w-full bg-gray-50 dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 text-gray-900 dark:text-white rounded-xl pl-10 pr-4 py-3.5 focus:ring-2 focus:ring-[#0F172A] dark:focus:ring-white/20 focus:border-transparent outline-none transition-all font-mono font-bold"
              />
            </div>
          </div>
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-bold text-gray-700">Level 1 Members</label>
              <span className="text-[10px] uppercase tracking-widest font-black text-[#0F172A] dark:text-white bg-[#0F172A]/10 px-2.5 py-1 rounded-full">15% Comm.</span>
            </div>
            <input 
              type="number" 
              min="0"
              value={l1Count || ''}
              onChange={(e) => setL1Count(Math.max(0, parseInt(e.target.value) || 0))}
              placeholder="0"
              className="w-full bg-gray-50 dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 text-gray-900 dark:text-white rounded-xl px-4 py-3.5 focus:ring-2 focus:ring-[#0F172A] dark:focus:ring-white/20 focus:border-transparent outline-none transition-all font-mono font-bold"
            />
          </div>
          
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-bold text-gray-700">Level 2 Members</label>
              <span className="text-[10px] uppercase tracking-widest font-black text-[#0F172A] dark:text-white bg-[#0F172A]/10 px-2.5 py-1 rounded-full">3% Comm.</span>
            </div>
            <input 
              type="number" 
              min="0"
              value={l2Count || ''}
              onChange={(e) => setL2Count(Math.max(0, parseInt(e.target.value) || 0))}
              placeholder="0"
              className="w-full bg-gray-50 dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 text-gray-900 dark:text-white rounded-xl px-4 py-3.5 focus:ring-2 focus:ring-[#0F172A] dark:focus:ring-white/20 focus:border-transparent outline-none transition-all font-mono font-bold"
            />
          </div>
          {role === 'admin' && (
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-bold text-gray-700">Level 3 Members</label>
                <span className="text-[10px] uppercase tracking-widest font-black text-[#EF4444] bg-[#EF4444]/10 px-2.5 py-1 rounded-full">4% Comm.</span>
              </div>
              <input 
                type="number" 
                min="0"
                value={l3Count || ''}
                onChange={(e) => setL3Count(Math.max(0, parseInt(e.target.value) || 0))}
                placeholder="0"
                className="w-full bg-gray-50 dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 text-gray-900 dark:text-white rounded-xl px-4 py-3.5 focus:ring-2 focus:ring-[#0F172A] dark:focus:ring-white/20 focus:border-transparent outline-none transition-all font-mono font-bold"
              />
            </div>
          )}
        </div>
        <div className="bg-gradient-to-br from-[#0F172A] to-[#0F172A] text-white rounded-3xl p-8 flex flex-col justify-center items-center text-center shadow-2xl relative overflow-hidden group border border-[#0F172A]/20">
          <div className="absolute top-0 right-0 -mt-10 -mr-10 w-40 h-40 bg-[#EF4444] opacity-30 rounded-full blur-2xl group-hover:scale-125 group-hover:opacity-40 transition-all duration-700 pointer-events-none" />
          
          <span className="text-white/80 font-bold uppercase tracking-widest text-xs mb-4 z-10">Estimated Monthly Earnings</span>
          <span className="text-4xl md:text-5xl lg:text-6xl font-black text-white drop-shadow-md mb-6 z-10 font-mono tracking-tighter">
            {currencyFormatter.format(totalEarnings).replace('NGN', '₦').trim()}
          </span>
          <div className="h-1.5 w-12 bg-gradient-to-r from-[#EF4444] to-[#EF4444]/80 rounded-full mb-6 z-10" />
          <p className="text-white/70 text-sm max-w-[250px] font-medium z-10 leading-relaxed mb-6">
            This is an estimate based on {role === 'admin' ? '3' : '2'} levels of your network downline.
          </p>
        </div>
      </div>
    </motion.div>
  );
}

function UserSalesHistory() {
  const { profile } = useAuth();
  const [sales, setSales] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMySales = async () => {
      if (!profile) return;
      try {
        const data = await sanityClient.fetch(`*[_type == "sale" && userId == $userId] | order(createdAt desc)`, { userId: profile._id || profile.id });
        setSales(data);
      } catch (err) {
        console.error("Error fetching user sales", err);
      } finally {
        setLoading(false);
      }
    };
    fetchMySales();
  }, [profile]);

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.3 }} className="bg-white dark:bg-[#0F172A] rounded-3xl shadow-lg border border-gray-200 dark:border-white/10 p-8 md:p-10 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-[#EF4444]/5 dark:from-transparent to-transparent opacity-50 pointer-events-none" />
      <div className="flex items-center gap-4 mb-8 relative z-10">
        <div className="bg-[#EF4444] p-3.5 rounded-2xl shadow-md text-white">
          <History size={28} />
        </div>
        <div>
          <h3 className="text-2xl font-black text-gray-900 dark:text-white tracking-tight">
            My Sales History
          </h3>
          <p className="text-gray-600 dark:text-gray-400 text-sm font-medium">Track your logged property sales and commission status</p>
        </div>
      </div>

      <div className="overflow-x-auto w-full relative z-10">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-gray-200 dark:border-white/10">
              <th className="py-3 px-4 text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest">Property</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest">Amount (₦)</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest">Date Sold</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest">Approval Status</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest text-right">Payout Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-white/5">
            {loading ? (
              <tr><td colSpan={5} className="py-8 text-center text-sm text-gray-600 dark:text-gray-400">Loading your sales...</td></tr>
            ) : sales.length === 0 ? (
              <tr><td colSpan={5} className="py-8 text-center text-sm text-gray-600 dark:text-gray-400">You haven't logged any sales yet.</td></tr>
            ) : (
              sales.map((s) => (
                <tr key={s._id} className="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
                  <td className="py-3 px-4 text-sm font-bold text-gray-900 dark:text-white">{s.propertyName || 'N/A'}</td>
                  <td className="py-3 px-4 text-sm font-mono text-gray-900 dark:text-white">₦{s.amount?.toLocaleString()}</td>
                  <td className="py-3 px-4 text-sm text-gray-600 dark:text-gray-400">{s.dateSold ? new Date(s.dateSold).toLocaleDateString() : 'N/A'}</td>
                  <td className="py-3 px-4">
                    {s.status === 'pending' ? (
                      <span className="inline-block px-2 py-1 bg-yellow-100 text-yellow-800 text-[10px] font-bold rounded">PENDING</span>
                    ) : s.status === 'approved' ? (
                      <span className="inline-block px-2 py-1 bg-green-100 text-green-800 text-[10px] font-bold rounded">APPROVED</span>
                    ) : (
                      <span className="inline-block px-2 py-1 bg-red-100 text-red-800 text-[10px] font-bold rounded">REJECTED</span>
                    )}
                  </td>
                  <td className="py-3 px-4 text-right">
                    {s.payoutStatus === 'paid' ? (
                      <span className="inline-block px-2 py-1 bg-blue-100 text-blue-800 text-[10px] font-bold rounded">PAID</span>
                    ) : (
                      <span className="inline-block px-2 py-1 bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300 text-[10px] font-bold rounded">PENDING</span>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </motion.div>
  );
}

export function Dashboard() {
  const { user, profile, signOut } = useAuth();
  const [showToast, setShowToast] = useState(false);
  const [downline, setDownline] = useState<(UserProfile & { id: string })[]>([]);
  const [level2Downline, setLevel2Downline] = useState<(UserProfile & { id: string })[]>([]);
  const [level3Downline, setLevel3Downline] = useState<(UserProfile & { id: string })[]>([]);
  const [allUsers, setAllUsers] = useState<(UserProfile & { id: string })[]>([]);
  const [loading, setLoading] = useState(true);
  const [sponsorName, setSponsorName] = useState<string>('Admin');
  const [showNotifications, setShowNotifications] = useState(false);
    const navigate = useNavigate();
  
  const unreadCount = profile?.notifications?.filter(n => !n.read).length || 0;
  
  const handleOpenNotifications = async () => {
    setShowNotifications(!showNotifications);
    if (!showNotifications && unreadCount > 0) {
      try {
        await fetch('/api/auth/notifications/read', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userId: profile._id })
        });
        // Mutate local profile optimistically if possible, or it'll refresh on reload
      } catch (e) {
        console.error(e);
      }
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      if (!user || !profile) return;
      
      try {
        if (profile.isAdmin || profile.role === 'admin') {
          const users = await sanityClient.fetch(`*[_type == "user"]`);
          setAllUsers(users.map((u: any) => ({ ...u, id: u._id })));
        } else {
          // Fetch downline using Nested Set Model bounds
          const allDescendantsRaw = await sanityClient.fetch(`*[_type == "user" && lft > $lft && rgt < $rgt]`, { lft: profile.lft, rgt: profile.rgt });
          const allDescendants = allDescendantsRaw.map((u: any) => ({ ...u, id: u._id }));
          
          // For the ReferralTree, we need to provide the user themselves as the root
          setAllUsers([{ ...profile, id: profile._id || profile.id || '' }, ...allDescendants]);

          // We can group them by level in memory by building a quick lookup
          const idToNode = new Map<string, any>();
          idToNode.set(profile.referralCode, { ...profile, __level: 0 });
          idToNode.set(profile._id, { ...profile, __level: 0 }); // fallback for sponsorId as UID
          
          allDescendants.forEach((u: any) => {
              idToNode.set(u.referralCode, { ...u, __level: -1 });
              idToNode.set(u.id, { ...u, __level: -1 });
          });

          // Calculate levels
          let changed = true;
          while (changed) {
              changed = false;
              allDescendants.forEach((u: any) => {
                  const node = idToNode.get(u.id);
                  if (node.__level === -1) {
                      const parent = idToNode.get(u.sponsorId);
                      if (parent && parent.__level >= 0) {
                          node.__level = parent.__level + 1;
                          idToNode.set(u.referralCode, node);
                          idToNode.set(u.id, node);
                          changed = true;
                      }
                  }
              });
          }

          const l1Users = allDescendants.filter((u: any) => idToNode.get(u.id).__level === 1);
          const l2Users = allDescendants.filter((u: any) => idToNode.get(u.id).__level === 2);
          const l3Users = allDescendants.filter((u: any) => idToNode.get(u.id).__level === 3);
          
          setDownline(l1Users);
          setLevel2Downline(l2Users);
          setLevel3Downline(l3Users);

          // Fetch sponsor name
          if (profile.sponsorId && profile.sponsorId !== 'admin') {
            const sponsorDoc = await sanityClient.fetch(`*[_type == "user" && (referralCode == $sid || _id == $sid)][0]`, { sid: profile.sponsorId });
            if (sponsorDoc) {
              setSponsorName(sponsorDoc.displayName || 'Unknown');
            }
          }
        }
      } catch (err: any) {
        console.error("Missing Sanity Project ID or API Token. Please check your environment variables.", err);
        // Fallback for dashboard error state
        alert("Missing Sanity Project ID or API Token. Please check your environment variables.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user, profile]);

  const isFirstLogin = profile?.createdAt === profile?.lastLoginAt;

  const copyReferralLink = (e: React.MouseEvent) => {
    e.stopPropagation();
    e.preventDefault();
    const refString = profile?.firstName ? `${profile.firstName.replace(/\s+/g, "")}-${profile.referralCode}` : profile?.referralCode;
    const link = `https://globalsaleselite.com/signup?ref=${refString}`;
    navigator.clipboard.writeText(link);
    setShowToast(true);
    setTimeout(() => setShowToast(false), 3000);
  };

  if (!profile || loading) {
    return <div className="min-h-screen bg-gray-50 flex items-center justify-center font-bold text-xl text-[#0F172A] dark:text-white">Loading...</div>;
  }

  return (
    <div className="w-full bg-gray-50 dark:bg-[#020617] flex flex-col font-sans relative pb-12 transition-colors duration-300">
      {/* Toast Notification */}
      <div className={`fixed top-6 right-6 z-[100] transition-all duration-300 transform ${showToast ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0 pointer-events-none'}`}>
        <div className="bg-[#10B981] text-white px-6 py-4 rounded-xl shadow-2xl flex items-center gap-3 font-semibold text-sm">
          <div className="bg-white/20 p-1.5 rounded-full">
            <Copy size={16} className="text-white" />
          </div>
          Referral link copied to clipboard!
        </div>
      </div>
      <Navbar />

      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 pt-32 pb-12 space-y-8">
        
        {/* Header Section */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }} className="bg-gradient-to-br from-[#0F172A] to-[#0F172A] rounded-3xl shadow-xl border border-[#0F172A]/20 p-8 md:p-10 flex flex-col md:flex-row gap-8 justify-between items-start md:items-center relative overflow-hidden">
          <div className="absolute top-0 right-0 -mt-16 -mr-16 w-64 h-64 bg-white opacity-5 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute bottom-0 left-0 -mb-16 -ml-16 w-48 h-48 bg-[#EF4444] opacity-10 rounded-full blur-2xl pointer-events-none" />
          
          <div className="relative z-10 text-white">
            <div className="flex items-center gap-6 mb-2">
              <ProfilePhotoUpload className="w-16 h-16 sm:w-20 sm:h-20 text-xl" />
              <h2 className="text-3xl md:text-4xl font-black tracking-tight drop-shadow-sm">
                {isFirstLogin ? 'Welcome' : 'Welcome back'}, <span className="text-[#EF4444]">{profile.firstName || profile.displayName?.split(' ')[0]}</span>
              </h2>
            </div>
            <p className="text-white/80 text-lg max-w-xl font-medium">
              {profile.isAdmin || profile.role === 'admin' 
                ? "You have full administrative access to monitor and manage the Global Sales Elite network." 
                : `Continue building your network. Your current sponsor is ${sponsorName}.`}
            </p>
          </div>
          
          <div className="relative z-10 bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-5 flex flex-col gap-3 min-w-[320px] shadow-2xl">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-white/90 uppercase tracking-widest flex items-center gap-2">
                <LinkIcon size={14} className="text-[#EF4444]" /> Your Referral Link
              </span>
            </div>
            <div className="flex items-center gap-2">
              <input 
                type="text" 
                readOnly 
                value={`https://globalsaleselite.com/signup?ref=${profile?.firstName ? `${profile.firstName.replace(/\s+/g, "")}-${profile.referralCode}` : profile?.referralCode}`}
                className="flex-1 bg-white/10 border border-white/20 text-sm text-white rounded-xl px-4 py-3 outline-none focus:border-white/40 transition-colors font-mono"
              />
              <button 
                onClick={copyReferralLink}
                className="bg-[#EF4444] hover:bg-[#c9291f] text-white px-4 py-3 rounded-xl transition-colors shadow-lg hover:shadow-xl hover:-translate-y-0.5 duration-200 flex items-center gap-2 font-bold text-sm"
              >
                <Copy size={16} /> Copy
              </button>
            </div>
          </div>
        </motion.div>

        {/* Network Section */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.3 }} className="bg-white dark:bg-[#0F172A] rounded-3xl shadow-lg border border-gray-200 dark:border-white/10 p-6 md:p-8 relative overflow-hidden">
          <div className="flex items-center gap-4 mb-6 border-b border-gray-100 pb-6 relative z-10">
            <div className="bg-gray-100 dark:bg-[#0F172A] p-3 rounded-2xl text-[#0F172A] dark:text-white">
              <Network size={28} />
            </div>
            <div>
              <h3 className="text-2xl font-black text-gray-900 dark:text-white tracking-tight">
                {profile.role === 'admin' ? 'Global Network Tree' : 'Your Downline'}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm font-medium mt-1">Explore and manage your connections</p>
            </div>
          </div>
          
          <div className="relative z-10">
            <ReferralTree 
              users={allUsers} 
              rootUserId={profile.role === 'admin' ? undefined : (profile.id || profile._id)} 
              isAdminView={profile.role === 'admin' || profile.isAdmin}
            />
          </div>
        </motion.div>

        <SalesLogger />
        <UserSalesHistory />
        <CommissionCalculator 
          role={profile.role} 
          defaultL1={downline.length} 
          defaultL2={level2Downline.length} 
          defaultL3={level3Downline.length} 
        />
      </main>
    </div>
  );
}

