import { useEffect, useState } from "react";
import api from "../../api/api";

export default function AIInsights() {
  const [sales, setSales] = useState(null);
  const [inventory, setInventory] = useState(null);

  useEffect(() => {
    api.get("/insights/sales")
      .then((res) => setSales(res.data))
      .catch(console.error);

    api.get("/insights/inventory")
      .then((res) => setInventory(res.data))
      .catch(console.error);
  }, []);

  return (
    <div className="table-card">

      <h2>🤖 AI Business Insights</h2>

      <div style={{ marginTop: "20px" }}>

        <h3 style={{ color: "#4F8EF7" }}>Sales</h3>

        <ul>
          {sales?.bullets?.map((item, index) => (
            <li
              key={index}
              style={{
                color: "#ddd",
                marginBottom: "10px",
                lineHeight: 1.6,
              }}
            >
              {item}
            </li>
          ))}
        </ul>

        <p
          style={{
            color: "#ffffff",
            marginTop: "15px",
            fontStyle: "italic",
          }}
        >
          {sales?.summary}
        </p>

        <hr style={{ margin: "30px 0", borderColor: "#444" }} />

        <h3 style={{ color: "#22c55e" }}>Inventory</h3>

        <ul>
          {inventory?.bullets?.map((item, index) => (
            <li
              key={index}
              style={{
                color: "#ddd",
                marginBottom: "10px",
                lineHeight: 1.6,
              }}
            >
              {item}
            </li>
          ))}
        </ul>

        <p
          style={{
            color: "#ffffff",
            marginTop: "15px",
            fontStyle: "italic",
          }}
        >
          {inventory?.summary}
        </p>

      </div>

    </div>
  );
}