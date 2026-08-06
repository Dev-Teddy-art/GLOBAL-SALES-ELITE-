import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Update chevron imports
content = content.replace("ChevronRight, Copy", "ChevronRight, ChevronDown, Copy")

# Add FAQ Component
faq_component = """
function FAQItem({ question, answer }: { question: string, answer: string }) {
  const [isOpen, setIsOpen] = React.useState(false);
  return (
    <div className="border-b border-gray-200 dark:border-white/10 pb-4">
      <button 
        onClick={() => setIsOpen(!isOpen)} 
        className="w-full flex justify-between items-center py-4 text-left font-bold text-gray-900 dark:text-white"
      >
        {question}
        <ChevronDown size={20} className={`transform transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ height: 0, opacity: 0 }} 
            animate={{ height: 'auto', opacity: 1 }} 
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden text-gray-600 dark:text-gray-400 text-sm leading-relaxed"
          >
            <p className="pb-4">{answer}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
"""

content = content.replace("function EarningsCalculator() {", faq_component + "\nfunction EarningsCalculator() {")

# Add Expansion Sections
new_sections = """      {/* Detailed Compensation Plan */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-24 border-t border-gray-100 dark:border-white/5 text-center">
        <h2 className="text-3xl md:text-5xl font-black text-gray-900 dark:text-white mb-6">Unrivaled Compensation Plan</h2>
        <p className="text-gray-600 dark:text-gray-400 font-medium text-lg leading-relaxed mb-12 max-w-2xl mx-auto">
          We built our payouts to maximize earning potential for both direct effort and team building.
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="bg-[#EF4444]/10 dark:bg-[#EF4444]/5 border border-[#EF4444]/20 rounded-3xl p-8 flex flex-col items-center justify-center">
            <h3 className="text-4xl font-black text-[#EF4444] mb-2">15%</h3>
            <p className="text-gray-900 dark:text-white font-bold text-lg">Direct Referral</p>
            <p className="text-gray-500 text-sm mt-2 text-center">Earn 15% immediately for anyone who signs up directly using your link.</p>
          </div>
          <div className="bg-white dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-3xl p-8 flex flex-col items-center justify-center">
            <h3 className="text-4xl font-black text-gray-900 dark:text-white mb-2">3%</h3>
            <p className="text-gray-900 dark:text-white font-bold text-lg">Indirect Level 2</p>
            <p className="text-gray-500 text-sm mt-2 text-center">Earn 3% for the direct referrals made by your Level 1 network.</p>
          </div>
          <div className="bg-white dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded-3xl p-8 flex flex-col items-center justify-center">
            <h3 className="text-4xl font-black text-gray-900 dark:text-white mb-2">1%</h3>
            <p className="text-gray-900 dark:text-white font-bold text-lg">Indirect Level 3+</p>
            <p className="text-gray-500 text-sm mt-2 text-center">Earn 1% on deeper network sales, driving massive spillover income.</p>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-24 border-t border-gray-100 dark:border-white/5">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-black text-gray-900 dark:text-white mb-4">Success Stories</h2>
          <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto font-medium">Hear from top earners who are already scaling their network in our global matrix.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 p-8 rounded-3xl">
            <div className="flex gap-1 text-yellow-400 mb-4">★★★★★</div>
            <p className="text-gray-600 dark:text-gray-400 italic mb-6 leading-relaxed">
              "The 15% direct commission and immediate withdrawals changed the game for my agency. The visual network tree makes it so easy to see where spillover is happening."
            </p>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gray-200 rounded-full bg-[url('https://i.pravatar.cc/150?img=33')] bg-cover" />
              <div>
                <p className="font-bold text-gray-900 dark:text-white">Sarah O.</p>
                <p className="text-xs text-gray-500">Executive Director</p>
              </div>
            </div>
          </div>
          <div className="bg-white dark:bg-[#1E293B] border border-gray-200 dark:border-white/10 p-8 rounded-3xl">
            <div className="flex gap-1 text-yellow-400 mb-4">★★★★★</div>
            <p className="text-gray-600 dark:text-gray-400 italic mb-6 leading-relaxed">
              "I've built teams in three different systems before, but GSE's dual-leg matrix ensures my team actually benefits from my over-recruiting. Highly recommended."
            </p>
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gray-200 rounded-full bg-[url('https://i.pravatar.cc/150?img=11')] bg-cover" />
              <div>
                <p className="font-bold text-gray-900 dark:text-white">David K.</p>
                <p className="text-xs text-gray-500">Diamond Rank Earner</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="relative z-10 max-w-3xl mx-auto px-6 py-24 border-t border-gray-100 dark:border-white/5">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-black text-gray-900 dark:text-white mb-4">Frequently Asked Questions</h2>
        </div>
        <div className="space-y-2">
          <FAQItem 
            question="How do I get paid?" 
            answer="Commissions are instantly credited to your GSE dashboard. You can request a withdrawal to your registered local bank account at any time. Our admin team processes payouts usually within 24 hours."
          />
          <FAQItem 
            question="What happens if I recruit more than 2 people?" 
            answer="Because GSE uses a 2-leg binary matrix, your 3rd recruit will automatically 'spill over' into the downline of your first two recruits. This helps your team grow and motivates everyone!"
          />
          <FAQItem 
            question="Is there a limit to how deep I can earn?" 
            answer="Direct (15%) and Level 2 (3%) are uncapped in volume. Deep network bonuses (1%) apply significantly across your entire lineage, ensuring you keep earning as your tree expands."
          />
        </div>
      </section>
"""

content = content.replace("{/* Footer */}", new_sections + "\n{/* Footer */}")

with open('src/App.tsx', 'w') as f:
    f.write(content)
