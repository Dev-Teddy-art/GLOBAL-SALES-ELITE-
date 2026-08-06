import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

# Replace wrapper
old_wrapper = """  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#020617] text-gray-900 dark:text-gray-200 font-sans relative overflow-hidden">
      {/* Background Ambience */}"""
new_wrapper = """  return (
    <div className="w-full bg-gray-50 dark:bg-[#020617] text-gray-900 dark:text-gray-200 font-sans relative pb-12">
      {/* Background Ambience */}"""
content = content.replace(old_wrapper, new_wrapper)

# Update imports
old_imports = "import { Shield, ChevronLeft, ChevronDown, ChevronRight, CheckCircle, DollarSign, Activity, Users, Search, AlertCircle, LayoutDashboard, Database, Link as LinkIcon, Network } from 'lucide-react';"
new_imports = "import { Shield, ChevronLeft, ChevronDown, ChevronRight, CheckCircle, DollarSign, Activity, Users, Search, AlertCircle, LayoutDashboard, Database, Link as LinkIcon, Network, Crown, Landmark, History, Terminal, UserCheck, ScrollText, Waypoints } from 'lucide-react';"
content = content.replace(old_imports, new_imports)

# Replace Icons
# Visual Binary Inspector
content = content.replace("<Network className=\"text-[#EF4444]", "<Waypoints className=\"text-[#EF4444]")
# Admin Portal header
content = content.replace("<Shield className=\"text-[#EF4444]\" /> GSE Admin Portal", "<Crown className=\"text-[#EF4444]\" /> GSE Admin Portal")
# Full Sales History
content = content.replace("<Database className=", "<History className=")
# Sales & Commission Requests
content = content.replace("<DollarSign className=\"text-[#0F172A]", "<Landmark className=\"text-[#0F172A]")
content = content.replace("<DollarSign size={20} />", "<Landmark size={20} />")
# System Logs
content = content.replace("<Activity className=\"text-[#0F172A] dark:text-white\" size={20} />\n        System Logs", "<Terminal className=\"text-[#0F172A] dark:text-white\" size={20} />\n        System Logs")

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
