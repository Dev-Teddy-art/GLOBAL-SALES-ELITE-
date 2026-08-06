import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_route = """function AdminRoute({ children }: { children: React.ReactNode }) {
  const { user, profile, loading } = useAuth();
  if (loading) return <div className="min-h-screen flex items-center justify-center bg-gray-50 text-[#070b5e] font-bold text-xl">Loading...</div>;
  if (!user || !profile || (profile.role !== 'admin' && !profile.isAdmin)) return <Navigate to="/dashboard" replace />;
  return <>{children}</>;
}"""

new_route = """function AdminRoute({ children }: { children: React.ReactNode }) {
  const { user, profile, loading } = useAuth();
  if (loading) return <div className="min-h-screen flex items-center justify-center bg-gray-50 text-[#070b5e] font-bold text-xl">Loading...</div>;
  if (!user) return <Navigate to="/" replace />;
  if (!profile || (profile.role !== 'admin' && !profile.isAdmin)) return <Navigate to="/dashboard" replace />;
  return <>{children}</>;
}"""

content = content.replace(old_route, new_route)

with open('src/App.tsx', 'w') as f:
    f.write(content)
