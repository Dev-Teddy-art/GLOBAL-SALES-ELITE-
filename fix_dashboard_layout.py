import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# Update icons
old_imports = "import { LogOut, Copy, Users, Network, Link as LinkIcon, Share2, Crown, Shield, Calculator, BarChart as BarChartIcon, Bell, DollarSign } from 'lucide-react';"
new_imports = "import { LogOut, Copy, Users, Network, Link as LinkIcon, Share2, Crown, Shield, Calculator, BarChart as BarChartIcon, Bell, DollarSign, Wallet, Target, Award, TrendingUp, Waypoints, BadgeDollar } from 'lucide-react';"
content = content.replace(old_imports, new_imports)

# Fix wrapper
old_wrapper = """  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#020617] text-gray-900 dark:text-gray-200 font-sans relative overflow-hidden">
      {/* Background Ambience */}"""
new_wrapper = """  return (
    <div className="w-full bg-gray-50 dark:bg-[#020617] text-gray-900 dark:text-gray-200 font-sans relative">
      {/* Background Ambience */}"""
content = content.replace(old_wrapper, new_wrapper)

# Update SalesLogger icon
content = content.replace("<DollarSign size={24} />", "<BadgeDollar size={24} />")

# Update Stat Cards icons
content = content.replace("<DollarSign className=", "<Wallet className=")
content = content.replace("<Crown className=", "<Award className=")
content = content.replace("<Users className=", "<Target className=")
content = content.replace("<BarChartIcon className=", "<TrendingUp className=")

# Downline Tree
content = content.replace("<Network className=\"text-[#0F172A]", "<Waypoints className=\"text-[#0F172A]")

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
