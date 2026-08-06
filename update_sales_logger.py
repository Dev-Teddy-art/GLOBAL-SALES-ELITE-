import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

old_sales_logger = """  const [submitting, setSubmitting] = useState(false);

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
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.4 }} className="bg-white dark:bg-[#0F172A] rounded-3xl shadow-lg border border-gray-200 dark:border-white/10 p-6 md:p-8 relative overflow-hidden">"""

new_sales_logger = """  const [submitting, setSubmitting] = useState(false);
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
      <SuccessAnimation show={showSuccess} message="Commission Requested!" />"""

content = content.replace(old_sales_logger, new_sales_logger)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
