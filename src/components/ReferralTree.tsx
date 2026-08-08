import React, { useState, useMemo } from 'react';
import { Network, Search, User, ChevronRight, ChevronDown, Shield } from 'lucide-react';

interface TreeNode {
  id: string;
  _id?: string;
  displayName?: string;
  name?: string;
  email?: string;
  referralCode?: string;
  sponsorId?: string;
  role?: string;
  children: TreeNode[];
  directCount: number;
  networkCount: number;
}

export function ReferralTree({ users = [], currentUserId, isAdminView = false }: { users: any[], currentUserId?: string, isAdminView?: boolean }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedNodes, setExpandedNodes] = useState<Record<string, boolean>>({});

  // 1. Process users into hierarchical map with robust fallback matching
  const { rootNodes, allNodesMap } = useMemo(() => {
    if (!Array.isArray(users) || users.length === 0) {
      return { rootNodes: [], allNodesMap: new Map<string, TreeNode>() };
    }

    const nodeMap = new Map<string, TreeNode>();

    // Initialize clean node structures
    users.forEach((u: any) => {
      const id = u._id || u.id;
      if (!id) return;
      nodeMap.set(id, {
        ...u,
        id,
        children: [],
        directCount: 0,
        networkCount: 0
      });
    });

    const rootList: TreeNode[] = [];

    // Build hierarchy
    nodeMap.forEach((node) => {
      const parentId = node.sponsorId;
      
      // Look up parent by _id, referralCode, or email
      let parentNode: TreeNode | undefined = undefined;
      if (parentId && parentId !== 'admin') {
        parentNode = nodeMap.get(parentId) || Array.from(nodeMap.values()).find(
          (n) => n.referralCode === parentId || n.email === parentId || n._id === parentId
        );
      }

      if (parentNode && parentNode.id !== node.id) {
        parentNode.children.push(node);
      } else {
        rootList.push(node);
      }
    });

    // 2. Compute Direct & Total Network Counts recursively
    const computeCounts = (n: TreeNode): number => {
      n.directCount = n.children.length;
      let total = n.children.length;
      n.children.forEach(child => {
        total += computeCounts(child);
      });
      n.networkCount = total;
      return total;
    };

    rootList.forEach(computeCounts);

    return { rootNodes: rootList, allNodesMap: nodeMap };
  }, [users]);

  const toggleExpand = (id: string) => {
    setExpandedNodes(prev => ({ ...prev, [id]: !prev[id] }));
  };

  // 3. Safe Search Filter (Prevents blank-screen crash on missing properties)
  const filteredRoots = useMemo(() => {
    if (!searchTerm.trim()) return rootNodes;

    const term = searchTerm.toLowerCase().trim();
    
    // Find matching target node safely
    const targetNode = Array.from(allNodesMap.values()).find(n => {
      const name = (n.displayName || n.name || '').toLowerCase();
      const email = (n.email || '').toLowerCase();
      const ref = (n.referralCode || '').toLowerCase();
      return name.includes(term) || email.includes(term) || ref.includes(term);
    });

    return targetNode ? [targetNode] : [];
  }, [searchTerm, rootNodes, allNodesMap]);

  const renderNode = (node: TreeNode, depth = 0) => {
    const isExpanded = expandedNodes[node.id] ?? true;
    const hasChildren = node.children.length > 0;
    const displayName = node.displayName || node.name || node.email?.split('@')[0] || 'User';

    return (
      <div key={node.id} className="flex flex-col gap-2 my-1" style={{ marginLeft: `${depth * 18}px` }}>
        <div className="flex items-center justify-between p-4 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all">
          <div className="flex items-center gap-3">
            {hasChildren ? (
              <button onClick={() => toggleExpand(node.id)} className="p-1 rounded-lg hover:bg-white/10 text-gray-400">
                {isExpanded ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
              </button>
            ) : (
              <div className="w-6" />
            )}
            
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#EF4444] to-red-600 flex items-center justify-center font-bold text-white shadow-lg">
              {displayName.charAt(0).toUpperCase()}
            </div>

            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-white text-sm">{displayName}</span>
                {node.role === 'admin' && (
                  <span className="px-2 py-0.5 rounded-md bg-[#EF4444]/20 border border-[#EF4444]/30 text-[#EF4444] text-[10px] font-bold">ADMIN</span>
                )}
              </div>
              <p className="text-xs text-gray-400">{node.email || 'No email provided'}</p>
            </div>
          </div>

          <div className="flex items-center gap-4 text-xs">
            <div className="text-center px-3 py-1 rounded-lg bg-white/5 border border-white/5">
              <span className="text-gray-400 block text-[10px]">REF CODE</span>
              <span className="font-mono font-bold text-red-400">{node.referralCode || 'N/A'}</span>
            </div>
            <div className="text-center px-3 py-1 rounded-lg bg-white/5 border border-white/5">
              <span className="text-gray-400 block text-[10px]">DIRECT</span>
              <span className="font-bold text-white">{node.directCount}</span>
            </div>
            <div className="text-center px-3 py-1 rounded-lg bg-white/5 border border-white/5">
              <span className="text-gray-400 block text-[10px]">NETWORK</span>
              <span className="font-bold text-white">{node.networkCount}</span>
            </div>
          </div>
        </div>

        {hasChildren && isExpanded && (
          <div className="flex flex-col gap-1 border-l-2 border-white/10 pl-2">
            {node.children.map(child => renderNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="bg-[#0B1120] border border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col gap-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-4">
        <div className="flex items-center gap-3">
          <Network className="text-red-500" size={24} />
          <h3 className="text-xl font-bold text-white">Visual Referral Tree</h3>
        </div>

        <div className="relative w-full md:w-72">
          <input
            type="text"
            placeholder="Focus on specific user..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-red-500 text-sm transition-all"
          />
          <Search size={16} className="absolute left-3 top-3.5 text-gray-400" />
        </div>
      </div>

      <div className="flex flex-col gap-2 max-h-[600px] overflow-y-auto pr-2">
        {filteredRoots.length > 0 ? (
          filteredRoots.map(root => renderNode(root))
        ) : (
          <div className="text-center py-12 text-gray-400 text-sm">
            No matching user or tree structure found.
          </div>
        )}
      </div>
    </div>
  );
}
