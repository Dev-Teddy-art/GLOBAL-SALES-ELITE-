import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

# Make sure Navbar is imported
if "import { Navbar }" not in content:
    content = content.replace("import { ThemeToggle } from './ThemeToggle';", "import { ThemeToggle } from './ThemeToggle';\nimport { Navbar } from './Navbar';")

old_header_block = """      <div className="max-w-[1600px] mx-auto p-4 md:p-8 relative z-10 flex flex-col">
        {/* Top Header */}
        <motion.header 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col md:flex-row items-center justify-between gap-6 mb-8 bg-white/80 dark:bg-[#0F172A]/50 backdrop-blur-md border border-gray-200 dark:border-white/5 p-4 rounded-3xl"
        >
          <div className="flex items-center gap-4">
            <ThemeToggle className="text-gray-900 dark:text-gray-300" />
            <button 
              onClick={() => navigate('/dashboard')} 
              className="h-10 w-10 bg-white/5 hover:bg-white/10 rounded-full flex items-center justify-center transition-colors"
            >
              <ChevronLeft size={20} className="text-gray-700 dark:text-gray-300" />
            </button>
            <div>
              <h1 className="text-2xl font-black text-gray-900 dark:text-white flex items-center gap-2">
                <Crown className="text-[#EF4444]" /> GSE Admin Portal
              </h1>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-4">
            <div className="bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-white/5 px-4 py-2 rounded-xl flex items-center gap-3">
              <div className="bg-[#0F172A]/20 p-1.5 rounded-lg"><Users size={16} className="text-[#0F172A] dark:text-white" /></div>
              <div>
                <div className="text-[10px] uppercase text-gray-500 dark:text-gray-500 font-bold">Total Network</div>
                <div className="text-sm font-bold text-gray-900 dark:text-white">{users.length} Nodes</div>
              </div>
            </div>
            <div className="bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-white/5 px-4 py-2 rounded-xl flex items-center gap-3">
              <div className="bg-[#0F172A]/20 p-1.5 rounded-lg"><Activity size={16} className="text-[#0F172A] dark:text-white" /></div>
              <div>
                <div className="text-[10px] uppercase text-gray-500 dark:text-gray-500 font-bold">System Status</div>
                <div className="text-sm font-bold text-[#0F172A] dark:text-white flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#0F172A] animate-pulse" /> Healthy
                </div>
              </div>
            </div>
          </div>
        </motion.header>"""

new_header_block = """      <Navbar />
      <div className="max-w-[1600px] mx-auto p-4 md:p-8 pt-12 relative z-10 flex flex-col">
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col md:flex-row items-center justify-between gap-6 mb-8"
        >
          <div className="flex items-center gap-4">
            <h1 className="text-3xl font-black text-gray-900 dark:text-white flex items-center gap-3">
              <Crown className="text-[#EF4444]" /> GSE Admin Portal
            </h1>
          </div>

          <div className="flex flex-wrap items-center gap-4">
            <ThemeToggle className="text-gray-900 dark:text-gray-300 mr-2" />
            <div className="bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-white/5 px-4 py-2 rounded-xl flex items-center gap-3 shadow-sm">
              <div className="bg-[#0F172A]/10 dark:bg-[#0F172A]/50 p-1.5 rounded-lg"><Users size={16} className="text-[#0F172A] dark:text-white" /></div>
              <div>
                <div className="text-[10px] uppercase text-gray-500 dark:text-gray-500 font-bold">Total Network</div>
                <div className="text-sm font-bold text-gray-900 dark:text-white">{users.length} Nodes</div>
              </div>
            </div>
            <div className="bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-white/5 px-4 py-2 rounded-xl flex items-center gap-3 shadow-sm">
              <div className="bg-[#0F172A]/10 dark:bg-[#0F172A]/50 p-1.5 rounded-lg"><Activity size={16} className="text-[#0F172A] dark:text-white" /></div>
              <div>
                <div className="text-[10px] uppercase text-gray-500 dark:text-gray-500 font-bold">System Status</div>
                <div className="text-sm font-bold text-[#0F172A] dark:text-white flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#0F172A] animate-pulse" /> Healthy
                </div>
              </div>
            </div>
          </div>
        </motion.div>"""

content = content.replace(old_header_block, new_header_block)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
