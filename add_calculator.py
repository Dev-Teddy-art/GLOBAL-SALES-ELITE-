import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

calculator_jsx = """
      {/* Earnings Calculator Section */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-24 border-t border-white/5">
        <div className="flex flex-col lg:flex-row gap-16 items-center">
          <div className="flex-1 text-left">
            <h2 className="text-3xl md:text-5xl font-black text-white mb-6">Calculate Your Potential</h2>
            <p className="text-gray-400 font-medium text-lg leading-relaxed mb-8 max-w-xl">
              Use our interactive slider to project your estimated weekly earnings based on active network referrals and system spillover. 
            </p>
            <div className="flex items-center gap-4">
              <div className="flex -space-x-4">
                {[1,2,3,4].map(i => (
                  <div key={i} className={`w-12 h-12 rounded-full border-2 border-[#0B0F19] bg-gradient-to-br from-red-500 to-red-900 flex items-center justify-center font-bold text-white text-xs z-${10-i}`}>
                    +{i}k
                  </div>
                ))}
              </div>
              <span className="text-gray-500 text-sm font-bold uppercase tracking-widest">Active Earners</span>
            </div>
          </div>
          
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="flex-1 w-full bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 lg:p-12 shadow-2xl relative"
          >
            {/* Ambient Glow */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-red-500/10 rounded-full blur-[80px] pointer-events-none" />
            
            <EarningsCalculator />
          </motion.div>
        </div>
      </section>
"""

# Insert before Footer
footer_idx = content.find('{/* Footer */}')
if footer_idx != -1:
    content = content[:footer_idx] + calculator_jsx + content[footer_idx:]

calculator_component = """
function EarningsCalculator() {
  const [directReferrals, setDirectReferrals] = React.useState(5);
  const [teamDepth, setTeamDepth] = React.useState(3);

  const calculateEarnings = () => {
    const baseValue = 50000; // 50,000 NGN
    const directBonus = directReferrals * (baseValue * 0.05);
    const indirectBonus = (Math.pow(2, teamDepth) - 2) * (baseValue * 0.02);
    return directBonus + indirectBonus;
  };

  return (
    <div className="flex flex-col gap-8 relative z-10">
      <div>
        <div className="flex justify-between mb-2">
          <label className="text-white font-bold text-sm">Direct Referrals</label>
          <span className="text-[#EF4444] font-black">{directReferrals}</span>
        </div>
        <input 
          type="range" 
          min="1" max="50" 
          value={directReferrals} 
          onChange={e => setDirectReferrals(parseInt(e.target.value))}
          className="w-full accent-[#EF4444] h-2 bg-black/40 rounded-lg appearance-none cursor-pointer"
        />
      </div>
      
      <div>
        <div className="flex justify-between mb-2">
          <label className="text-white font-bold text-sm">Average Team Depth</label>
          <span className="text-[#EF4444] font-black">Level {teamDepth}</span>
        </div>
        <input 
          type="range" 
          min="1" max="10" 
          value={teamDepth} 
          onChange={e => setTeamDepth(parseInt(e.target.value))}
          className="w-full accent-[#EF4444] h-2 bg-black/40 rounded-lg appearance-none cursor-pointer"
        />
      </div>

      <div className="bg-black/30 border border-white/10 rounded-2xl p-6 mt-4 flex items-center justify-between">
        <div>
          <div className="text-xs text-gray-400 font-bold uppercase tracking-wider mb-1">Projected Weekly Income</div>
          <div className="text-3xl font-black text-white">₦{calculateEarnings().toLocaleString()}</div>
        </div>
        <div className="w-12 h-12 rounded-full bg-emerald-500/20 flex items-center justify-center">
          <DollarSign className="text-emerald-400" size={24} />
        </div>
      </div>
    </div>
  );
}
"""

content = content.replace("function LandingPage() {", calculator_component + "\nfunction LandingPage() {")

with open('src/App.tsx', 'w') as f:
    f.write(content)

