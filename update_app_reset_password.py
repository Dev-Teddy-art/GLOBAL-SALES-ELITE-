import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

state_additions = """
  const [modalMode, setModalMode] = React.useState<'login' | 'forgot'>('login');
  const [resetEmail, setResetEmail] = React.useState('');
  const [resetPassword, setResetPassword] = React.useState('');
  const [resetSuccess, setResetSuccess] = React.useState(false);

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!resetEmail || !resetPassword) return;
    setIsSigningIn(true);
    setErrorMsg('');
    setResetSuccess(false);
    try {
      const res = await fetch('/api/auth/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: resetEmail, newPassword: resetPassword })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to reset password');
      setResetSuccess(true);
      setModalMode('login');
      setLoginEmail(resetEmail);
      setLoginPassword('');
    } catch(err: any) {
      setErrorMsg(err.message || String(err));
    } finally {
      setIsSigningIn(false);
    }
  };
"""

content = content.replace(
    "const [showLoginPassword, setShowLoginPassword] = React.useState(false);",
    "const [showLoginPassword, setShowLoginPassword] = React.useState(false);\n" + state_additions
)

# Open modal reset
content = content.replace(
    "onClick={() => setShowLoginModal(true)}",
    "onClick={() => { setShowLoginModal(true); setModalMode('login'); setResetSuccess(false); }}"
)

modal_ui_old = """              <div className="text-center mb-8">
                <div className="mx-auto bg-[#EF4444] p-3 rounded-2xl w-max mb-4 shadow-lg">
                  <Shield size={24} className="text-gray-900 dark:text-white" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Welcome Back</h2>
                <p className="text-gray-600 dark:text-gray-400 text-sm">Sign in to access your network dashboard</p>
              </div>

              {errorMsg && (
                <div className="bg-[#EF4444]/20 text-[#EF4444] border border-[#EF4444]/30 px-4 py-3 rounded-xl text-sm mb-6">
                  {errorMsg}
                </div>
              )}
              
              <form onSubmit={handleLogin} className="flex flex-col gap-4">
                <input 
                  type="email" 
                  placeholder="Email Address" 
                  value={loginEmail}
                  onChange={(e) => setLoginEmail(e.target.value)}
                  className="w-full bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:border-[#EF4444] focus:ring-1 focus:ring-[#EF4444] transition-all"
                  required
                />
                <div className="relative">
                  <input 
                    type={showLoginPassword ? "text" : "password"} 
                    placeholder="Password" 
                    value={loginPassword}
                    onChange={(e) => setLoginPassword(e.target.value)}
                    className="w-full bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:border-[#EF4444] focus:ring-1 focus:ring-[#EF4444] transition-all pr-12"
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
                  className="w-full bg-[#EF4444] hover:bg-[#EF4444] text-white font-bold py-3.5 rounded-xl shadow-[0_0_15px_rgba(239,68,68,0.3)] transition-all mt-4 disabled:opacity-50"
                >
                  {isSigningIn ? 'Authenticating...' : 'Sign In'}
                </button>
              </form>"""

modal_ui_new = """              <div className="text-center mb-8">
                <div className="mx-auto bg-[#EF4444] p-3 rounded-2xl w-max mb-4 shadow-lg">
                  <Shield size={24} className="text-gray-900 dark:text-white" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  {modalMode === 'login' ? 'Welcome Back' : 'Reset Password'}
                </h2>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  {modalMode === 'login' ? 'Sign in to access your network dashboard' : 'Enter your email and new password to reset'}
                </p>
              </div>

              {errorMsg && (
                <div className="bg-[#EF4444]/20 text-[#EF4444] border border-[#EF4444]/30 px-4 py-3 rounded-xl text-sm mb-6">
                  {errorMsg}
                </div>
              )}
              {resetSuccess && (
                <div className="bg-green-500/20 text-green-600 dark:text-green-400 border border-green-500/30 px-4 py-3 rounded-xl text-sm mb-6">
                  Password reset successfully. Please log in.
                </div>
              )}
              
              {modalMode === 'login' ? (
                <form onSubmit={handleLogin} className="flex flex-col gap-4">
                  <input 
                    type="email" 
                    placeholder="Email Address" 
                    value={loginEmail}
                    onChange={(e) => setLoginEmail(e.target.value)}
                    className="w-full bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:border-[#EF4444] focus:ring-1 focus:ring-[#EF4444] transition-all"
                    required
                  />
                  <div className="relative">
                    <input 
                      type={showLoginPassword ? "text" : "password"} 
                      placeholder="Password" 
                      value={loginPassword}
                      onChange={(e) => setLoginPassword(e.target.value)}
                      className="w-full bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:border-[#EF4444] focus:ring-1 focus:ring-[#EF4444] transition-all pr-12"
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
                  
                  <div className="text-right">
                    <button 
                      type="button" 
                      onClick={() => { setModalMode('forgot'); setErrorMsg(''); setResetSuccess(false); }}
                      className="text-sm text-gray-500 hover:text-[#EF4444] transition-colors"
                    >
                      Forgot Password?
                    </button>
                  </div>

                  <button 
                    type="submit"
                    disabled={isSigningIn}
                    className="w-full bg-[#EF4444] hover:bg-[#EF4444] text-white font-bold py-3.5 rounded-xl shadow-[0_0_15px_rgba(239,68,68,0.3)] transition-all mt-2 disabled:opacity-50"
                  >
                    {isSigningIn ? 'Authenticating...' : 'Sign In'}
                  </button>
                </form>
              ) : (
                <form onSubmit={handleResetPassword} className="flex flex-col gap-4">
                  <input 
                    type="email" 
                    placeholder="Email Address" 
                    value={resetEmail}
                    onChange={(e) => setResetEmail(e.target.value)}
                    className="w-full bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:border-[#EF4444] focus:ring-1 focus:ring-[#EF4444] transition-all"
                    required
                  />
                  <div className="relative">
                    <input 
                      type={showLoginPassword ? "text" : "password"} 
                      placeholder="New Password" 
                      value={resetPassword}
                      onChange={(e) => setResetPassword(e.target.value)}
                      className="w-full bg-white dark:bg-black/20 border border-gray-200 dark:border-white/10 rounded-xl px-4 py-3 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:border-[#EF4444] focus:ring-1 focus:ring-[#EF4444] transition-all pr-12"
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
                    className="w-full bg-[#EF4444] hover:bg-[#EF4444] text-white font-bold py-3.5 rounded-xl shadow-[0_0_15px_rgba(239,68,68,0.3)] transition-all mt-4 disabled:opacity-50"
                  >
                    {isSigningIn ? 'Resetting...' : 'Reset Password'}
                  </button>
                  <button 
                    type="button"
                    onClick={() => { setModalMode('login'); setErrorMsg(''); }}
                    className="text-sm text-gray-500 hover:text-gray-900 dark:hover:text-white transition-colors mt-2"
                  >
                    Back to Login
                  </button>
                </form>
              )}"""

content = content.replace(modal_ui_old, modal_ui_new)

with open('src/App.tsx', 'w') as f:
    f.write(content)

