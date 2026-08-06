import re

with open('src/contexts/AuthContext.tsx', 'r') as f:
    content = f.read()

# Add profileImage to UserProfile
content = content.replace("  lastLoginAt?: string;\n}", "  lastLoginAt?: string;\n  profileImage?: string;\n}")

# Add updateProfile to AuthContextType
content = content.replace("  signOut: () => Promise<void>;\n}", "  signOut: () => Promise<void>;\n  updateProfile: (updates: Partial<UserProfile>) => void;\n}")

# Add updateProfile implementation
content = content.replace("  const signOut = async () => {", "  const updateProfile = (updates: Partial<UserProfile>) => {\n    setProfile(prev => prev ? { ...prev, ...updates } : null);\n  };\n\n  const signOut = async () => {")

# Provide updateProfile in value
content = content.replace("value={{ user, profile, loading, signUpWithEmail, signInWithEmail, signOut }}", "value={{ user, profile, loading, signUpWithEmail, signInWithEmail, signOut, updateProfile }}")

with open('src/contexts/AuthContext.tsx', 'w') as f:
    f.write(content)
