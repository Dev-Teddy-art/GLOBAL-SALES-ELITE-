with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

# We'll just create a new file content
new_content = """import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, UserProfile } from '../contexts/AuthContext';
import { sanityClient } from '../lib/sanity';
import { motion, AnimatePresence } from 'motion/react';
import { Shield, ChevronLeft, ChevronDown, ChevronRight, CheckCircle, DollarSign, Activity, Users, Search, AlertCircle, LayoutDashboard, Database, Link as LinkIcon, Network } from 'lucide-react';

// Specialized Admin Binary Tree Component
function AdminBinaryTree({ users }: { users: (UserProfile & { id: string })[] }) {
  const [searchTerm, setSearchTerm] = useState('');
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
        const parent = map.get(u.sponsorId);
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
      u.displayName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      u.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      u.referralCode.toLowerCase().includes(searchTerm.toLowerCase())
    ).slice(0, 5);
  }, [users, searchTerm]);

  return (
    <div className="bg-[#0F172A]/80 backdrop-blur-xl border border-white/10 rounded-3xl p-6 h-[800px] flex flex-col relative overflow-hidden">
      {/* Background Orbs */}
      <div className="absolute top-0 right-0 -mt-20 -mr-20 w-72 h-72 bg-[#1E3A8A] opacity-20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-64 h-64 bg-[#EF4444] opacity-10 rounded-full blur-3xl pointer-events-none" />
      
      {/* Search Header */}
      <div className="relative z-20 flex flex-col sm:flex-row items-center justify-between gap-4 mb-6">
        <h3 className="text-xl font-bold text-white flex items-center gap-3">
          <Network className="text-[#EF4444]" />
          Visual Binary Inspector
        </h3>
        
        <div className="relative w-full sm:w-72">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-4 w-4 text-gray-400" />
          </div>
          <input
            type="text"
            placeholder="Search by name, email, or code..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="w-full bg-[#1E293B]/80 border border-white/10 rounded-xl pl-10 pr-4 py-2.5 text-sm text-white placeholder-gray-400 focus:outline-none focus:border-[#EF4444] transition-colors"
          />
          
          {/* Search Dropdown */}
          <AnimatePresence>
            {searchTerm && filteredUsers.length > 0 && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
                className="absolute top-full left-0 right-0 mt-2 bg-[#1E293B] border border-white/10 rounded-xl shadow-2xl overflow-hidden z-50"
              >
                {filteredUsers.map(u => (
                  <button
                    key={u.id}
                    onClick={() => {
                      setFocusedId(u.id);
                      setSearchTerm('');
                    }}
                    className="w-full text-left px-4 py-3 hover:bg-white/5 transition-colors border-b border-white/5 last:border-0"
                  >
                    <div className="font-semibold text-white text-sm">{u.displayName}</div>
                    <div className="text-xs text-gray-400 font-mono">{u.referralCode}</div>
                  </button>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {focusedId && (
        <div className="mb-4 flex items-center gap-3 bg-[#EF4444]/10 border border-[#EF4444]/20 p-3 rounded-xl relative z-20 w-max">
          <span className="text-sm text-[#EF4444]">Focused: <strong>{nodeMap.get(focusedId)?.displayName}</strong></span>
          <button 
            onClick={() => setFocusedId(null)}
            className="text-xs bg-[#EF4444] text-white px-2 py-1 rounded hover:bg-red-600 transition-colors"
          >
            Reset
          </button>
        </div>
      )}

      {/* Tree Canvas */}
      <div className="flex-1 overflow-auto relative z-10 custom-scrollbar pr-2 pb-10">
        <div className="min-w-[600px] flex flex-col items-center pt-8">
          {displayRoot.length === 0 ? (
            <div className="text-gray-500 mt-20">No network data.</div>
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

function AdminTreeNode({ node, level }: { node: any, level: number }) {
  const [expanded, setExpanded] = useState(true);
  const hasChildren = node.children && node.children.length > 0;

  return (
    <div className="flex flex-col items-center">
      {/* Node Card */}
      <motion.div 
        whileHover={{ scale: 1.05 }}
        className={`relative z-10 w-64 bg-[#1E293B] border border-white/10 rounded-2xl p-4 shadow-xl flex flex-col items-center gap-2 cursor-pointer transition-colors ${expanded ? 'border-white/20' : ''}`}
        onClick={() => hasChildren && setExpanded(!expanded)}
      >
        <div className={`absolute top-0 right-0 w-2 h-2 rounded-full m-3 ${node.isAdmin || node.role === 'admin' ? 'bg-amber-400' : 'bg-emerald-400'} shadow-[0_0_8px_rgba(52,211,153,0.8)]`} />
        
        <div className="h-12 w-12 rounded-full bg-gradient-to-br from-[#1E3A8A] to-[#0F172A] flex items-center justify-center font-bold text-lg text-white shadow-inner border border-white/10">
          {node.displayName.charAt(0).toUpperCase()}
        </div>
        <div className="text-center">
          <h4 className="font-bold text-white text-sm truncate w-56">{node.displayName}</h4>
          <span className="text-[10px] font-mono text-[#EF4444] bg-[#EF4444]/10 px-2 py-0.5 rounded mt-1 inline-block border border-[#EF4444]/20">
            {node.referralCode}
          </span>
        </div>

        {/* L / R Slots Indicators */}
        <div className="flex gap-2 w-full mt-2 pt-2 border-t border-white/5">
          <div className={`flex-1 text-center py-1 rounded text-xs font-bold ${node.left ? 'bg-blue-900/40 text-blue-300' : 'bg-gray-800/50 text-gray-500 border border-dashed border-gray-700'}`}>
            {node.left ? 'L' : 'L (Open)'}
          </div>
          <div className={`flex-1 text-center py-1 rounded text-xs font-bold ${node.right ? 'bg-red-900/40 text-red-300' : 'bg-gray-800/50 text-gray-500 border border-dashed border-gray-700'}`}>
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

function PayoutApprovals({ users }: { users: any[] }) {
  const usersWithBank = users.filter(u => u.role !== 'admin' && u.bankAccountNumber);
  
  return (
    <div className="bg-[#0F172A]/80 backdrop-blur-xl border border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col h-[380px]">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <DollarSign className="text-emerald-400" size={20} />
          Pending Payouts
        </h3>
        <span className="bg-[#EF4444] text-white text-xs font-bold px-2.5 py-1 rounded-full">{usersWithBank.length}</span>
      </div>
      
      <div className="flex-1 overflow-auto custom-scrollbar pr-2 space-y-3">
        {usersWithBank.length === 0 ? (
          <div className="text-gray-500 text-center py-10 text-sm">No pending payouts.</div>
        ) : (
          usersWithBank.map((u, i) => (
            <motion.div 
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1 }}
              key={u.id}
              className="bg-[#1E293B] border border-white/5 rounded-xl p-4 hover:border-white/20 transition-colors"
            >
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h4 className="font-bold text-white text-sm">{u.displayName}</h4>
                  <p className="text-xs text-gray-400">{u.bankName}</p>
                </div>
                <button className="bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500 hover:text-white transition-colors p-1.5 rounded-lg">
                  <CheckCircle size={16} />
                </button>
              </div>
              <div className="text-xs font-mono text-gray-300 bg-black/20 p-2 rounded flex justify-between items-center">
                <span>{u.bankAccountNumber}</span>
                <span className="text-[#EF4444] font-bold">₦---</span>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </div>
  );
}

function SystemLogs() {
  const logs = [
    { id: 1, msg: "New user registration: Michael O.", time: "2 min ago", type: 'info' },
    { id: 2, msg: "Spillover triggered for node REF-X92", time: "15 min ago", type: 'warning' },
    { id: 3, msg: "Payout batch #42 approved", time: "1 hour ago", type: 'success' },
    { id: 4, msg: "Nested sets boundary recalibrated", time: "3 hours ago", type: 'info' },
  ];

  return (
    <div className="bg-[#0F172A]/80 backdrop-blur-xl border border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col h-[396px]">
      <h3 className="text-lg font-bold text-white flex items-center gap-2 mb-4">
        <Activity className="text-blue-400" size={20} />
        System Logs
      </h3>
      
      <div className="flex-1 overflow-auto custom-scrollbar pr-2 space-y-4">
        {logs.map((log, i) => (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 + 0.3 }}
            key={log.id} 
            className="flex gap-3 items-start"
          >
            <div className={`mt-0.5 w-2 h-2 rounded-full flex-shrink-0 ${log.type === 'info' ? 'bg-blue-400' : log.type === 'warning' ? 'bg-amber-400' : 'bg-emerald-400'}`} />
            <div>
              <p className="text-sm text-gray-300 leading-tight">{log.msg}</p>
              <span className="text-xs text-gray-500">{log.time}</span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

export function AdminConsolePage() {
  const { profile } = useAuth();
  const navigate = useNavigate();
  const [users, setUsers] = useState<(UserProfile & { id: string })[]>([]);
  const [loading, setLoading] = useState(true);

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
    fetchUsers();
  }, []);

  if (!profile || (profile.role !== 'admin' && !profile.isAdmin)) return null;

  return (
    <div className="min-h-screen bg-[#020617] text-gray-200 font-sans relative overflow-hidden">
      {/* Background Ambience */}
      <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-[#1E3A8A]/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-[600px] h-[600px] bg-[#EF4444]/10 rounded-full blur-[150px] pointer-events-none" />

      <div className="max-w-[1600px] mx-auto p-4 md:p-8 relative z-10 h-screen flex flex-col">
        {/* Top Header */}
        <motion.header 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col md:flex-row items-center justify-between gap-6 mb-8 bg-[#0F172A]/50 backdrop-blur-md border border-white/5 p-4 rounded-3xl"
        >
          <div className="flex items-center gap-4">
            <button 
              onClick={() => navigate('/dashboard')} 
              className="h-10 w-10 bg-white/5 hover:bg-white/10 rounded-full flex items-center justify-center transition-colors"
            >
              <ChevronLeft size={20} className="text-gray-300" />
            </button>
            <div>
              <h1 className="text-2xl font-black text-white flex items-center gap-2">
                <Shield className="text-[#EF4444]" /> GSE Admin Portal
              </h1>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-4">
            <div className="bg-[#1E293B] border border-white/5 px-4 py-2 rounded-xl flex items-center gap-3">
              <div className="bg-blue-500/20 p-1.5 rounded-lg"><Users size={16} className="text-blue-400" /></div>
              <div>
                <div className="text-[10px] uppercase text-gray-500 font-bold">Total Network</div>
                <div className="text-sm font-bold text-white">{users.length} Nodes</div>
              </div>
            </div>
            <div className="bg-[#1E293B] border border-white/5 px-4 py-2 rounded-xl flex items-center gap-3">
              <div className="bg-emerald-500/20 p-1.5 rounded-lg"><Activity size={16} className="text-emerald-400" /></div>
              <div>
                <div className="text-[10px] uppercase text-gray-500 font-bold">System Status</div>
                <div className="text-sm font-bold text-emerald-400 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" /> Healthy
                </div>
              </div>
            </div>
          </div>
        </motion.header>

        {loading ? (
          <div className="flex-1 flex items-center justify-center text-[#EF4444] animate-pulse">Loading visualizer...</div>
        ) : (
          <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-0">
            {/* Left Column - 3/5 width on large screens */}
            <motion.div 
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="lg:col-span-7 xl:col-span-8 flex flex-col min-h-[600px]"
            >
              <AdminBinaryTree users={users} />
            </motion.div>

            {/* Right Column - 2/5 width */}
            <motion.div 
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="lg:col-span-5 xl:col-span-4 flex flex-col gap-6 h-full"
            >
              <PayoutApprovals users={users} />
              <SystemLogs />
            </motion.div>
          </div>
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
      `}</style>
    </div>
  );
}
"""

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(new_content)
