import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Replace the checkInitialAuth with just a redirect if user exists?
# Wait, if they want to create a new account, they should be able to.
# Let's just remove the `if (user) return ...` line and add a navigate effect.

old_signup_check = """  React.useEffect(() => {
    const checkInitialAuth = async () => {
      const storedUserId = localStorage.getItem('userId');
      if (storedUserId) {
         await signOut();
      }
    };
    checkInitialAuth();
  }, []);

  const [isSigningIn, setIsSigningIn] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState('');
  
  const oauthEmail = location.state?.email || '';
  const oauthDisplayName = location.state?.displayName || '';
  const [showSignUpPassword, setShowSignUpPassword] = React.useState(false);
  const [formData, setFormData] = React.useState({
    firstName: oauthDisplayName ? oauthDisplayName.split(' ')[0] : '',
    lastName: oauthDisplayName ? oauthDisplayName.split(' ').slice(1).join(' ') : '',
    email: oauthEmail || '',
    password: '',
    address: '',
    bankAccountNumber: '',
    bankAccountName: '',
    bankName: '',
    sponsorId: refCode || '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  if (loading) return <div className="min-h-screen bg-[#070b5e] flex items-center justify-center text-white">Loading...</div>;
  if (user) return <div className="min-h-screen bg-[#070b5e] flex items-center justify-center text-white">Signing out current session...</div>;"""

new_signup_check = """  React.useEffect(() => {
    // If a logged-in user visits signup directly (not right after signing up),
    // they can either be redirected to dashboard or signed out. 
    // Let's redirect them to dashboard if they are already logged in.
    if (user && !isSigningIn) {
      navigate('/dashboard', { replace: true });
    }
  }, [user, navigate, isSigningIn]);

  const [isSigningIn, setIsSigningIn] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState('');
  
  const oauthEmail = location.state?.email || '';
  const oauthDisplayName = location.state?.displayName || '';
  const [showSignUpPassword, setShowSignUpPassword] = React.useState(false);
  const [formData, setFormData] = React.useState({
    firstName: oauthDisplayName ? oauthDisplayName.split(' ')[0] : '',
    lastName: oauthDisplayName ? oauthDisplayName.split(' ').slice(1).join(' ') : '',
    email: oauthEmail || '',
    password: '',
    address: '',
    bankAccountNumber: '',
    bankAccountName: '',
    bankName: '',
    sponsorId: refCode || '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  if (loading) return <div className="min-h-screen bg-[#070b5e] flex items-center justify-center text-white">Loading...</div>;"""

content = content.replace(old_signup_check, new_signup_check)

with open('src/App.tsx', 'w') as f:
    f.write(content)
