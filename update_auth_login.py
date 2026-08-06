import re

with open('src/contexts/AuthContext.tsx', 'r') as f:
    content = f.read()

# Replace signInWithEmail
old_signIn = re.compile(r'const signInWithEmail = async \(email: string, password: string\) => \{.*?\};\s*const signOut', re.DOTALL)

new_signIn = '''const signInWithEmail = async (email: string, password: string) => {
    try {
      const userDoc = await sanityClient.fetch(`*[_type == "user" && email == $email][0]`, { email });
      if (!userDoc) {
        throw new Error("Account not found. Please sign up first.");
      }
        
      const isValid = bcrypt.compareSync(password, userDoc.passwordHash || '');
      if (!isValid) {
        throw new Error("Invalid email or password.");
      }
        
      // Update last login
      await sanityClient.patch(userDoc._id).set({ lastLoginAt: new Date().toISOString() }).commit();

      localStorage.setItem('userId', userDoc._id);
      setUser({ uid: userDoc._id, email: userDoc.email });
      setProfile(userDoc as UserProfile);
    } catch (err: any) {
      if (err.message === "Account not found. Please sign up first.") throw err;
      if (err.message === "Invalid email or password.") throw err;
      handleSanityError(err);
    }
  };

  const signOut'''

content = old_signIn.sub(new_signIn, content)

with open('src/contexts/AuthContext.tsx', 'w') as f:
    f.write(content)
