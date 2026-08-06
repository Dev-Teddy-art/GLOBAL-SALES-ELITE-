import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

# Add motion import
if "from 'motion/react'" not in content:
    content = content.replace("import { sanityClient } from '../lib/sanity';", "import { sanityClient } from '../lib/sanity';\nimport { motion } from 'motion/react';")

# NetworkTreeView
old_network_map = '''          {users.map(user => (
            <tr key={user.id} className="hover:bg-gray-50 transition-colors">'''

new_network_map = '''          {users.map((user, index) => (
            <motion.tr 
              key={user.id} 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
              className="hover:bg-gray-50 transition-colors"
            >'''
content = content.replace(old_network_map, new_network_map)

# Replace the closing tr for NetworkTreeView
# It's tricky to replace just the closing tr, so we can use a regex or replace all </tr> inside that map?
# We can replace the exact block:
old_network_tr_close = '''              </td>
            </tr>
          ))}'''
new_network_tr_close = '''              </td>
            </motion.tr>
          ))}'''
content = content.replace(old_network_tr_close, new_network_tr_close)


# PayoutsManagement
old_payout_map = '''            {users.filter(u => u.role !== 'admin' && u.bankAccountNumber).map(user => (
              <React.Fragment key={user.id}>
                <tr className="hover:bg-gray-50 transition-colors">'''

new_payout_map = '''            {users.filter(u => u.role !== 'admin' && u.bankAccountNumber).map((user, index) => (
              <React.Fragment key={user.id}>
                <motion.tr 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                  className="hover:bg-gray-50 transition-colors"
                >'''
content = content.replace(old_payout_map, new_payout_map)

old_payout_tr_close = '''                  </td>
                </tr>
                {expandedRow === user.id && ('''
new_payout_tr_close = '''                  </td>
                </motion.tr>
                {expandedRow === user.id && ('''
content = content.replace(old_payout_tr_close, new_payout_tr_close)

old_expanded_tr = '''                  <tr className="bg-red-50/30">'''
new_expanded_tr = '''                  <motion.tr 
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="bg-red-50/30"
                  >'''
content = content.replace(old_expanded_tr, new_expanded_tr)

old_expanded_tr_close = '''                    </td>
                  </tr>
                )}
              </React.Fragment>'''
new_expanded_tr_close = '''                    </td>
                  </motion.tr>
                )}
              </React.Fragment>'''
content = content.replace(old_expanded_tr_close, new_expanded_tr_close)

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
