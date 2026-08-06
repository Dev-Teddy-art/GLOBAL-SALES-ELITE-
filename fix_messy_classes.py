import re
import glob

def clean_classes(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Clean up duplicate classes
    content = re.sub(r'text-gray-[0-9]+ dark:text-gray-[0-9]+ dark:text-gray-[0-9]+ dark:text-gray-[0-9]+', 'text-gray-600 dark:text-gray-400', content)
    content = re.sub(r'text-gray-[0-9]+ dark:text-gray-[0-9]+ dark:text-gray-[0-9]+ dark:text-white/80', 'text-gray-700 dark:text-gray-300', content)
    content = re.sub(r'text-gray-[0-9]+ dark:text-gray-[0-9]+ dark:text-white/70', 'text-gray-600 dark:text-gray-400', content)
    content = re.sub(r'dark:bg-gray-[0-9]+ dark:bg-\[#[0-9A-F]+\]', 'dark:bg-[#0F172A]', content)
    
    with open(file_path, 'w') as f:
        f.write(content)

for p in glob.glob('src/**/*.tsx', recursive=True):
    clean_classes(p)

