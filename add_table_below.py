import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

old_grid = """              <SalesApprovals sales={sales} loading={salesLoading} onProcess={handleProcessSale} />
              <SystemLogs users={users} />
            </motion.div>
          </div>
        )}
      </div>
      
      {/* Global styles for custom scrollbar in admin panel */}"""

new_grid = """              <SalesApprovals sales={sales} loading={salesLoading} onProcess={handleProcessSale} />
              <SystemLogs users={users} />
            </motion.div>
          </div>
          
          <SalesHistoryTable sales={sales} />
        )}
      </div>
      
      {/* Global styles for custom scrollbar in admin panel */}"""

content = content.replace(old_grid, new_grid)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
