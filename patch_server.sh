sed -i '/app.post('"'"'\/api\/admin\/sales\/process'"'"'/i \
  app.post("/api/admin/sales/delete", async (req, res) => {\
    try {\
      const { adminId, saleId } = req.body;\
      const admin = await sanityClient.fetch(`*[_type == "user" && _id == $id][0]`, { id: adminId });\
      if (!admin || (admin.role !== "admin" && !admin.isAdmin)) {\
        return res.status(403).json({ error: "Unauthorized" });\
      }\
      await sanityClient.delete(saleId);\
      res.json({ success: true });\
    } catch (err: any) {\
      res.status(500).json({ error: err.message });\
    }\
  });\
' server.ts
