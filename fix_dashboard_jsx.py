import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

bad_ternary = """          {profile.isAdmin || profile.role === 'admin' ? (
            
          ) : ("""

good_ternary = """          {profile.isAdmin || profile.role === 'admin' ? (
            <div className="text-gray-500 py-8 text-center bg-gray-50 rounded-xl border border-gray-100">
              <Network className="mx-auto h-8 w-8 mb-2 text-gray-400" />
              <p>Network Tree is managed in the Admin Console.</p>
              <button onClick={() => navigate('/admin')} className="mt-4 text-[#e03126] font-medium hover:underline">Go to Admin Console</button>
            </div>
          ) : ("""

content = content.replace(bad_ternary, good_ternary)

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
