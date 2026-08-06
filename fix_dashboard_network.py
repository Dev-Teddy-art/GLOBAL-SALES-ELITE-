import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# Replace from {false ? ( to the end of the block
start_idx = content.find("{false ? (")
end_idx = content.find("        </div>\n        <CommissionCalculator")

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + content[end_idx:]

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
