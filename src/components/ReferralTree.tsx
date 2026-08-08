import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { ChevronRight, ChevronDown, User, Crown, Network, Search } from 'lucide-react';
import { UserProfile } from '../contexts/AuthContext';

type UserNode = UserProfile & { 
  id: string; 
  children: UserNode[];
  depth: number;
};

interface ReferralTreeProps {
  users: (UserProfile & { id: string })[];
  rootUserId?: string; // Optional: If provided, tree starts from this user
  isAdminView?: boolean;
}

export function ReferralTree({ users, rootUserId, isAdminView = false }: ReferralTreeProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [focusedUserId, setFocusedUserId] = useState<string | null>(rootUserId || null);
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set());

  const toggleNode = (nodeId: string) => {
    setExpandedNodes(prev => {
      const next = new Set(prev);
      if (next.has(nodeId)) {
        next.delete(nodeId);
      } else {
        next.add(nodeId);
      }
      return next;
    });
  };

  // Build the tree
  const treeData = useMemo(() => {
    const nodeMap = new Map<string, UserNode>();
    const roots: UserNode[] = [];

    // Initialize all nodes
    users.forEach(u => {
      const node = { ...u, children: [], depth: 0 };
      nodeMap.set(u.id, node);
      if (u.referralCode) {
        nodeMap.set(u.referralCode, node); // Support lookup by ref code too, pointing to same reference
      }
    });

    users.forEach(u => {
      const node = nodeMap.get(u.id)!;
      const parentId = u.sponsorId;
      
            const parentNode = nodeMap.get(parentId) || Array.from(nodeMap.values()).find((n: any) => n.referralCode === parentId || n.email === parentId);
      if (parentId && parentId !== 'admin') {
        parentNode = nodeMap.get(parentId);
      }

      if (parentNode) {
        parentNode.children.push(node);
      } else {
        roots.push(node);
      }
    });

    // Helper to calculate depth
    const calculateDepth = (node: UserNode, currentDepth: number) => {
      node.depth = currentDepth;
      node.children.forEach(child => calculateDepth(child, currentDepth + 1));
    };

    roots.forEach(root => calculateDepth(root, 0));

    return { roots, nodeMap };
  }, [users]);

  // Find the focused root
  const displayRoots = useMemo(() => {
    if (focusedUserId) {
      const focusedNode = treeData.nodeMap.get(focusedUserId);
      if (focusedNode) {
        // Reset depth relative to this root for display?
        // Let's just return it as the root
        return [focusedNode];
      }
    }
    // Default to admin or top-level roots
    const adminRoot = users.find(u => u.role === 'admin' || u.isAdmin);
    if (adminRoot && !focusedUserId) {
      const rootNode = treeData.nodeMap.get(adminRoot.id);
      if (rootNode) return [rootNode];
    }
    return treeData.roots;
  }, [treeData, focusedUserId, users]);

  // Expand default roots
  React.useEffect(() => {
    const initialExpanded = new Set<string>();
    displayRoots.forEach(r => initialExpanded.add(r.id));
    setExpandedNodes(initialExpanded);
  }, [displayRoots]);

  const filteredUsers = useMemo(() => {
    if (!searchTerm) return [];
    return users.filter(u => 
      u.displayName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      u.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      u.referralCode.toLowerCase().includes(searchTerm.toLowerCase())
    ).slice(0, 5);
  }, [users, searchTerm]);

  return (
    <div className="bg-white dark:bg-[#1E293B] rounded-3xl shadow-lg border border-gray-100 dark:border-white/10 overflow-hidden relative">
      {/* Header and Controls */}
      <div className="p-6 md:p-8 border-b border-gray-100 dark:border-white/10 bg-gradient-to-r from-gray-50 to-white dark:from-[#1E293B] dark:to-[#1E293B] relative z-10">
        <div className="flex flex-col md:flex-row gap-4 justify-between items-start md:items-center">
          <div className="flex items-center gap-3">
            <Network className="text-[#0F172A] dark:text-white" size={24} />
            <h3 className="text-xl font-bold text-gray-900 dark:text-white">
              Visual Referral Tree
            </h3>
          </div>

          {isAdminView && (
            <div className="relative w-full md:w-72">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Focus on specific user..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 rounded-xl bg-white dark:bg-[#0F172A] border border-gray-200 dark:border-white/10 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#0F172A]/20 dark:focus:ring-white/20 transition-all text-sm"
                />
                <Search size={16} className="absolute left-3 top-2.5 text-gray-500 dark:text-gray-400" />
              </div>
              
              <AnimatePresence>
                {searchTerm && filteredUsers.length > 0 && (
                  <motion.div 
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 5 }}
                    className="absolute z-10 w-full mt-2 bg-white dark:bg-[#1E293B] rounded-xl shadow-lg border border-gray-100 dark:border-white/10 overflow-hidden"
                  >
                    {filteredUsers.map(u => (
                      <button
                        key={u.id}
                        onClick={() => {
                          setFocusedUserId(u.id);
                          setSearchTerm('');
                        }}
                        className="w-full text-left px-4 py-3 hover:bg-gray-50 dark:bg-white/5 transition-colors flex flex-col border-b border-gray-50 last:border-0"
                      >
                        <span className="font-semibold text-gray-900 dark:text-white text-sm">{u.displayName}</span>
                        <span className="text-xs text-gray-600 dark:text-gray-400 dark:text-gray-400">{u.email}</span>
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          )}
        </div>
        
        {focusedUserId && isAdminView && (
          <div className="mt-4 flex items-center gap-2">
            <span className="text-sm text-gray-600 dark:text-gray-400 dark:text-gray-400">Currently focused on:</span>
            <span className="text-sm font-semibold text-[#0F172A] dark:text-white bg-gray-100 dark:bg-[#0F172A] px-2 py-1 rounded">
              {treeData.nodeMap.get(focusedUserId)?.displayName || 'Unknown User'}
            </span>
            <button 
              onClick={() => setFocusedUserId(null)}
              className="text-xs text-gray-600 dark:text-gray-400 dark:text-gray-400 hover:text-[#EF4444] transition-colors underline ml-2"
            >
              Reset to Root
            </button>
          </div>
        )}
      </div>

      {/* Tree View */}
      <div className="p-6 overflow-x-auto">
        <div className="min-w-[600px]">
          {displayRoots.length === 0 ? (
            <div className="text-center py-10 text-gray-500 dark:text-gray-400 dark:text-gray-600 dark:text-gray-400">
              No network data found.
            </div>
          ) : (
            displayRoots.map(root => (
              <TreeNode 
                key={root.id} 
                node={root} 
                expandedNodes={expandedNodes}
                toggleNode={toggleNode}
                level={0}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
}

const TreeNode: React.FC<{ 
  node: UserNode; 
  expandedNodes: Set<string>;
  toggleNode: (id: string) => void;
  level: number;
}> = ({ 
  node, 
  expandedNodes, 
  toggleNode, 
  level 
}) => {
  const isExpanded = expandedNodes.has(node.id);
  const hasChildren = node.children && node.children.length > 0;
  
  // Calculate total network size recursively for this node (optional, if we want to show it)
  const calculateTotalNetwork = (n: UserNode): number => {
    let size = n.children.length;
    n.children.forEach(c => size += calculateTotalNetwork(c));
    return size;
  };
  
  const totalNetwork = calculateTotalNetwork(node);

  return (
    <div className="select-none flex flex-col">
      <div 
        className={`flex items-center py-2 ${level > 0 ? 'mt-2' : ''}`}
        style={{ paddingLeft: `${level * 2}rem` }}
      >
        {/* Connection Lines (Simplified for now with just spacing, but we can add border-l lines if needed) */}
        <div className="relative flex items-center flex-1">
          {/* Expand/Collapse Button */}
          <div 
            className={`w-6 h-6 flex items-center justify-center mr-2 rounded cursor-pointer transition-colors ${hasChildren ? 'hover:bg-gray-100 text-gray-600 dark:text-gray-400 dark:text-gray-400' : 'text-transparent'}`}
            onClick={() => hasChildren && toggleNode(node.id)}
          >
            {hasChildren && (
              isExpanded ? <ChevronDown size={18} /> : <ChevronRight size={18} />
            )}
          </div>
          
          {/* Node Card */}
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.3 }} className="flex-1 bg-white dark:bg-[#1E293B] border border-gray-100 dark:border-white/10 rounded-2xl p-4 flex items-center gap-4 shadow-sm hover:shadow-md transition-all hover:-translate-y-0.5 relative overflow-hidden group">
            {/* Status indicator line */}
            <div className={`absolute left-0 top-0 bottom-0 w-1 ${node.isAdmin || node.role === 'admin' ? 'bg-[#EF4444]' : 'bg-[#0F172A]'}`} />
            
            <div className={`h-10 w-10 rounded-full flex-shrink-0 flex items-center justify-center font-bold text-sm overflow-hidden ${node.isAdmin || node.role === 'admin' ? 'bg-[#EF4444]/10 text-[#EF4444]' : 'bg-gray-100 dark:bg-[#0F172A] text-[#0F172A] dark:text-white'}`}>
              {(node.profileImage || node.avatarUrl) ? (
                <img src={node.profileImage || node.avatarUrl} alt="Avatar" className="w-full h-full object-cover" />
              ) : (node.isAdmin || node.role === 'admin') ? (
                <Crown size={18} />
              ) : (
                node.displayName?.charAt(0).toUpperCase() || 'U'
              )}
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <h4 className="font-bold text-gray-900 dark:text-white truncate">{node.displayName}</h4>
                {node.isAdmin || node.role === 'admin' ? (
                  <span className="text-[10px] uppercase tracking-widest font-bold bg-[#EF4444]/10 text-[#EF4444] px-2.5 py-1 rounded-full">Admin</span>
                ) : null}
              </div>
              <p className="text-xs text-gray-600 dark:text-gray-400 dark:text-gray-400 truncate">{node.email}</p>
            </div>
            
            <div className="hidden sm:flex items-center gap-6 pr-4">
              <div className="flex flex-col items-end">
                <span className="text-[10px] uppercase font-bold text-gray-500 dark:text-gray-400 dark:text-gray-600 dark:text-gray-400">Ref Code</span>
                <span className="text-xs font-mono font-medium text-[#EF4444] bg-[#EF4444]/5 px-2 py-0.5 rounded border border-[#EF4444]/20">
                  {node.referralCode}
                </span>
              </div>
              
              <div className="flex flex-col items-end">
                <span className="text-[10px] uppercase font-bold text-gray-500 dark:text-gray-400 dark:text-gray-600 dark:text-gray-400">Direct</span>
                <span className="text-sm font-bold text-gray-700 dark:text-gray-200">
                  {node.children.length}
                </span>
              </div>
              
              <div className="flex flex-col items-end">
                <span className="text-[10px] uppercase font-bold text-gray-500 dark:text-gray-400 dark:text-gray-600 dark:text-gray-400">Network</span>
                <span className="text-sm font-bold text-gray-700 dark:text-gray-200">
                  {totalNetwork}
                </span>
              </div>
              
              <div className="flex flex-col items-end">
                <span className="text-[10px] uppercase font-bold text-gray-500 dark:text-gray-400 dark:text-gray-600 dark:text-gray-400">Level</span>
                <span className="text-sm font-bold text-gray-700 dark:text-gray-200">
                  {level}
                </span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      <AnimatePresence>
        {isExpanded && hasChildren && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden"
          >
            <div className="relative">
              {/* Vertical line connecting children */}
              <div 
                className="absolute left-[calc(1.5rem-1px)] top-0 bottom-6 w-px bg-gradient-to-b from-gray-200 dark:from-white/20 to-transparent" 
                style={{ left: `calc(${level * 2}rem + 1.5rem - 1px)` }}
              />
              {node.children.map(child => (
                <TreeNode 
                  key={child.id} 
                  node={child} 
                  expandedNodes={expandedNodes}
                  toggleNode={toggleNode}
                  level={level + 1}
                />
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

