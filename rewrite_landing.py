import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Replace LandingPage
landing_page_pattern = re.compile(r'function LandingPage\(\) \{.*?(?=function SignUpPage\(\) \{)', re.DOTALL)

# We will create a new LandingPage function.
new_landing_page = """function LandingPage() {
  const { user, loading, signInWithEmail } = useAuth();
  const navigate = useNavigate();
  const [isSigningIn, setIsSigningIn] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState('');

  const [showLoginModal, setShowLoginModal] = React.useState(false);
  const [loginEmail, setLoginEmail] = React.useState('');
  const [loginPassword, setLoginPassword] = React.useState('');
  const [showLoginPassword, setShowLoginPassword] = React.useState(false);

  if (loading) return <div className="min-h-screen bg-[#0B0F19] flex items-center justify-center text-white">Loading...</div>;
  if (user) return <Navigate to="/dashboard" replace />;

  const handleLogin = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!loginEmail || !loginPassword) return;
    
    setIsSigningIn(true);
    setErrorMsg('');
    try {
      await signInWithEmail(loginEmail, loginPassword);
    } catch (err: any) {
      setErrorMsg(err.message || String(err));
      console.error("SANITY DB ERROR:", err);
    } finally {
      setIsSigningIn(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] flex flex-col font-sans selection:bg-[#EF4444] selection:text-white overflow-hidden relative">
      {/* Dynamic Background */}
      <div className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] bg-[#1E3A8A]/30 rounded-full blur-[120px] pointer-events-none mix-blend-screen" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40vw] h-[40vw] bg-[#EF4444]/20 rounded-full blur-[150px] pointer-events-none mix-blend-screen" />
      
      {/* Floating Header */}
      <header className="fixed top-4 left-0 right-0 z-50 w-full max-w-7xl mx-auto px-4">
        <motion.div 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="flex justify-between items-center bg-white/5 backdrop-blur-lg border border-white/10 p-4 rounded-2xl shadow-xl"
        >
          <div className="flex items-center gap-6">
            <div className="text-white font-black text-xl tracking-tighter flex items-center gap-2">
              <span className="bg-[#EF4444] p-1.5 rounded-lg"><Network size={20} className="text-white" /></span>
              GSE
            </div>
          </div>
          <div className="flex items-center gap-4">
            <button onClick={() => setShowLoginModal(true)} className="text-white/80 hover:text-white font-semibold text-sm transition-colors">
              Login
            </button>
            <button onClick={() => navigate('/signup')} className="bg-[#EF4444] hover:bg-red-500 text-white font-bold text-sm px-5 py-2.5 rounded-xl shadow-[0_0_15px_rgba(239,68,68,0.4)] transition-all transform hover:scale-105">
              Get Started
            </button>
          </div>
        </motion.div>
      </header>

      {/* Main Hero Section */}
      <section className="relative z-10 flex flex-col lg:flex-row items-center justify-between max-w-7xl mx-auto w-full px-6 pt-32 pb-20 min-h-screen">
        
        {/* Left Copy */}
        <motion.div 
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          variants={{
            hidden: {},
            visible: { transition: { staggerChildren: 0.1 } }
          }}
          className="flex-1 flex flex-col items-start gap-6 pt-10"
        >
          <motion.div variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }} className="inline-flex items-center gap-2 bg-[#EF4444]/10 border border-[#EF4444]/30 px-3 py-1.5 rounded-full">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#EF4444] opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[#EF4444]"></span>
            </span>
            <span className="text-[#EF4444] text-xs font-bold tracking-wider uppercase">Live Spillover Active</span>
          </motion.div>
          
          <motion.h1 
            variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
            className="text-5xl md:text-7xl font-black text-white leading-[1.1] tracking-tight"
          >
            Build Your <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-white via-gray-200 to-gray-500">Binary Network.</span><br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#EF4444] to-red-600">Maximize Earnings.</span>
          </motion.h1>
          
          <motion.p 
            variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
            className="text-lg text-gray-400 max-w-lg leading-relaxed font-medium"
          >
            Join the Global Sales Elite platform. Leverage our automated 2-leg spillover matrix, earn multi-tier commissions, and track your global downline in real-time.
          </motion.p>
          
          <motion.div 
            variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
            className="flex items-center gap-4 mt-4"
          >
            <button onClick={() => navigate('/signup')} className="bg-[#EF4444] hover:bg-red-500 text-white font-bold text-lg px-8 py-4 rounded-xl shadow-[0_0_20px_rgba(239,68,68,0.3)] transition-all transform hover:scale-105 flex items-center gap-2">
              Join the Network <ChevronRight size={20} />
            </button>
          </motion.div>
        </motion.div>

        {/* Right Live Preview Graphic */}
        <motion.div 
          initial={{ opacity: 0, x: 40, rotateY: 10 }}
          animate={{ opacity: 1, x: 0, rotateY: 0 }}
          transition={{ type: "spring", stiffness: 50, delay: 0.2 }}
          className="flex-1 w-full max-w-lg mt-16 lg:mt-0 relative"
          style={{ perspective: '1000px' }}
        >
          <div className="bg-[#1E293B]/80 backdrop-blur-2xl border border-white/10 rounded-3xl p-6 shadow-2xl relative">
            <div className="flex items-center justify-between mb-8 border-b border-white/10 pb-4">
              <h3 className="text-white font-bold flex items-center gap-2">
                <Network className="text-blue-400" size={18}/> Live Matrix Simulator
              </h3>
              <div className="flex gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-red-500" />
                <div className="w-2.5 h-2.5 rounded-full bg-yellow-500" />
                <div className="w-2.5 h-2.5 rounded-full bg-green-500" />
              </div>
            </div>
            
            {/* Mock Binary Tree Animation */}
            <div className="flex flex-col items-center gap-6 relative pt-4">
              <motion.div 
                animate={{ y: [0, -5, 0] }} 
                transition={{ repeat: Infinity, duration: 3, ease: "easeInOut" }}
                className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#1E3A8A] to-[#0F172A] border border-blue-500/30 flex items-center justify-center text-white font-bold shadow-[0_0_15px_rgba(30,58,138,0.5)] z-10"
              >
                YOU
              </motion.div>
              
              {/* Lines */}
              <svg className="absolute top-16 left-0 w-full h-32 pointer-events-none" preserveAspectRatio="none">
                <path d="M 230 0 C 230 40, 100 40, 100 80" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="2" />
                <path d="M 230 0 C 230 40, 360 40, 360 80" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="2" />
              </svg>

              <div className="flex gap-20 w-full justify-center">
                <motion.div 
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 1 }}
                  className="w-12 h-12 rounded-full bg-[#1E293B] border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-xs shadow-[0_0_10px_rgba(16,185,129,0.2)] z-10"
                >
                  L1
                </motion.div>
                <motion.div 
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 2.5 }}
                  className="w-12 h-12 rounded-full bg-[#1E293B] border border-[#EF4444]/30 flex items-center justify-center text-[#EF4444] font-bold text-xs shadow-[0_0_10px_rgba(239,68,68,0.2)] z-10 relative"
                >
                  <motion.div 
                    initial={{ scale: 2, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ delay: 2.3 }}
                    className="absolute -top-3 -right-3 bg-red-500 text-white text-[9px] font-bold px-1.5 py-0.5 rounded"
                  >
                    NEW
                  </motion.div>
                  R1
                </motion.div>
              </div>
              
              {/* Stats Ticker */}
              <div className="w-full bg-black/40 rounded-xl p-4 mt-4 flex justify-between items-center border border-white/5">
                <div className="text-center">
                  <div className="text-[10px] text-gray-500 uppercase font-bold tracking-wider">Total Volume</div>
                  <div className="text-emerald-400 font-mono font-bold">₦12.5M</div>
                </div>
                <div className="h-6 w-px bg-white/10" />
                <div className="text-center">
                  <div className="text-[10px] text-gray-500 uppercase font-bold tracking-wider">Network Size</div>
                  <div className="text-blue-400 font-mono font-bold">1,402</div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Value Prop Grid */}
      <section className="relative z-10 max-w-7xl mx-auto px-6 py-24">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-black text-white mb-4">Engineered for Growth</h2>
          <p className="text-gray-400 max-w-2xl mx-auto font-medium">Our system is designed to reward active builders while ensuring sustainable payouts through advanced matrix mechanics.</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="bg-white/5 backdrop-blur-md border border-white/10 hover:border-red-500/50 transition-all rounded-3xl p-8 flex flex-col gap-4 group"
          >
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#EF4444] to-red-900 flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
              <Network size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-white mt-2">2-Leg Spillover Matrix</h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              Every node has exactly two spots. Additional recruits automatically "spill over" to the next available spot in your downline, helping your team grow faster.
            </p>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="bg-white/5 backdrop-blur-md border border-white/10 hover:border-blue-500/50 transition-all rounded-3xl p-8 flex flex-col gap-4 group"
          >
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#1E3A8A] to-blue-900 flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
              <DollarSign size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-white mt-2">Tiered Commissions</h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              Earn 5% on direct referrals, 2% on second level, and 1% down to level 5. A robust compensation plan built for massive scaling.
            </p>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="bg-white/5 backdrop-blur-md border border-white/10 hover:border-emerald-500/50 transition-all rounded-3xl p-8 flex flex-col gap-4 group"
          >
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-500 to-emerald-900 flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
              <Activity size={28} className="text-white" />
            </div>
            <h3 className="text-xl font-bold text-white mt-2">Instant Payout Approvals</h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              Direct integration with local banks allows for rapid commission clearance. Track pending approvals directly from your dashboard.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/10 bg-[#070b14] pt-20 pb-10 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start gap-12">
          <div>
            <div className="text-white font-black text-2xl tracking-tighter flex items-center gap-2 mb-4">
              <span className="bg-[#EF4444] p-1.5 rounded-lg"><Network size={20} className="text-white" /></span>
              Global Sales Elite
            </div>
            <p className="text-gray-500 max-w-sm text-sm">Empowering the next generation of sales professionals with transparent, high-yield network marketing infrastructure.</p>
          </div>
          <div className="flex gap-16">
            <div>
              <h4 className="text-white font-bold mb-4">Platform</h4>
              <ul className="space-y-2 text-sm text-gray-500">
                <li><a href="#" className="hover:text-white transition-colors">How it works</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Compensation Plan</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Matrix Mechanics</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-bold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-gray-500">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
              </ul>
            </div>
          </div>
        </div>
        <div className="max-w-7xl mx-auto mt-16 pt-8 border-t border-white/5 text-center text-sm text-gray-600">
          © {new Date().getFullYear()} Global Sales Elite. All rights reserved.
        </div>
      </footer>

      {/* Login Modal */}
      <AnimatePresence>
        {showLoginModal && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center px-4">
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-black/60 backdrop-blur-sm"
              onClick={() => setShowLoginModal(false)}
            />
            <motion.div 
              initial={{ scale: 0.95, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.95, opacity: 0, y: 20 }}
              className="bg-[#1E293B]/90 backdrop-blur-xl border border-white/10 p-8 rounded-3xl shadow-2xl w-full max-w-md relative z-10"
            >
              <button 
                onClick={() => setShowLoginModal(false)}
                className="absolute top-4 right-4 w-8 h-8 flex items-center justify-center rounded-full bg-white/5 hover:bg-white/10 text-white/50 hover:text-white transition-colors"
              >
                ✕
              </button>
              
              <div className="text-center mb-8">
                <div className="mx-auto bg-[#EF4444] p-3 rounded-2xl w-max mb-4 shadow-lg">
                  <Shield size={24} className="text-white" />
                </div>
                <h2 className="text-2xl font-bold text-white mb-2">Welcome Back</h2>
                <p className="text-gray-400 text-sm">Sign in to access your network dashboard</p>
              </div>

              {errorMsg && (
                <div className="bg-red-500/20 text-red-200 border border-red-500/30 px-4 py-3 rounded-xl text-sm mb-6">
                  {errorMsg}
                </div>
              )}
              
              <form onSubmit={handleLogin} className="flex flex-col gap-4">
                <input 
                  type="email" 
                  placeholder="Email Address" 
                  value={loginEmail}
                  onChange={(e) => setLoginEmail(e.target.value)}
                  className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-[#EF4444] focus:ring-1 focus:ring-[#EF4444] transition-all"
                  required
                />
                <div className="relative">
                  <input 
                    type={showLoginPassword ? "text" : "password"} 
                    placeholder="Password" 
                    value={loginPassword}
                    onChange={(e) => setLoginPassword(e.target.value)}
                    className="w-full bg-black/20 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-[#EF4444] focus:ring-1 focus:ring-[#EF4444] transition-all pr-12"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowLoginPassword(!showLoginPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition-colors"
                  >
                    {showLoginPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
                
                <button 
                  type="submit"
                  disabled={isSigningIn}
                  className="w-full bg-[#EF4444] hover:bg-red-600 text-white font-bold py-3.5 rounded-xl shadow-[0_0_15px_rgba(239,68,68,0.3)] transition-all mt-4 disabled:opacity-50"
                >
                  {isSigningIn ? 'Authenticating...' : 'Sign In'}
                </button>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
"""

new_content = landing_page_pattern.sub(new_landing_page, content)

with open('src/App.tsx', 'w') as f:
    f.write(new_content)

