import re

with open('src/components/AdminConsolePage.tsx', 'r') as f:
    content = f.read()

# 1. Add Sales State to AdminConsolePage
new_state = """  const [users, setUsers] = useState<(UserProfile & { id: string })[]>([]);
  const [sales, setSales] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [salesLoading, setSalesLoading] = useState(true);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const data = await sanityClient.fetch(`*[_type == "user"]`);
        setUsers(data.map((u: any) => ({ ...u, id: u._id })));
      } catch (err) {
        console.error("Error fetching users:", err);
      } finally {
        setLoading(false);
      }
    };
    
    const fetchSales = async () => {
      if (!profile) return;
      try {
        const res = await fetch(`/api/admin/sales?adminId=${profile._id || profile.id}`);
        if (res.ok) {
          const data = await res.json();
          setSales(data);
        }
      } catch (err) {
        console.error("Error fetching sales", err);
      } finally {
        setSalesLoading(false);
      }
    };

    fetchUsers();
    fetchSales();
  }, [profile]);

  const handleProcessSale = async (saleId: string, status: 'approved' | 'rejected') => {
    try {
      const res = await fetch('/api/admin/sales/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ adminId: profile?._id || profile?.id, saleId, status })
      });
      if (res.ok) {
        setSales(sales.map(s => s._id === saleId ? { ...s, status } : s));
      }
    } catch (e) {
      console.error(e);
    }
  };"""

old_state = """  const [users, setUsers] = useState<(UserProfile & { id: string })[]>([]);
  const [loading, setLoading] = useState(true);

  const [editingUser, setEditingUser] = useState<any>(null);
  const [editForm, setEditForm] = useState<any>({});


  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const data = await sanityClient.fetch(`*[_type == "user"]`);
        setUsers(data.map((u: any) => ({ ...u, id: u._id })));
      } catch (err) {
        console.error("Error fetching users:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchUsers();
  }, []);"""

content = content.replace(old_state, new_state)

# 2. Update SalesApprovals to just accept props
old_sales_approvals = """function SalesApprovals({ users }: { users: any[] }) {
  const { profile } = useAuth();
  const [sales, setSales] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSales = async () => {
      if (!profile) return;
      try {
        const res = await fetch(`/api/admin/sales?adminId=${profile._id || profile.id}`);
        if (res.ok) {
          const data = await res.json();
          setSales(data);
        }
      } catch (err) {
        console.error("Error fetching sales", err);
      } finally {
        setLoading(false);
      }
    };
    fetchSales();
  }, [profile]);

  const handleProcess = async (saleId: string, status: 'approved' | 'rejected') => {
    try {
      const res = await fetch('/api/admin/sales/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ adminId: profile?._id || profile?.id, saleId, status })
      });
      if (res.ok) {
        setSales(sales.filter(w => w._id !== saleId));
      }
    } catch (e) {
      console.error(e);
    }
  };"""

new_sales_approvals = """function SalesApprovals({ sales, loading, onProcess }: { sales: any[], loading: boolean, onProcess: (id: string, status: 'approved' | 'rejected') => void }) {
  const pendingSales = sales.filter(s => s.status === 'pending');
  const handleProcess = onProcess;
"""

content = content.replace(old_sales_approvals, new_sales_approvals)

# 3. Update the SalesApprovals render to map pendingSales
content = content.replace("sales.length", "pendingSales.length")
content = content.replace("sales.map((w)", "pendingSales.map((w)")

# 4. Inject SalesHistoryTable where SalesApprovals is rendered
# Let's find <SalesApprovals users={users} />
content = content.replace("<SalesApprovals users={users} />", "<SalesApprovals sales={sales} loading={salesLoading} onProcess={handleProcessSale} />")

with open('src/components/AdminConsolePage.tsx', 'w') as f:
    f.write(content)
