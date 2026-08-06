import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

# Completely replace PayoutApprovals component
old_payouts = r"function PayoutApprovals\(\{ users \}: \{ users: any\[\] \}\) \{.*?  \);\n}"
new_payouts = """function PayoutApprovals({ users }: { users: any[] }) {
  const { profile } = useAuth();
  const [withdrawals, setWithdrawals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchWithdrawals = async () => {
      if (!profile) return;
      try {
        const res = await fetch(`/api/admin/withdrawals?adminId=${profile._id || profile.id}`);
        if (res.ok) {
          const data = await res.json();
          setWithdrawals(data);
        }
      } catch (err) {
        console.error("Error fetching withdrawals", err);
      } finally {
        setLoading(false);
      }
    };
    fetchWithdrawals();
  }, [profile]);

  const handleProcess = async (withdrawalId: string, status: 'approved' | 'rejected') => {
    try {
      const res = await fetch('/api/admin/withdrawals/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ adminId: profile?._id || profile?.id, withdrawalId, status })
      });
      if (res.ok) {
        setWithdrawals(withdrawals.filter(w => w._id !== withdrawalId));
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <>
      <div className="bg-white/90 dark:bg-[#0F172A]/80 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col h-[380px] relative z-10">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <DollarSign className="text-[#0F172A] dark:text-white" size={20} />
            Pending Payouts
          </h3>
          <span className="bg-[#EF4444] text-gray-900 dark:text-white text-xs font-bold px-2.5 py-1 rounded-full">{withdrawals.length}</span>
        </div>
        
        <div className="flex-1 overflow-auto custom-scrollbar pr-2 space-y-3">
          {loading ? (
            <div className="text-gray-500 text-center py-10 text-sm">Loading...</div>
          ) : withdrawals.length === 0 ? (
            <div className="text-gray-500 dark:text-gray-500 text-center py-10 text-sm">No pending payouts.</div>
          ) : (
            withdrawals.map((w) => (
              <motion.div 
                key={w._id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-gray-50 dark:bg-[#1E293B] border border-gray-200 dark:border-white/5 rounded-xl p-3 flex justify-between items-center group hover:border-[#EF4444]/30 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-[#EF4444]/10 flex items-center justify-center text-[#EF4444]">
                    <DollarSign size={16} />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-gray-900 dark:text-white leading-none">{w.userRef?.displayName}</p>
                    <p className="text-xs text-gray-500 mt-1">₦{w.amount.toLocaleString()} • {w.userRef?.bankName}</p>
                    <p className="text-xs text-gray-400 font-mono mt-0.5">{w.userRef?.bankAccountNumber}</p>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button onClick={() => handleProcess(w._id, 'approved')} className="text-xs font-bold bg-green-500/10 text-green-600 hover:bg-green-500 hover:text-white px-3 py-1.5 rounded-lg transition-colors">
                    Approve
                  </button>
                  <button onClick={() => handleProcess(w._id, 'rejected')} className="text-xs font-bold bg-red-500/10 text-red-600 hover:bg-red-500 hover:text-white px-3 py-1.5 rounded-lg transition-colors">
                    Reject
                  </button>
                </div>
              </motion.div>
            ))
          )}
        </div>
      </div>
    </>
  );
}"""
content = re.sub(old_payouts, new_payouts, content, flags=re.DOTALL)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
