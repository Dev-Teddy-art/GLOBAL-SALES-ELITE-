import re

with open('src/components/Dashboard.tsx', 'r') as f:
    content = f.read()

# Update rates and comments
content = content.replace("const l1Rate = 0.05; // 5%", "const l1Rate = 0.15; // 15%")
content = content.replace("const l2Rate = 0.02; // 2%", "const l2Rate = 0.03; // 3%")

# Update UI badges
content = content.replace("5% Comm.", "15% Comm.")
content = content.replace("2% Comm.", "3% Comm.")

with open('src/components/Dashboard.tsx', 'w') as f:
    f.write(content)
