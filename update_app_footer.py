import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Add import
if 'import { Footer } from' not in content:
    content = content.replace("import { Dashboard } from './components/Dashboard';", "import { Dashboard } from './components/Dashboard';\nimport { Footer } from './components/Footer';")

# Add Footer under Routes
old_router = """        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/signup" element={<SignUpPage />} />
          <Route path="/dashboard" element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          } />
          <Route path="/admin" element={
            <AdminRoute>
              <AdminConsolePage />
            </AdminRoute>
          } />
        </Routes>"""
new_router = """        <div className="flex flex-col min-h-screen">
          <div className="flex-1">
            <Routes>
              <Route path="/" element={<LandingPage />} />
              <Route path="/signup" element={<SignUpPage />} />
              <Route path="/dashboard" element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              } />
              <Route path="/admin" element={
                <AdminRoute>
                  <AdminConsolePage />
                </AdminRoute>
              } />
            </Routes>
          </div>
          <Footer />
        </div>"""
content = content.replace(old_router, new_router)

with open('src/App.tsx', 'w') as f:
    f.write(content)
