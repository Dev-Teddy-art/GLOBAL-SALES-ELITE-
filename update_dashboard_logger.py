import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

old_logger = """function SalesLogger() {
  const { profile } = useAuth();
  const [amount, setAmount] = useState<number | ''>('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!amount || amount <= 0 || !profile) return;
    
    setSubmitting(true);
    try {
      const res = await fetch('/api/sales', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: profile._id || profile.id, amount })
      });
      if (res.ok) {
        alert("Sale logged successfully! Commission request sent to Admin.");
        setAmount('');
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
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.4 }} className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6 md:p-8 relative overflow-hidden">
      <div className="flex items-center gap-4 mb-6 relative z-10">
        <div className="bg-gradient-to-br from-[#10B981] to-[#047857] p-3 rounded-2xl shadow-md text-white">
          <DollarSign size={24} />
        </div>
        <div>
          <h3 className="text-xl font-black text-gray-900 tracking-tight">
            Log a Sale
          </h3>
          <p className="text-gray-500 text-sm font-medium">Record amounts you have sold to request commissions</p>
        </div>
      </div>
      
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4 items-end relative z-10">
        <div className="flex-1 w-full">
          <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Amount Sold (₦)</label>
          <input 
            type="number" 
            min="0"
            value={amount}
            onChange={(e) => setAmount(Number(e.target.value) || '')}
            placeholder="e.g. 500000"
            className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#10B981] focus:border-transparent outline-none transition-all font-mono font-bold"
            required
          />
        </div>
        <button 
          type="submit" 
          disabled={submitting || !amount}
          className="bg-[#10B981] hover:bg-[#059669] disabled:opacity-50 text-white px-8 py-3 rounded-xl font-bold shadow-lg transition-all h-[50px] w-full sm:w-auto whitespace-nowrap"
        >
          {submitting ? 'Submitting...' : 'Log Sale'}
        </button>
      </form>
    </motion.div>
  );
}"""

new_logger = """function SalesLogger() {
  const { profile } = useAuth();
  const [amount, setAmount] = useState<number | ''>('');
  const [propertyName, setPropertyName] = useState('');
  const [dateSold, setDateSold] = useState('');
  const [submitting, setSubmitting] = useState(false);

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
        alert("Sale logged successfully! Commission request sent to Admin.");
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
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.4 }} className="bg-white rounded-3xl shadow-lg border border-gray-100 p-6 md:p-8 relative overflow-hidden">
      <div className="flex items-center gap-4 mb-6 relative z-10">
        <div className="bg-gradient-to-br from-[#10B981] to-[#047857] p-3 rounded-2xl shadow-md text-white">
          <DollarSign size={24} />
        </div>
        <div>
          <h3 className="text-xl font-black text-gray-900 tracking-tight">
            Log a Sale
          </h3>
          <p className="text-gray-500 text-sm font-medium">Record sales to automatically request commissions</p>
        </div>
      </div>
      
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex-1 w-full">
            <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Property Name</label>
            <input 
              type="text" 
              value={propertyName}
              onChange={(e) => setPropertyName(e.target.value)}
              placeholder="e.g. Seaside Villa"
              className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#10B981] focus:border-transparent outline-none transition-all font-bold"
              required
            />
          </div>
          <div className="flex-1 w-full">
            <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Amount Sold (₦)</label>
            <input 
              type="number" 
              min="0"
              value={amount}
              onChange={(e) => setAmount(Number(e.target.value) || '')}
              placeholder="e.g. 5000000"
              className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#10B981] focus:border-transparent outline-none transition-all font-mono font-bold"
              required
            />
          </div>
          <div className="flex-1 w-full">
            <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Date Sold</label>
            <input 
              type="date" 
              value={dateSold}
              onChange={(e) => setDateSold(e.target.value)}
              className="w-full bg-gray-50 border border-gray-200 text-gray-900 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#10B981] focus:border-transparent outline-none transition-all font-bold"
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
}"""

content = content.replace(old_logger, new_logger)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
