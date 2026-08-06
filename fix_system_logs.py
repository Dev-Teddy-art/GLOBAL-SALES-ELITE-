import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

system_logs_new = """function SystemLogs({ users }: { users: any[] }) {
  // Use real data (recent users) to generate logs instead of mock data
  const recentUsers = [...users].sort((a, b) => new Date(b.createdAt || 0).getTime() - new Date(a.createdAt || 0).getTime()).slice(0, 5);
  
  return (
    <div className="bg-white/90 dark:bg-[#0F172A]/80 backdrop-blur-xl border border-gray-200 dark:border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col h-[396px]">
      <h3 className="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2 mb-4">
        <Activity className="text-blue-400" size={20} />
        System Logs
      </h3>
      
      <div className="flex-1 overflow-auto custom-scrollbar pr-2 space-y-4">
        {recentUsers.length === 0 ? (
          <div className="text-gray-500 dark:text-gray-500 text-center py-10 text-sm">No recent activity.</div>
        ) : (
          recentUsers.map((u, i) => (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 + 0.3 }}
              key={u.id || i} 
              className="flex gap-3 items-start"
            >
              <div className="mt-0.5 w-2 h-2 rounded-full flex-shrink-0 bg-blue-400" />
              <div>
                <p className="text-sm text-gray-700 dark:text-gray-300 leading-tight">New user registration: {u.displayName}</p>
                <span className="text-xs text-gray-500 dark:text-gray-500">{new Date(u.createdAt || Date.now()).toLocaleDateString()}</span>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </div>
  );
}"""

content = re.sub(r'function SystemLogs\(\) \{.*?(?=export function AdminConsolePage)', system_logs_new + '\n\n', content, flags=re.DOTALL)

content = content.replace('<SystemLogs />', '<SystemLogs users={users} />')

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
