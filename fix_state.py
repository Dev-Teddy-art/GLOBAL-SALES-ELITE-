import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

content = content.replace("  const [salesLoading, setSalesLoading] = useState(true);", "  const [salesLoading, setSalesLoading] = useState(true);\n  const [editingUser, setEditingUser] = useState<any>(null);\n  const [editForm, setEditForm] = useState<any>({});")

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
