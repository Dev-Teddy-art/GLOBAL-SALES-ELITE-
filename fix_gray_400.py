import re
import glob

def clean_classes(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Find text-gray-400 that isn't preceded by dark:
    content = re.sub(r'(?<!dark:)text-gray-400', 'text-gray-500 dark:text-gray-400', content)
    # Fix the double dark:text-gray-400 that might have been created
    content = re.sub(r'dark:text-gray-500 dark:text-gray-400', 'dark:text-gray-400', content)
    
    with open(file_path, 'w') as f:
        f.write(content)

for p in glob.glob('src/**/*.tsx', recursive=True):
    clean_classes(p)

