import re
import os

color_map = {
    'from-blue-50': 'from-[#0F172A]/5 dark:from-transparent',
    'dark:bg-red-900': 'dark:bg-[#EF4444]',
    'bg-red-900/40': 'bg-[#EF4444]/40',
    'text-red-300': 'text-[#EF4444]',
    'text-red-100': 'text-white',
    'to-[#0F172A]': 'to-[#0F172A]', # leave alone or fix
    'from-[#EF4444] to-[#0F172A]': 'from-[#EF4444] to-[#EF4444]',
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
