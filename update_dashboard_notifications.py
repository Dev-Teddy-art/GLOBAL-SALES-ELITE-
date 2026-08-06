import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# Add Bell to lucide imports
content = content.replace("BarChart as BarChartIcon } from 'lucide-react';", "BarChart as BarChartIcon, Bell } from 'lucide-react';")

# Add Notifications state
state_block = """  const [sponsorName, setSponsorName] = useState<string>('Admin');
  const navigate = useNavigate();"""
new_state_block = """  const [sponsorName, setSponsorName] = useState<string>('Admin');
  const [showNotifications, setShowNotifications] = useState(false);
  const navigate = useNavigate();
  
  const unreadCount = profile?.notifications?.filter(n => !n.read).length || 0;
  
  const handleOpenNotifications = async () => {
    setShowNotifications(!showNotifications);
    if (!showNotifications && unreadCount > 0) {
      try {
        await fetch('/api/auth/notifications/read', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userId: profile._id })
        });
        // Mutate local profile optimistically if possible, or it'll refresh on reload
      } catch (e) {
        console.error(e);
      }
    }
  };"""
content = content.replace(state_block, new_state_block)

# Add Notifications UI in header
header_block = """          <div className="flex items-center gap-4">
            {profile.isAdmin || profile.role === 'admin' ? ("""
new_header_block = """          <div className="flex items-center gap-4 relative">
            <div className="relative">
              <button onClick={handleOpenNotifications} className="relative p-2 text-white/80 hover:text-white hover:bg-white/10 rounded-xl transition-colors">
                <Bell size={20} />
                {unreadCount > 0 && (
                  <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-[#EF4444] rounded-full border-2 border-[#0F172A]" />
                )}
              </button>
              
              {showNotifications && (
                <div className="absolute right-0 mt-2 w-80 bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden z-50">
                  <div className="px-4 py-3 border-b border-gray-100 flex justify-between items-center bg-gray-50">
                    <h3 className="font-bold text-gray-900 text-sm">Notifications</h3>
                  </div>
                  <div className="max-h-80 overflow-y-auto">
                    {profile?.notifications && profile.notifications.length > 0 ? (
                      profile.notifications.slice().reverse().map(n => (
                        <div key={n.id} className={`px-4 py-3 text-sm border-b border-gray-50 last:border-0 ${n.read ? 'bg-white' : 'bg-[#EF4444]/5'}`}>
                          <p className="text-gray-800">{n.message}</p>
                          <span className="text-xs text-gray-400 mt-1 block">
                            {new Date(n.createdAt).toLocaleDateString()} {new Date(n.createdAt).toLocaleTimeString()}
                          </span>
                        </div>
                      ))
                    ) : (
                      <div className="px-4 py-8 text-center text-gray-500 text-sm">
                        No notifications yet
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
            
            {profile.isAdmin || profile.role === 'admin' ? ("""
content = content.replace(header_block, new_header_block)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
