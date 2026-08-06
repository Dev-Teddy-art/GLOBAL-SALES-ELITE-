import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Replace Imports
old_imports = "import { Globe, Users, Network, LogOut, ChevronRight, ChevronDown, Copy, Check, Facebook, Twitter, Instagram, Crown, Shield, Eye, EyeOff, DollarSign, Activity } from 'lucide-react';"
new_imports = "import { Globe, Users, Network, LogOut, ChevronRight, ChevronDown, Copy, Check, Facebook, Twitter, Instagram, Crown, Shield, ShieldCheck, Eye, EyeOff, DollarSign, Activity, Waypoints, TrendingUp, Banknote } from 'lucide-react';"
content = content.replace(old_imports, new_imports)

# Line 96, 358 (Earnings Calculator & Features)
content = content.replace("<DollarSign className", "<Banknote className")
content = content.replace("<DollarSign size", "<Banknote size")

# Line 258, 342
content = content.replace("<Network className", "<Waypoints className")
content = content.replace("<Network size", "<Waypoints size")

# Line 374
content = content.replace("<Activity size", "<TrendingUp size")

# Line 529
content = content.replace("<Shield size", "<ShieldCheck size")

with open('src/App.tsx', 'w') as f:
    f.write(content)
