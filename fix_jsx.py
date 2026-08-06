import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

old_jsx = """        {loading ? (
          <div className="flex-1 flex items-center justify-center text-[#EF4444] animate-pulse">Loading visualizer...</div>
        ) : (
          <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 relative z-20">"""
new_jsx = """        {loading ? (
          <div className="flex-1 flex items-center justify-center text-[#EF4444] animate-pulse">Loading visualizer...</div>
        ) : (
          <>
          <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 relative z-20">"""
content = content.replace(old_jsx, new_jsx)

old_jsx2 = """            </motion.div>
          </div>
          
          <SalesHistoryTable sales={sales} />
        )}"""
new_jsx2 = """            </motion.div>
          </div>
          
          <SalesHistoryTable sales={sales} />
          </>
        )}"""
content = content.replace(old_jsx2, new_jsx2)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
