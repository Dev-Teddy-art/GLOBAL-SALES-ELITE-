import re
import os

color_map = {
    'text-blue-400': 'text-[#0F172A] dark:text-white',
    'bg-blue-400': 'bg-[#0F172A]',
    'dark:bg-blue-900': 'dark:bg-[#0F172A]',
    'bg-blue-500/20': 'bg-[#0F172A]/20',
    'bg-blue-500': 'bg-[#0F172A]',
    'border-blue-500/30': 'border-[#0F172A]/30',
    'border-blue-500/50': 'border-[#0F172A]/50',
    'hover:border-blue-500/50': 'hover:border-[#0F172A]/50',
    'hover:bg-blue-500': 'hover:bg-[#0F172A]',
    'bg-red-500': 'bg-[#EF4444]',
    'bg-red-400': 'bg-[#EF4444]',
    'text-red-500': 'text-[#EF4444]',
    'text-red-400': 'text-[#EF4444]',
    'border-red-500': 'border-[#EF4444]',
    'hover:border-red-500/50': 'hover:border-[#EF4444]/50',
    'hover:bg-red-500': 'hover:bg-[#EF4444]',
    'from-blue-500': 'from-[#0F172A]',
    'from-[#1E3A8A]': 'from-[#0F172A]',
    'to-red-400': 'to-[#EF4444]/80',
    'to-red-500': 'to-[#EF4444]',
    'to-red-900': 'to-[#0F172A]',
    'from-red-500': 'from-[#EF4444]',
    'bg-red-100': 'bg-[#EF4444]/10',
    'bg-blue-100': 'bg-[#0F172A]/10',
    'text-blue-700': 'text-[#0F172A] dark:text-white',
    'text-red-200': 'text-[#EF4444]',
    'hover:text-red-100': 'hover:text-[#EF4444]/80',
    'border-red-100': 'border-[#EF4444]/20',
    'bg-red-50': 'bg-[#EF4444]/5',
    'bg-red-400/5': 'bg-[#EF4444]/5',
    'dark:bg-red-900/10': 'dark:bg-[#EF4444]/10',
    'bg-blue-400/5': 'bg-[#0F172A]/5',
    'dark:bg-blue-900/20': 'dark:bg-[#0F172A]/20',
    'bg-blue-400/10': 'bg-[#0F172A]/10',
    'dark:bg-[#0F172A]/30': 'dark:bg-[#0F172A]/30',
    'bg-blue-900/40': 'bg-[#0F172A]/40',
    'text-blue-300': 'text-white',
    'rgba(30,58,138,0.5)': 'rgba(15,23,42,0.5)',
    'rgba(239,68,68,0.3)': 'rgba(239,68,68,0.3)',
    'text-red-500/80': 'text-[#EF4444]/80',
    'bg-red-500/20': 'bg-[#EF4444]/20',
    'text-red-200': 'text-[#EF4444]',
    'border-red-500/30': 'border-[#EF4444]/30',
}

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            original_content = content
            for k, v in color_map.items():
                content = content.replace(k, v)
                
            if original_content != content:
                with open(path, 'w') as f:
                    f.write(content)
                print(f"Updated {path}")
