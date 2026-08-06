import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add signInWithEmail to LandingPage
content = content.replace(
    'const { user, loading, signInWithGoogle } = useAuth();',
    'const { user, loading, signInWithGoogle, signInWithEmail } = useAuth();'
)

# Update handleLogin to open a modal instead of directly signing in with Google
old_handle_login = '''  const handleLogin = async () => {
    setIsSigningIn(true);
    setErrorMsg('');
    try {
      await signInWithGoogle('', true);
    } catch (err: any) {
      if (err?.message === 'auth/user-not-found') {
        navigate('/signup', { 
          state: { 
            email: err.email || '', 
            displayName: err.displayName || '' 
          } 
        });
      } else if (err?.code === 'auth/popup-closed-by-user') {
        setErrorMsg('Sign-in was cancelled. Please try again.');
      } else {
        setErrorMsg('An error occurred during sign in. Please try again.');
      }
    } finally {
      setIsSigningIn(false);
    }
  };'''

new_handle_login = '''  const [showLoginModal, setShowLoginModal] = React.useState(false);
  const [loginEmail, setLoginEmail] = React.useState('');
  const [loginPassword, setLoginPassword] = React.useState('');

  const handleLogin = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!loginEmail || !loginPassword) return;
    
    setIsSigningIn(true);
    setErrorMsg('');
    try {
      await signInWithEmail(loginEmail, loginPassword);
    } catch (err: any) {
      setErrorMsg(err.message || 'Invalid email or password.');
    } finally {
      setIsSigningIn(false);
    }
  };

  const handleGoogleLogin = async () => {
    setIsSigningIn(true);
    setErrorMsg('');
    try {
      await signInWithGoogle('', true);
    } catch (err: any) {
      if (err?.message === 'auth/user-not-found') {
        navigate('/signup', { 
          state: { 
            email: err.email || '', 
            displayName: err.displayName || '' 
          } 
        });
      } else if (err?.code === 'auth/popup-closed-by-user') {
        setErrorMsg('Sign-in was cancelled. Please try again.');
      } else {
        setErrorMsg('An error occurred during sign in. Please try again.');
      }
    } finally {
      setIsSigningIn(false);
    }
  };'''

content = content.replace(old_handle_login, new_handle_login)

# Replace the Login button click handler
content = content.replace(
    '''            <button 
              onClick={handleLogin}
              disabled={isSigningIn}
              className="text-white hover:text-white/80 font-medium transition-colors text-sm"
            >
              {isSigningIn ? '...' : 'Login'}
            </button>''',
    '''            <button 
              onClick={() => setShowLoginModal(true)}
              className="text-white hover:text-white/80 font-medium transition-colors text-sm"
            >
              Login
            </button>'''
)

# Insert the modal HTML just before the closing </div> of LandingPage
modal_html = '''        {showLoginModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
            <div className="bg-[#070b5e] border border-white/20 p-8 rounded-2xl w-full max-w-md shadow-2xl relative">
              <button 
                onClick={() => setShowLoginModal(false)}
                className="absolute top-4 right-4 text-white/50 hover:text-white"
              >
                ✕
              </button>
              <h2 className="text-2xl font-bold text-white mb-6 text-center">Login to Portal</h2>
              
              {errorMsg && (
                <div className="bg-red-500/20 text-red-100 border border-red-500/30 px-4 py-3 rounded-xl text-sm mb-6 text-left">
                  {errorMsg}
                </div>
              )}
              
              <form onSubmit={handleLogin} className="flex flex-col gap-4">
                <input 
                  type="email" 
                  placeholder="Email Address" 
                  value={loginEmail}
                  onChange={(e) => setLoginEmail(e.target.value)}
                  className="w-full bg-white/5 border border-white/20 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#e03126]"
                  required
                />
                <input 
                  type="password" 
                  placeholder="Password" 
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  className="w-full bg-white/5 border border-white/20 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-[#e03126]"
                  required
                />
                <button 
                  type="submit"
                  disabled={isSigningIn}
                  className="w-full bg-[#e03126] hover:bg-red-700 text-white font-bold px-6 py-3 rounded-xl transition-all disabled:opacity-50 mt-2"
                >
                  {isSigningIn ? 'Signing In...' : 'Sign In'}
                </button>
              </form>
              
              <div className="relative flex items-center justify-center mt-6 mb-6">
                <div className="border-t border-white/20 w-full"></div>
                <span className="bg-[#070b5e] px-4 text-white/50 text-sm absolute">OR</span>
              </div>
              
              <button 
                onClick={handleGoogleLogin}
                disabled={isSigningIn}
                className="w-full bg-white hover:bg-gray-100 text-gray-900 font-bold px-6 py-3 rounded-xl transition-all disabled:opacity-50 flex items-center justify-center gap-3"
              >
                <svg viewBox="0 0 24 24" width="20" height="20" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                Sign In with Google
              </button>
            </div>
          </div>
        )}
    </div>
  );
}'''

content = content.replace('    </div>\n  );\n}\n\nfunction SignUpPage()', modal_html + '\n\nfunction SignUpPage()')

with open('src/App.tsx', 'w') as f:
    f.write(content)
