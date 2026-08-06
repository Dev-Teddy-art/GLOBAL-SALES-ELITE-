import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# Add a toast state inside Dashboard component
toast_state = """
  const [showToast, setShowToast] = useState(false);
"""

# Find the start of Dashboard component
content = content.replace("export function Dashboard() {\n  const { user, profile, signOut } = useAuth();", "export function Dashboard() {\n  const { user, profile, signOut } = useAuth();\n  const [showToast, setShowToast] = useState(false);")

# Update copyReferralLink
old_copy = """  const copyReferralLink = (e: React.MouseEvent) => {
    e.stopPropagation();
    e.preventDefault();
    const link = `${window.location.origin}/signup?ref=${profile?.referralCode}`;
    navigator.clipboard.writeText(link);
    alert('Referral link copied to clipboard!');
  };"""

new_copy = """  const copyReferralLink = (e: React.MouseEvent) => {
    e.stopPropagation();
    e.preventDefault();
    const link = `${window.location.origin}/signup?ref=${profile?.referralCode}`;
    navigator.clipboard.writeText(link);
    setShowToast(true);
    setTimeout(() => setShowToast(false), 3000);
  };"""

content = content.replace(old_copy, new_copy)

# Add Toast UI near the top level of return (min-h-screen container)
old_return = """    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">"""
new_return = """    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      {/* Toast Notification */}
      <div className={`fixed top-6 right-6 z-[100] transition-all duration-300 transform ${showToast ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0 pointer-events-none'}`}>
        <div className="bg-[#10B981] text-white px-6 py-4 rounded-xl shadow-2xl flex items-center gap-3 font-semibold text-sm">
          <div className="bg-white/20 p-1.5 rounded-full">
            <Copy size={16} className="text-white" />
          </div>
          Referral link copied to clipboard!
        </div>
      </div>"""

content = content.replace(old_return, new_return)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
