import React, { useState, useMemo } from 'react';
import { Network, Search, User, ChevronRight, ChevronDown, Shield, Trash2, CheckCircle, RefreshCw } from 'lucide-react';
import { sanityClient } from '../lib/sanity';

export function AdminConsolePage({ users = [], sales = [], profile, setSales }: any) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedUser, setSelectedUser] = useState<any>(null);
  const [showSuccess, setShowSuccess] = useState(false);

  // 1. Safe search filter across all user fields (Prevents blank screen crashes)
  const safeUsers = useMemo(() => Array.isArray(users) ? users : [], [users]);

  // 2. Build Tree Structure matching sponsorId to _id, referralCode, or email
  const { nodeMap, rootNode } = useMemo(() => {
    const map = new Map<string, any>();

    safeUsers.forEach((u: any) => {
      const id = u._id || u.id;
      if (!id) return;
      map.set(id, {
        ...u,
        id,
        children: [],
      });
    });

    let root: any = null;

    map.forEach((node) => {
      const pId = node.sponsorId;
      let parent = pId ? (map.get(pId) || Array.from(map.values()).find((n: any) => n.referralCode === pId || n.email === pId)) : null;

      if (parent && parent.id !== node.id) {
        parent.children.push(node);
      } else if (!root || node.referralCode === 'CSX5A3' || node.role === 'admin') {
        root = node;
      }
    });

    // Fallback unlinked nodes directly under root
    if (root) {
      map.forEach((node) => {
        if (node.id !== root.id && !node.sponsorId) {
          if (!root.children.includes(node)) root.children.push(node);
        }
      });
    }

    return { nodeMap: map, rootNode: root };
  }, [safeUsers]);

  // 3. Search target resolution
  const displayRoot = useMemo(() => {
    if (!searchTerm.trim()) return rootNode;
    const term = searchTerm.toLowerCase().trim();
    const found = Array.from(nodeMap.values()).find((u: any) => {
      const name = (u.displayName || u.name || '').toLowerCase();
      const email = (u.email || '').toLowerCase();
      const code = (u.referralCode || '').toLowerCase();
      return name.includes(term) || email.includes(term) || code.includes(term);
    });
    return found || rootNode;
  }, [searchTerm, nodeMap, rootNode]);

  // Delete sale handler
  const handleDeleteSale = async (saleId: string) => {
    try {
      await sanityClient.delete(saleId);
      if (typeof setSales === 'function') {
        setSales((prev: any[]) => prev.filter((s: any) => (s._id || s.id) !== saleId));
      }
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 2500);
    } catch (err) {
      console.error("Failed to delete sale:", err);
    }
  };

  // 4. Recursive Binary Tree Renderer (L / R Slots)
  const renderBinaryNode = (node: any, depth = 0): React.ReactNode => {
    if (!node || depth > 3) return null;
    const leftChild = node.children && node.children[0];
    const rightChild = node.children && node.children[1];
    const name = node.displayName || node.name || node.email?.split('@')[0] || 'User';

    return (
      <div className="flex flex-col items-center gap-4 my-2">
        <div className="relative bg-white/5 border border-white/10 p-4 rounded-2xl flex flex-col items-center min-w-[220px] shadow-xl">
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-red-500 to-red-600 flex items-center justify-center font-bold text-white mb-2 text-lg shadow-md">
            {name.charAt(0).toUpperCase()}
          </div>
          <span className="font-bold text-white text-sm text-center">{name}</span>
          <span className="text-[11px] text-red-400 font-mono bg-red-500/10 px-2 py-0.5 rounded border border-red-500/20 mt-1">
            {node.referralCode || 'NO_REF'}
          </span>
          <div className="flex gap-3 text-[10px] text-gray-400 mt-2">
            <span>Direct: <strong className="text-white">{node.children?.length || 0}</strong></span>
          </div>
        </div>

        <div className="flex items-start gap-8 border-t border-white/10 pt-4">
          <div className="flex flex-col items-center">
            <span className="text-[10px] text-gray-400 font-bold mb-1">L (Left)</span>
            {leftChild ? renderBinaryNode(leftChild, depth + 1) : (
              <div className="border border-dashed border-white/20 px-4 py-2 rounded-xl text-gray-500 text-xs bg-white/5">
                L (Open)
              </div>
            )}
          </div>
          <div className="flex flex-col items-center">
            <span className="text-[10px] text-gray-400 font-bold mb-1">R (Right)</span>
            {rightChild ? renderBinaryNode(rightChild, depth + 1) : (
              <div className="border border-dashed border-white/20 px-4 py-2 rounded-xl text-gray-500 text-xs bg-white/5">
                R (Open)
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col gap-8 p-6 bg-[#0B1120] min-h-screen text-white">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-6">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <Shield className="text-red-500" /> GSE Admin Portal
          </h1>
          <p className="text-sm text-gray-400">System overview, tree hierarchy, and user network management</p>
        </div>

        <div className="relative w-full md:w-80">
          <input
            type="text"
            placeholder="Search user name, email, or ref code..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 text-sm"
          />
          <Search size={16} className="absolute left-3 top-3.5 text-gray-400" />
        </div>
      </div>

      {showSuccess && (
        <div className="p-4 rounded-xl bg-green-500/20 border border-green-500/30 text-green-400 text-sm">
          Action completed successfully!
        </div>
      )}

      {/* Visual Binary Inspector Board */}
      <div className="bg-white/5 border border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col items-center overflow-x-auto">
        <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2 self-start">
          <Network className="text-red-500" size={20} /> Visual Binary Inspector
        </h2>
        
        {displayRoot ? (
          renderBinaryNode(displayRoot)
        ) : (
          <div className="text-gray-400 text-sm py-12">No network structure available.</div>
        )}
      </div>
    </div>
  );
}
