import os
import re

directories = ['src']

color_map = {
    '#e03126': '#EF4444',
    '#070b5e': '#0F172A',
    '#0a0f82': '#0F172A',
    '#1E3A8A': '#0F172A',
    'blue-900': '[#0F172A]',
    'blue-800': '[#0F172A]',
    'red-600': 'red-500',
    'red-700': 'red-500',
    'bg-[#0F172A]/10': 'bg-gray-100 dark:bg-[#0F172A]',
    'text-[#0F172A]': 'text-[#0F172A] dark:text-white',
    # Replace blue-400, blue-500 with #0F172A or #EF4444?
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
