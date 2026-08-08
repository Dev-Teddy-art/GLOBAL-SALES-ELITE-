import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, UserProfile } from '../contexts/AuthContext';
import { sanityClient } from '../lib/sanity';
import { motion, AnimatePresence } from 'motion/react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ThemeToggle } from './ThemeToggle';
import { Navbar } from './Navbar';
import { Shield, ChevronLeft, ChevronDown, ChevronRight, CheckCircle, DollarSign, Activity, Users, Search, AlertCircle, LayoutDashboard, Database, Link as LinkIcon, Network, Crown, Landmark, History, Terminal, Check, UserCheck, ScrollText, Waypoints } from 'lucide-react';

// Specialized Admin Binary Tree Component
function AdminBinaryTree({ users, onManageUser }: { users: (UserProfile & { id: string })[], onManageUser?: (u: any) => void }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [inspectModalUser, setInspectModalUser] = useState<any>(null);
  const [focusedId, setFocusedId] = useState<string | null>(null);

  // Build a fast lookup and basic tree structure
  const { nodeMap, roots } = useMemo(() => {
    const map = new Map<string, any>();
    users.forEach(u => {
      map.set(u.id, { ...u, children: [], left: null, right: null });
      if (u.referralCode) {
        map.set(u.referralCode, map.get(u.id));
      }
    });

    const rootNodes: any[] = [];
    users.forEach(u => {
      const node = map.get(u.id);
      if (u.sponsorId && u.sponsorId !== 'admin') {
        const parent = (map.get(u.sponsorId) || Array.from(map.values()).find((n: any) => n.referralCode === u.sponsorId || n.email === u.sponsorId));
        if (parent) {
          parent.children.push(node);
          // Assign L/R conceptually for binary visual (first child L, second R)
          if (!parent.left) parent.left = node;
          else if (!parent.right) parent.right = node;
        } else {
          rootNodes.push(node);
        }
      } else {
        rootNodes.push(node);
      }
    });
    return { nodeMap: map, roots: rootNodes };
  }, [users]);

  const displayRoot = useMemo(() => {
    if (focusedId && nodeMap.get(focusedId)) {
      return [nodeMap.get(focusedId)];
    }
    const adminRoot = users.find(u => u.role === 'admin' || u.isAdmin);
    if (adminRoot && nodeMap.get(adminRoot.id)) {
      return [nodeMap.get(adminRoot.id)];
    }
    return roots;
  }, [roots, nodeMap, focusedId, users]);

  const filteredUsers = useMemo(() => {
    if (!searchTerm) return [];
    return users.filter(u => 
      (u?.displayName || u?.name || "").toLowerCase().includes(searchTerm.toLowerCase()) ||
      (u?.email || "").toLowerCase().includes(searchTerm.toLowerCase()) ||
      (u?.referralCode || "").toLowerCase().includes(searchTerm.toLowerCase())
    ).slice(0, 5);
  }, [users, searchTerm]);

  return (
    <div className="bg-white/90 dark:bg-[#0F172A]/80 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-3xl p-6 h-[800px] flex flex-col relative overflow-hidden">
      {/* Background Orbs */}
      <div className="absolute top-0 right-0 -mt-20 -mr-20 w-72 h-72 bg-[#0F172A] dark:bg-[#0F172A] opacity-5 dark:opacity-20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-64 h-64 bg-[#EF4444] dark:bg-[#EF4444] opacity-5 dark:opacity-10 rounded-full blur-3xl pointer-events-none" />
      
      {/* Search Header */}
      <div className="relative z-20 flex flex-col sm:flex-row items-center justify-between gap-4 mb-6">
        <h3 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
          <Waypoints className="text-[#EF4444]" />
          Visual Binary Inspector
        </h3>
        
        <div className="relative w-full sm:w-72">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-4 w-4 text-gray-600 dark:text-gray-400" />
          </div>
          <input
            type="text"
            placeholder="Search by name, email, or code..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="w-full bg-white dark:bg-white/80 dark:bg-[#1E293B]/80 border border-gray-200 dark:border-white/10 rounded-xl pl-10 pr-4 py-2.5 text-sm text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:border-[#EF4444] transition-colors"
          />
          
          {/* Search Dropdown */}
          <AnimatePresence>
            {searchTerm && filteredUsers.length > 0 && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 rounded-xl shadow-2xl overflow-hidden z-50"
              >
                {filteredUsers.map(u => (
                  <button
                    key={u.id}
                    onClick={() => {
                      setFocusedId(u.id);
                      setSearchTerm('');
                    }}
                    className="w-full text-left px-4 py-3 hover:bg-white/5 transition-colors border-b border-gray-200 dark:border-white/5 last:border-0"
                  >
                    <div className="font-semibold text-gray-900 dark:text-white text-sm">{u.displayName}</div>
                    <div className="text-xs text-gray-600 dark:text-gray-400 font-mono">{u.referralCode}</div>
                  </button>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {focusedId && (
        <div className="mb-4 flex items-center gap-3 bg-[#EF4444]/5 dark:bg-[#EF4444]/10 border border-[#EF4444]/20 p-3 rounded-xl relative z-20 w-max">
          <span className="text-sm text-[#EF4444]">Focused: <strong>{nodeMap.get(focusedId)?.displayName}</strong></span>
          <button 
            onClick={() => {
              const u = nodeMap.get(focusedId);
              if (u) {
                setModalUser(u || nodeMap.get(focusedId) || rootUser);
              }
            }}
            className="text-xs bg-blue-600 text-white px-3 py-1 rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
          >
            Manage User
          </button>
          <button 
            onClick={() => setFocusedId(null)}
            className="text-xs bg-gray-200 dark:bg-gray-800 text-gray-900 dark:text-white px-3 py-1 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-700 transition-colors"
          >
            Reset
          </button>
        </div>
      )}

      {/* Tree Canvas */}
      <div className="flex-1 overflow-auto relative z-10 custom-scrollbar pr-2 pb-10">
        <div className="min-w-[600px] flex flex-col items-center pt-8">
          {displayRoot.length === 0 ? (
            <div className="text-gray-600 dark:text-gray-400 mt-20">No network data.</div>
          ) : (
            displayRoot.map(root => (
              <AdminTreeNode key={root.id} node={root} level={0} />
            ))
          )}
        </div>
      </div>
    </div>

  );
}

const AdminTreeNode: React.FC<{ node: any, level: number }> = ({ node, level }) => {
  const [expanded, setExpanded] = useState(true);
  const hasChildren = node.children && node.children.length > 0;

  return (
    <div className="flex flex-col items-center">
      {/* Node Card */}
      <motion.div 
        whileHover={{ scale: 1.05 }}
        className={`relative z-10 w-64 bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 rounded-2xl p-4 shadow-xl flex flex-col items-center gap-2 cursor-pointer transition-colors ${expanded ? 'border-gray-300 dark:border-white/20' : ''}`}
        onClick={() => hasChildren && setExpanded(!expanded)}
      >
        <div className={`absolute top-0 right-0 w-2 h-2 rounded-full m-3 ${node.isAdmin || node.role === 'admin' ? 'bg-[#EF4444]' : 'bg-[#0F172A]'} shadow-[0_0_8px_rgba(52,211,153,0.8)]`} />
        
        <div className={`h-12 w-12 rounded-full bg-gradient-to-br ${node.isAdmin || node.role === 'admin' ? 'from-[#EF4444]/20 to-[#EF4444]/10 text-[#EF4444]' : 'from-[#0F172A] to-[#0F172A] text-white'} flex items-center justify-center font-bold text-lg shadow-inner border border-gray-200 dark:border-white/10 overflow-hidden`}>
          {(node.profileImage || node.avatarUrl) ? (
            <img src={node.profileImage || node.avatarUrl} alt="Avatar" className="w-full h-full object-cover" />
          ) : (node.isAdmin || node.role === 'admin') ? (
            <Crown size={20} />
          ) : (
            node.displayName?.charAt(0).toUpperCase() || 'U'
          )}
        </div>
        <div className="text-center">
          <h4 className="font-bold text-gray-900 dark:text-white text-sm truncate w-56">{node.displayName}</h4>
          <span className="text-[10px] font-mono text-[#EF4444] bg-[#EF4444]/5 dark:bg-[#EF4444]/10 px-2 py-0.5 rounded mt-1 inline-block border border-[#EF4444]/20">
            {node.referralCode}
          </span>
        </div>

        {/* L / R Slots Indicators */}
        <div className="flex gap-2 w-full mt-2 pt-2 border-t border-gray-200 dark:border-white/5">
          <div className={`flex-1 text-center py-1 rounded text-xs font-bold ${node.left ? 'bg-[#0F172A]/40 text-white' : 'bg-gray-800/50 text-gray-600 dark:text-gray-400 border border-dashed border-gray-700'}`}>
            {node.left ? 'L' : 'L (Open)'}
          </div>
          <div className={`flex-1 text-center py-1 rounded text-xs font-bold ${node.right ? 'bg-[#EF4444]/40 text-[#EF4444]' : 'bg-gray-800/50 text-gray-600 dark:text-gray-400 border border-dashed border-gray-700'}`}>
            {node.right ? 'R' : 'R (Open)'}
          </div>
        </div>
      </motion.div>

      {/* Children & Connectors */}
      <AnimatePresence>
        {expanded && hasChildren && (
          <motion.div 
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="flex flex-col items-center w-full"
          >
            {/* Vertical stem */}
            <div className="w-px h-8 bg-gradient-to-b from-white/20 to-white/5" />
            
            {/* Horizontal connector (if multiple children) */}
            {node.children.length > 1 && (
              <div className="w-[calc(100%-16rem)] h-px bg-white/10 relative">
                <div className="absolute left-0 top-0 w-px h-6 bg-white/10" />
                <div className="absolute right-0 top-0 w-px h-6 bg-white/10" />
              </div>
            )}
            
            {/* Children container */}
            <div className={`flex gap-8 justify-center ${node.children.length > 1 ? 'pt-6' : ''}`}>
              {node.children.map((child: any) => (
                <AdminTreeNode key={child.id} node={child} level={level + 1} />
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>

  );
}


function SalesTrendChart({ sales }: { sales: any[] }) {
  const chartData = useMemo(() => {
    // Group sales by day over the last 30 days
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(today.getDate() - 29);

    const dataMap = new Map<string, number>();
    for (let i = 0; i < 30; i++) {
      const d = new Date(thirtyDaysAgo);
      d.setDate(thirtyDaysAgo.getDate() + i);
      const dateStr = d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
      dataMap.set(dateStr, 0);
    }

    sales.forEach(sale => {
      // Use dateSold or createdAt
      const d = new Date(sale.dateSold || sale.createdAt);
      if (d >= thirtyDaysAgo) {
        const dateStr = d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
        if (dataMap.has(dateStr)) {
          // Track approved sales volume
          if (sale.status === 'approved') {
            dataMap.set(dateStr, dataMap.get(dateStr)! + (Number(sale.amount) || 0));
          }
        }
      }
    });

    return Array.from(dataMap.entries()).map(([date, volume]) => ({ date, volume }));
  }, [sales]);

  return (
    <div className="bg-white/90 dark:bg-[#0F172A]/80 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col w-full relative z-10 mt-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
          <Activity className="text-[#0F172A] dark:text-white" size={20} />
          30-Day Approved Sales Trend
        </h3>
      </div>
      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(128,128,128,0.2)" vertical={false} />
            <XAxis dataKey="date" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} tickMargin={10} />
            <YAxis stroke="#888888" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `₦${(value / 1000).toFixed(0)}k`} width={60} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1E293B', borderColor: 'rgba(255,255,255,0.1)', color: '#fff', borderRadius: '12px' }}
              itemStyle={{ color: '#10B981', fontWeight: 'bold' }}
              formatter={(value: number) => [`₦${value.toLocaleString()}`, 'Volume']}
            />
            <Line type="monotone" dataKey="volume" stroke="#10B981" strokeWidth={4} dot={{ r: 4, fill: '#1E293B', strokeWidth: 2, stroke: '#10B981' }} activeDot={{ r: 6, fill: '#10B981' }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function SalesHistoryTable({ sales, onTogglePayout, onDeleteSale }: { sales: any[], onTogglePayout: (id: string, currentStatus: string) => void, onDeleteSale: (id: string) => void }) {
  const approvedSales = sales.filter(s => s.status === 'approved');
  
  const pendingPayouts = approvedSales.filter(s => s.payoutStatus !== 'paid');
  const paidPayouts = approvedSales.filter(s => s.payoutStatus === 'paid');

  const pendingVolume = pendingPayouts.reduce((sum, s) => sum + (Number(s.commission || s.commissionAmount || (s.amount * 0.15)) || 0), 0);
  const paidVolume = paidPayouts.reduce((sum, s) => sum + (Number(s.commission || s.commissionAmount || (s.amount * 0.15)) || 0), 0);

  const [saleToDelete, setSaleToDelete] = useState<string | null>(null);

  return (
    <div className="w-full mt-8 flex flex-col gap-6">
      <AnimatePresence>
        {saleToDelete && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 p-4">
            <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.95 }} className="bg-white dark:bg-[#1E293B] rounded-2xl shadow-xl p-6 max-w-sm w-full">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Delete Sale?</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">Are you sure you want to permanently delete this sale record? This action cannot be undone.</p>
              <div className="flex gap-3 justify-end">
                <button onClick={() => setSaleToDelete(null)} className="px-4 py-2 rounded-xl text-sm font-bold text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-white/10 transition-colors">Cancel</button>
                <button 
                  onClick={() => {
                    onDeleteSale(saleToDelete);
                    setSaleToDelete(null);
                  }} 
                  className="px-4 py-2 rounded-xl text-sm font-bold bg-[#EF4444] text-white hover:bg-red-600 transition-colors"
                >
                  Delete
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 relative z-10">
        <div className="bg-white/90 dark:bg-[#0F172A]/80 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-3xl p-6 shadow-xl flex flex-col relative overflow-hidden">
           <h3 className="text-sm font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest mb-1">Total Payouts Pending</h3>
           <p className="text-3xl font-black text-yellow-600 dark:text-yellow-400 font-mono">
             ₦{pendingVolume.toLocaleString()}
           </p>
           <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 font-bold">{pendingPayouts.length} Approved Sales awaiting payout</p>
        </div>
        <div className="bg-white/90 dark:bg-[#0F172A]/80 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-3xl p-6 shadow-xl flex flex-col relative overflow-hidden">
           <h3 className="text-sm font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest mb-1">Total Payouts Paid</h3>
           <p className="text-3xl font-black text-green-600 dark:text-green-400 font-mono">
             ₦{paidVolume.toLocaleString()}
           </p>
           <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 font-bold">{paidPayouts.length} Completed Payouts</p>
        </div>
      </div>

      <div className="bg-white/90 dark:bg-[#0F172A]/80 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col w-full relative z-10">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
          <History className="text-[#0F172A] dark:text-white" size={20} />
          Full Sales History & Payouts
        </h3>
      </div>
      
      <div className="overflow-x-auto w-full">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-gray-200 dark:border-white/10">
              <th className="py-3 px-4 text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest">Realtor Name</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest">Property</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest">Amount (₦)</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest">Date</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest">Approval Status</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest text-right">Payout Status</th>
              <th className="py-3 px-4 text-xs font-bold text-gray-600 dark:text-gray-400 uppercase tracking-widest text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-white/5">
            {sales.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-8 text-center text-sm text-gray-600 dark:text-gray-400">No sales recorded yet.</td>
              </tr>
            ) : (
              sales.map((s) => (
                <tr key={s._id} className="hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
                  <td className="py-3 px-4 text-sm font-bold text-gray-900 dark:text-white">
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-full bg-gray-200 dark:bg-[#0F172A] flex items-center justify-center text-[10px] overflow-hidden flex-shrink-0">
                        {(s.userRef?.profileImage || s.userRef?.avatarUrl) ? (
                          <img src={s.userRef?.profileImage || s.userRef?.avatarUrl} alt="Avatar" className="w-full h-full object-cover" />
                        ) : (
                          (s.userRef?.displayName?.charAt(0).toUpperCase() || 'U')
                        )}
                      </div>
                      {s.userRef?.displayName || 'Unknown'}
                    </div>
                  </td>
                  <td className="py-3 px-4 text-sm text-gray-700 dark:text-gray-300">
                    {s.propertyName || 'N/A'}
                  </td>
                  <td className="py-3 px-4 text-sm font-mono text-gray-900 dark:text-white">
                    ₦{s.amount?.toLocaleString()}
                  </td>
                  <td className="py-3 px-4 text-sm text-gray-600 dark:text-gray-400">
                    {s.dateSold ? new Date(s.dateSold).toLocaleDateString() : 'N/A'}
                  </td>
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
                    <button 
                      onClick={() => onTogglePayout(s._id, s.payoutStatus || 'pending')}
                      className={`inline-block px-3 py-1 text-[10px] font-bold rounded cursor-pointer transition-colors ${s.payoutStatus === 'paid' ? 'bg-blue-100 text-blue-800 hover:bg-blue-200' : 'bg-gray-100 text-gray-800 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600'}`}
                    >
                      {s.payoutStatus === 'paid' ? 'PAID' : 'PENDING'}
                    </button>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <button 
                      onClick={() => setSaleToDelete(s._id)}
                      className="text-gray-400 hover:text-[#EF4444] transition-colors p-1"
                      title="Delete Sale"
                    >
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"></path><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
    </div>
  );
}

function SalesApprovals({ sales, loading, onProcess }: { sales: any[], loading: boolean, onProcess: (id: string, status: 'approved' | 'rejected') => void }) {
  const pendingSales = sales.filter(s => !s.status || s.status.toLowerCase() === 'pending');
  const handleProcess = onProcess;


  return (
    <>
      <div className="bg-white/90 dark:bg-[#0F172A]/80 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col h-[380px] relative z-10">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Landmark className="text-[#0F172A] dark:text-white" size={20} />
            Sales & Commission Requests
          </h3>
          <span className="bg-[#EF4444] text-white text-xs font-bold px-2.5 py-1 rounded-full">{pendingSales.length}</span>
        </div>
        
        <div className="flex-1 overflow-auto custom-scrollbar pr-2 space-y-3">
          {loading ? (
            <div className="text-gray-600 dark:text-gray-400 text-center py-10 text-sm">Loading...</div>
          ) : sales.length === 0 ? (
            <div className="text-gray-600 dark:text-gray-400 text-center py-10 text-sm">No sales logged yet.</div>
          ) : (
            pendingSales.map((w) => (
              <motion.div 
                key={w._id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-gray-50 dark:bg-[#1E293B] border border-gray-200 dark:border-white/5 rounded-xl p-4 flex flex-col gap-3 group hover:border-[#EF4444]/30 transition-colors"
              >
                <div className="flex justify-between items-start">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-[#10B981]/10 flex items-center justify-center text-[#10B981] overflow-hidden">
                      {(w.userRef?.profileImage || w.userRef?.avatarUrl) ? (
                        <img src={w.userRef?.profileImage || w.userRef?.avatarUrl} alt="Avatar" className="w-full h-full object-cover" />
                      ) : (
                        <Landmark size={20} />
                      )}
                    </div>
                    <div>
                      <p className="text-sm font-bold text-gray-900 dark:text-white leading-none">{w.propertyName || 'Property Sale'}</p>
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">Sold by: <strong>{w.userRef?.displayName}</strong></p>
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-0.5">Date: {w.dateSold ? new Date(w.dateSold).toLocaleDateString() : 'N/A'}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-black text-gray-900 dark:text-white">₦{w.amount?.toLocaleString()}</p>
                    {w.status === 'pending' ? (
                      <span className="inline-block mt-1 px-2 py-0.5 bg-yellow-100 text-yellow-800 text-[10px] font-bold rounded">PENDING</span>
                    ) : w.status === 'approved' ? (
                      <span className="inline-block mt-1 px-2 py-0.5 bg-green-100 text-green-800 text-[10px] font-bold rounded">APPROVED</span>
                    ) : (
                      <span className="inline-block mt-1 px-2 py-0.5 bg-red-100 text-red-800 text-[10px] font-bold rounded">REJECTED</span>
                    )}
                  </div>
                </div>
                
                <div className="bg-gray-100 dark:bg-[#0F172A] p-2 rounded-lg flex justify-between items-center text-xs">
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">Bank:</span> <span className="font-bold text-gray-700 dark:text-gray-300">{w.userRef?.bankName || 'N/A'}</span>
                    <span className="mx-2 text-gray-400 dark:text-gray-600">|</span>
                    <span className="text-gray-600 dark:text-gray-400">Acc:</span> <span className="font-mono text-gray-700 dark:text-gray-300">{w.userRef?.bankAccountNumber || 'N/A'}</span>
                  </div>
                </div>

                {w.status === 'pending' && (
                  <div className="flex gap-2 justify-end mt-1">
                    <button onClick={() => handleProcess(w._id, 'approved')} className="text-xs font-bold bg-[#10B981] text-white hover:bg-[#059669] px-4 py-1.5 rounded-lg transition-colors shadow-sm">
                      Mark Paid
                    </button>
                    <button onClick={() => handleProcess(w._id, 'rejected')} className="text-xs font-bold bg-gray-200 text-gray-700 hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600 px-4 py-1.5 rounded-lg transition-colors">
                      Reject
                    </button>
                  </div>
                )}
              </motion.div>
            ))
          )}
        </div>
      </div>
    </>
  );
}

function SystemLogs({ users }: { users: any[] }) {
  // Use real data (recent users) to generate logs instead of mock data
  const recentUsers = [...users].sort((a, b) => new Date(b.createdAt || 0).getTime() - new Date(a.createdAt || 0).getTime()).slice(0, 5);
  
  return (
    <div className="bg-white/90 dark:bg-[#0F172A]/80 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col h-[396px]">
      <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2 mb-4">
        <Terminal className="text-[#0F172A] dark:text-white" size={20} />
        System Logs
      </h3>
      
      <div className="flex-1 overflow-auto custom-scrollbar pr-2 space-y-4">
        {recentUsers.length === 0 ? (
          <div className="text-gray-600 dark:text-gray-400 text-center py-10 text-sm">No recent activity.</div>
        ) : (
          recentUsers.map((u, i) => (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 + 0.3 }}
              key={u.id || i} 
              className="flex gap-3 items-start p-2 hover:bg-gray-50 dark:hover:bg-white/5 rounded-xl transition-colors"
            >
              <div className="w-8 h-8 rounded-full flex-shrink-0 bg-gray-200 dark:bg-[#0F172A] flex items-center justify-center text-xs overflow-hidden font-bold">
                {(u.profileImage || u.avatarUrl) ? (
                  <img src={u.profileImage || u.avatarUrl} alt="Avatar" className="w-full h-full object-cover" />
                ) : (
                  (u.displayName?.charAt(0).toUpperCase() || 'U')
                )}
              </div>
              <div className="pt-0.5">
                <p className="text-sm font-bold text-gray-900 dark:text-gray-200 leading-tight">New user joined</p>
                <p className="text-xs text-gray-700 dark:text-gray-400 mt-0.5">{u.displayName}</p>
                <span className="text-[10px] text-gray-600 dark:text-gray-400 block mt-1">{new Date(u.createdAt || Date.now()).toLocaleDateString()}</span>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </div>

  );
}


const confettiParticles = Array.from({ length: 50 }).map((_, i) => ({
  id: i,
  color: ['bg-[#10B981]', 'bg-[#EF4444]', 'bg-blue-500', 'bg-yellow-400', 'bg-purple-500'][Math.floor(Math.random() * 5)],
  angle: Math.random() * Math.PI * 2,
  velocity: 15 + Math.random() * 30,
  size: 6 + Math.random() * 8
}));

function SuccessAnimation({ show, message, type = 'success' }: { show: boolean, message?: string, type?: 'success' | 'info' }) {
  return (
    <AnimatePresence>
      {show && (
        <div className="fixed inset-0 pointer-events-none z-[200] flex items-center justify-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.5, y: 50 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: -20 }}
            className={`absolute bg-white dark:bg-[#1E293B] px-8 py-5 rounded-2xl shadow-2xl flex items-center gap-4 border ${type === 'success' ? 'border-[#10B981]/20' : 'border-blue-500/20'} z-10`}
          >
            <div className={`${type === 'success' ? 'bg-[#10B981]' : 'bg-blue-500'} p-2 rounded-full text-white shadow-md`}>
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

export function AdminConsolePage() {
  const [isManageModalOpen, setIsManageModalOpen] = useState(false);
  const { profile } = useAuth();
  const navigate = useNavigate();
  const [users, setUsers] = useState<(UserProfile & { id: string })[]>([]);
  const [sales, setSales] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [salesLoading, setSalesLoading] = useState(true);
  const [editingUser, setEditingUser] = useState<any>(null);
  const [editForm, setEditForm] = useState<any>({});
  const [showSuccess, setShowSuccess] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const data = await sanityClient.fetch(`*[_type == "user"]`);
        setUsers(data.map((u: any) => ({ ...u, id: u._id })));
      } catch (err) {
        console.error("Error fetching users:", err);
      } finally {
        setLoading(false);
      }
    };
    
    const fetchSales = async () => {
      if (!profile) return;
      try {
        // Fallback directly to Sanity query to bypass API routing limits
        const query = `*[_type == "sale"] | order(_createdAt desc){
          _id,
          propertyName,
          amount,
          status,
          payoutStatus,
          dateSold,
          "userRef": user->{ _id, displayName, email, profileImage, avatarUrl, bankName, bankAccountNumber, bankAccountName }
        }`;
        const data = await sanityClient.fetch(query);
        setSales(data || []);
      } catch (err) {
        console.error("Error fetching sales from Sanity", err);
        // Fallback to API endpoint if direct Sanity fetch fails
        try {
          const res = await fetch(`/api/admin/sales?adminId=${profile._id || profile.id}`);
          if (res.ok) {
            const data = await res.json();
            setSales(data);
          }
        } catch (apiErr) {
          console.error("Error fetching sales API fallback", apiErr);
        }
      } finally {
        setSalesLoading(false);
      }
    };

    fetchUsers();
    fetchSales();
  }, [profile]);

  const handleProcessSale = async (saleId: string, status: 'approved' | 'rejected') => {
    try {
      // 1. Direct mutation on Sanity document
      await sanityClient.patch(saleId).set({ status }).commit();

      // 2. Update local state immediately for instant feedback
      setSales(prev => prev.map(s => s._id === saleId ? { ...s, status } : s));

      // 3. Trigger notification to user via Zoho mail API endpoint
      const targetSale = sales.find(s => s._id === saleId);
      if (targetSale?.userRef?.email) {
        fetch('/api/send-email', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            to: targetSale.userRef.email,
            subject: `Sale Status Update: ${targetSale.propertyName || 'Property Sale'}`,
            text: `Your sale for ${targetSale.propertyName || 'Property'} has been marked as ${status.toUpperCase()}.`
          })
        }).catch(e => console.error("Zoho email trigger error", e));
      }

      const res = await fetch('/api/admin/sales/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ adminId: profile?._id || profile?.id, saleId, status })
      });
      if (res.ok) {
        setSales(sales.map(s => s._id === saleId ? { ...s, status } : s));
        if (status === 'approved') {
          setSuccessMessage("Commission Approved!");
          setShowSuccess(true);
          setTimeout(() => setShowSuccess(false), 2500);
        }
      }
    } catch (e) {
      console.error(e);
    }
  };


  const handleTogglePayout = async (saleId: string, currentStatus: string) => {
    try {
      const newStatus = currentStatus === 'paid' ? 'pending' : 'paid';
      // 1. Mutate directly in Sanity
      await sanityClient.patch(saleId).set({ payoutStatus: newStatus }).commit();

      // 2. Optimistic UI update
      setSales(prev => prev.map(s => s._id === saleId ? { ...s, payoutStatus: newStatus } : s));

      // 3. Fallback API notification
      fetch('/api/admin/sales/payout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ adminId: profile?._id || profile?.id, saleId, payoutStatus: newStatus })
      }).catch(err => console.error("API payout update silent error:", err));
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 2500);
    } catch (e) {
      console.error(e);
    }
  };

  const handleDeleteSale = async (saleId: string) => {
    try {
      await sanityClient.delete(saleId);
      setSales(prev => prev.filter(s => (s._id || s.id) !== saleId));
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 2500);
    } catch (err) {
      console.error("Failed to delete sale:", err);
    }
  };

  const handleSaveUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingUser) return;
    try {
      const res = await fetch('/api/admin/update-user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ adminId: profile?._id, userId: editingUser.id, updates: editForm })
      });
      if (res.ok) {
        setUsers(users.map(u => u.id === editingUser.id ? { ...u, ...editForm } : u));
        setEditingUser(null);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleToggleBan = async (user: any) => {
    const isBanned = user.status === 'banned';
    try {
      const res = await fetch('/api/admin/ban-user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ adminId: profile?._id, userId: user.id, banned: !isBanned })
      });
      if (res.ok) {
        setUsers(users.map(u => u.id === user.id ? { ...u, status: !isBanned ? 'banned' : 'active' } : u));
        if (editingUser?.id === user.id) {
          setEditingUser({ ...editingUser, status: !isBanned ? 'banned' : 'active' });
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  if (!profile || (profile.role !== 'admin' && !profile.isAdmin)) return null;

  return (
    <div className="w-full bg-gray-50 dark:bg-[#020617] text-gray-900 dark:text-gray-200 font-sans relative pb-12">
      {/* Background Ambience */}
      <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-[#0F172A]/5 dark:bg-[#0F172A]/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-[600px] h-[600px] bg-[#EF4444]/5 dark:bg-[#EF4444]/10 rounded-full blur-[150px] pointer-events-none" />
      <SuccessAnimation show={showSuccess} message={successMessage} />
      <Navbar />
      <div className="max-w-[1600px] mx-auto p-4 md:p-8 pt-12 relative z-10 flex flex-col">
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col md:flex-row items-center justify-between gap-6 mb-8"
        >
          <div className="flex items-center gap-4">
            <h1 className="text-3xl font-black text-gray-900 dark:text-white flex items-center gap-3">
              <Crown className="text-[#EF4444]" /> GSE Admin Portal
            </h1>
          </div>

          <div className="flex flex-wrap items-center gap-4">
            <ThemeToggle className="text-gray-900 dark:text-gray-300 mr-2" />
            <div className="bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-white/5 px-4 py-2 rounded-xl flex items-center gap-3 shadow-sm">
              <div className="bg-[#0F172A]/10 dark:bg-[#0F172A]/50 p-1.5 rounded-lg"><Users size={16} className="text-[#0F172A] dark:text-white" /></div>
              <div>
                <div className="text-[10px] uppercase text-gray-600 dark:text-gray-400 font-bold">Total Network</div>
                <div className="text-sm font-bold text-gray-900 dark:text-white">{users.length} Nodes</div>
              </div>
            </div>
            <div className="bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-white/5 px-4 py-2 rounded-xl flex items-center gap-3 shadow-sm">
              <div className="bg-[#0F172A]/10 dark:bg-[#0F172A]/50 p-1.5 rounded-lg"><Activity size={16} className="text-[#0F172A] dark:text-white" /></div>
              <div>
                <div className="text-[10px] uppercase text-gray-600 dark:text-gray-400 font-bold">System Status</div>
                <div className="text-sm font-bold text-[#0F172A] dark:text-white flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#0F172A] animate-pulse" /> Healthy
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {loading ? (
          <div className="flex-1 flex items-center justify-center text-[#EF4444] animate-pulse">Loading visualizer...</div>
        ) : (
          <>
          <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-0">
            {/* Left Column - 3/5 width on large screens */}
            <motion.div 
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="lg:col-span-7 xl:col-span-8 flex flex-col min-h-[600px]"
            >
              <AdminBinaryTree users={users} onManageUser={(u) => {
                setEditingUser(u);
                setEditForm({ firstName: u.firstName || '', lastName: u.lastName || '', email: u.email || '', bankName: u.bankName || '', bankAccountNumber: u.bankAccountNumber || '' });
              }} />
            </motion.div>

            {/* Right Column - 2/5 width */}
            <motion.div 
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="lg:col-span-5 xl:col-span-4 flex flex-col gap-6 h-full"
            >
              <SalesApprovals sales={sales} loading={salesLoading} onProcess={handleProcessSale} />
              <SystemLogs users={users} />
            </motion.div>
          </div>
          
          <SalesTrendChart sales={sales} />
          <SalesHistoryTable sales={sales} onTogglePayout={handleTogglePayout} onDeleteSale={handleDeleteSale} />
          </>
        )}
      </div>
      
      {/* Global styles for custom scrollbar in admin panel */}
      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
          height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(255, 255, 255, 0.02);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(255, 255, 255, 0.2);
        }
      `}</style>      {/* User Details Modal */}
      {isManageModalOpen && focusedUser && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#0F172A] border border-white/20 rounded-3xl p-6 md:p-8 max-w-lg w-full shadow-2xl flex flex-col gap-6 relative animate-in fade-in zoom-in-95 duration-200">
            <div className="flex items-center justify-between border-b border-white/10 pb-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-red-500 to-red-600 flex items-center justify-center font-bold text-white text-xl shadow-lg">
                  {(focusedUser.displayName || focusedUser.name || focusedUser.email || 'U').charAt(0).toUpperCase()}
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">{focusedUser.displayName || focusedUser.name || 'User Profile'}</h3>
                  <p className="text-xs text-gray-400">{focusedUser.email || 'No email registered'}</p>
                </div>
              </div>
              <button 
                onClick={() => setIsManageModalOpen(false)}
                className="text-gray-400 hover:text-white p-2 rounded-xl bg-white/5 hover:bg-white/10 transition-all text-sm"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="bg-white/5 border border-white/10 p-3 rounded-2xl">
                <span className="text-xs text-gray-400 block">Referral Code</span>
                <span className="font-mono font-bold text-red-400">{focusedUser.referralCode || 'N/A'}</span>
              </div>
              <div className="bg-white/5 border border-white/10 p-3 rounded-2xl">
                <span className="text-xs text-gray-400 block">Sponsor ID</span>
                <span className="font-mono font-bold text-white">{focusedUser.sponsorId || 'Root / None'}</span>
              </div>
              <div className="bg-white/5 border border-white/10 p-3 rounded-2xl">
                <span className="text-xs text-gray-400 block">Phone</span>
                <span className="font-bold text-white">{focusedUser.phone || 'Not provided'}</span>
              </div>
              <div className="bg-white/5 border border-white/10 p-3 rounded-2xl">
                <span className="text-xs text-gray-400 block">Role</span>
                <span className="font-bold text-red-400 capitalize">{focusedUser.role || 'Member'}</span>
              </div>
              <div className="bg-white/5 border border-white/10 p-3 rounded-2xl col-span-2">
                <span className="text-xs text-gray-400 block">Bank Account Info</span>
                <span className="font-bold text-white block mt-1">
                  {focusedUser.bankName ? `${focusedUser.bankName} - ${focusedUser.accountNumber} (${focusedUser.accountName})` : 'No banking details saved'}
                </span>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setIsManageModalOpen(false)}
                className="w-full py-3 rounded-xl bg-red-600 hover:bg-red-500 font-bold text-white transition-all shadow-lg text-sm"
              >
                Close Profile
              </button>
            </div>
          </div>
        </div>
      )}      {/* User Details Modal */}
      {inspectModalUser && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-[#0F172A] border border-white/20 rounded-3xl p-6 md:p-8 max-w-lg w-full shadow-2xl flex flex-col gap-6 relative animate-in fade-in zoom-in-95 duration-200 text-left">
            <div className="flex items-center justify-between border-b border-white/10 pb-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-red-500 to-red-600 flex items-center justify-center font-bold text-white text-xl shadow-lg">
                  {(inspectModalUser.displayName || inspectModalUser.name || inspectModalUser.email || 'U').charAt(0).toUpperCase()}
                </div>
                <div>
                  <h3 className="text-xl font-bold text-white">{inspectModalUser.displayName || inspectModalUser.name || 'User Profile'}</h3>
                  <p className="text-xs text-gray-400">{inspectModalUser.email || 'No email registered'}</p>
                </div>
              </div>
              <button 
                onClick={() => setInspectModalUser(null)}
                className="text-gray-400 hover:text-white p-2 rounded-xl bg-white/5 hover:bg-white/10 transition-all text-sm font-bold"
              >
                ✕
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="bg-white/5 border border-white/10 p-3.5 rounded-2xl">
                <span className="text-xs text-gray-400 block mb-1">Referral Code</span>
                <span className="font-mono font-bold text-red-400">{inspectModalUser.referralCode || 'N/A'}</span>
              </div>
              <div className="bg-white/5 border border-white/10 p-3.5 rounded-2xl">
                <span className="text-xs text-gray-400 block mb-1">Sponsor Code</span>
                <span className="font-mono font-bold text-white">{inspectModalUser.sponsorId || 'Root / Direct'}</span>
              </div>
              <div className="bg-white/5 border border-white/10 p-3.5 rounded-2xl">
                <span className="text-xs text-gray-400 block mb-1">Phone Number</span>
                <span className="font-bold text-white">{inspectModalUser.phone || inspectModalUser.phoneNumber || 'Not provided'}</span>
              </div>
              <div className="bg-white/5 border border-white/10 p-3.5 rounded-2xl">
                <span className="text-xs text-gray-400 block mb-1">Account Role</span>
                <span className="font-bold text-red-400 capitalize">{inspectModalUser.role || 'Member'}</span>
              </div>
              <div className="bg-white/5 border border-white/10 p-3.5 rounded-2xl col-span-2">
                <span className="text-xs text-gray-400 block mb-1">Bank Payout Info</span>
                <span className="font-bold text-white block mt-0.5">
                  {inspectModalUser.bankName ? `${inspectModalUser.bankName} - ${inspectModalUser.accountNumber} (${inspectModalUser.accountName})` : 'No banking details submitted'}
                </span>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setInspectModalUser(null)}
                className="w-full py-3 rounded-xl bg-red-600 hover:bg-red-500 font-bold text-white transition-all shadow-lg text-sm"
              >
                Close Profile
              </button>
            </div>
          </div>
        </div>
      )}


          {modalUser && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#0F172A] border border-white/20 rounded-3xl p-6 max-w-lg w-full shadow-2xl flex flex-col gap-5 text-left text-white">
            <div className="flex items-center justify-between border-b border-white/10 pb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-red-600 flex items-center justify-center font-bold text-white text-lg">
                  {(modalUser.displayName || modalUser.name || 'U').charAt(0).toUpperCase()}
                </div>
                <div>
                  <h3 className="font-bold text-lg">{modalUser.displayName || modalUser.name || 'User Profile'}</h3>
                  <p className="text-xs text-gray-400">{modalUser.email || 'No email registered'}</p>
                </div>
              </div>
              <button onClick={() => setModalUser(null)} className="text-gray-400 hover:text-white text-sm font-bold">✕</button>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="bg-white/5 p-3 rounded-xl border border-white/10">
                <span className="text-gray-400 block text-[10px]">REFERRAL CODE</span>
                <span className="font-mono font-bold text-red-400 text-sm">{modalUser.referralCode || 'N/A'}</span>
              </div>
              <div className="bg-white/5 p-3 rounded-xl border border-white/10">
                <span className="text-gray-400 block text-[10px]">SPONSOR CODE</span>
                <span className="font-mono font-bold text-white text-sm">{modalUser.sponsorId || 'Direct'}</span>
              </div>
              <div className="bg-white/5 p-3 rounded-xl border border-white/10 col-span-2">
                <span className="text-gray-400 block text-[10px]">BANK DETAILS</span>
                <span className="font-bold text-white block mt-0.5">
                  {modalUser.bankName ? `${modalUser.bankName} - ${modalUser.accountNumber} (${modalUser.accountName})` : 'No banking details saved'}
                </span>
              </div>
            </div>

            <button onClick={() => setModalUser(null)} className="w-full py-2.5 rounded-xl bg-red-600 font-bold text-xs hover:bg-red-500 transition-all">
              Close Profile
            </button>
          </div>
        </div>
      )}</div>

  );
}





















