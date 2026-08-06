import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

# Add Check to lucide-react imports if not there
if 'Check,' not in content:
    content = content.replace("Landmark, History, Terminal", "Landmark, History, Terminal, Check")

success_animation_code = """
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

export function AdminConsolePage() {"""

content = content.replace('export function AdminConsolePage() {', success_animation_code)

# Add showSuccess state
old_admin_state = """  const [sales, setSales] = useState<any[]>([]);
  const [editingUser, setEditingUser] = useState<any | null>(null);"""

new_admin_state = """  const [sales, setSales] = useState<any[]>([]);
  const [editingUser, setEditingUser] = useState<any | null>(null);
  const [showSuccess, setShowSuccess] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");"""

content = content.replace(old_admin_state, new_admin_state)

# Update handleProcessSale
old_handle_process = """  const handleProcessSale = async (saleId: string, status: 'approved' | 'rejected') => {
    try {
      const res = await fetch('/api/admin/sales/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ adminId: profile?._id || profile?.id, saleId, status })
      });
      if (res.ok) {
        setSales(sales.map(s => s._id === saleId ? { ...s, status } : s));
      }
    } catch (e) {
      console.error(e);
    }
  };"""

new_handle_process = """  const handleProcessSale = async (saleId: string, status: 'approved' | 'rejected') => {
    try {
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
  };"""

content = content.replace(old_handle_process, new_handle_process)

# Add SuccessAnimation to AdminConsolePage render
old_return = """  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#0B0F19] font-sans relative overflow-hidden flex flex-col">"""

new_return = """  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#0B0F19] font-sans relative overflow-hidden flex flex-col">
      <SuccessAnimation show={showSuccess} message={successMessage} />"""

content = content.replace(old_return, new_return)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
