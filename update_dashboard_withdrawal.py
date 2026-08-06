import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# Add request withdrawal function to CommissionCalculator
logic = """  const currencyFormatter = new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN' });

  const [requesting, setRequesting] = useState(false);
  const { profile } = useAuth();
  const handleWithdraw = async () => {
    if (!profile) return;
    if (!profile.bankAccountNumber) {
      alert("Please update your bank account details in your profile before withdrawing.");
      return;
    }
    setRequesting(true);
    try {
      const res = await fetch('/api/withdrawals', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: profile._id || profile.id, amount: totalEarnings })
      });
      if (res.ok) alert("Withdrawal request submitted successfully!");
    } catch (e) {
      console.error(e);
      alert("Failed to request withdrawal.");
    } finally {
      setRequesting(false);
    }
  };
"""
content = content.replace("  const currencyFormatter = new Intl.NumberFormat('en-NG', { style: 'currency', currency: 'NGN' });", logic)

# Add withdraw button under the estimated earnings
old_est = """          <div className="h-1.5 w-12 bg-gradient-to-r from-[#EF4444] to-[#EF4444]/80 rounded-full mb-6 z-10" />
          <p className="text-white/70 text-sm max-w-[250px] font-medium z-10 leading-relaxed">
            This is an estimate based on {role === 'admin' ? '3' : '2'} levels of your network downline.
          </p>
        </div>"""
new_est = """          <div className="h-1.5 w-12 bg-gradient-to-r from-[#EF4444] to-[#EF4444]/80 rounded-full mb-6 z-10" />
          <p className="text-white/70 text-sm max-w-[250px] font-medium z-10 leading-relaxed mb-6">
            This is an estimate based on {role === 'admin' ? '3' : '2'} levels of your network downline.
          </p>
          <button 
            onClick={handleWithdraw}
            disabled={requesting || totalEarnings === 0}
            className="relative z-10 bg-[#EF4444] hover:bg-[#c9291f] disabled:opacity-50 text-white px-8 py-3 rounded-xl font-bold text-sm shadow-xl transition-all"
          >
            {requesting ? 'Processing...' : 'Request Withdrawal'}
          </button>
        </div>"""
content = content.replace(old_est, new_est)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
