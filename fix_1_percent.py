import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_comp = "Earn 5% on direct referrals, 2% on second level, and 1% down to level 5. A robust compensation plan built for massive scaling."
new_comp = "Earn 15% on direct referrals, and 3% on second level. A robust compensation plan built for massive scaling."
content = content.replace(old_comp, new_comp)

old_1_percent = """          <div className="bg-white dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-3xl p-8 flex flex-col items-center justify-center">
            <h3 className="text-4xl font-black text-gray-900 dark:text-white mb-2">1%</h3>
            <p className="text-gray-900 dark:text-white font-bold text-lg">Indirect Level 3+</p>
            <p className="text-gray-600 dark:text-gray-400 text-sm mt-2 text-center">Earn 1% on deeper network sales, driving massive spillover income.</p>
          </div>"""
new_1_percent = """          <div className="bg-white dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-3xl p-8 flex flex-col items-center justify-center relative overflow-hidden">
            <div className="absolute top-4 right-4"><Crown size={16} className="text-yellow-500" /></div>
            <h3 className="text-4xl font-black text-gray-900 dark:text-white mb-2">1%</h3>
            <p className="text-gray-900 dark:text-white font-bold text-lg text-center">Indirect Level 3+<br/><span className="text-sm font-normal text-gray-500">(Admin Only)</span></p>
            <p className="text-gray-600 dark:text-gray-400 text-sm mt-2 text-center">Exclusive to Admin owners. Earn 1% on all deeper network sales.</p>
          </div>"""
content = content.replace(old_1_percent, new_1_percent)

old_faq = """          <FAQItem 
            question="Is there a limit to how deep I can earn?" 
            answer="Direct (15%) and Level 2 (3%) are uncapped in volume. Deep network bonuses (1%) apply significantly across your entire lineage, ensuring you keep earning as your tree expands."
          />"""
new_faq = """          <FAQItem 
            question="Is there a limit to how deep I can earn?" 
            answer="Direct (15%) and Level 2 (3%) are uncapped in volume. Deep network bonuses (1%) are strictly reserved for the Admin owner, ensuring the platform scales sustainably."
          />"""
content = content.replace(old_faq, new_faq)

with open('src/App.tsx', 'w') as f:
    f.write(content)
