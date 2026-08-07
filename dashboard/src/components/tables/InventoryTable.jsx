import { useEffect, useState } from "react";
import api from "../../api/api";

export default function InventoryTable() {
  const [rows, setRows] = useState([]);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    api
      .get("/inventory/products/status")
      .then((res) => setRows(res.data))
      .catch(console.error);
  }, []);

  const visibleRows = showAll ? rows : rows.slice(0, 10);

  return (
    <div className="table-card">
      <h2>Inventory Status</h2>

      <table className="table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Category</th>
            <th>Stock</th>
            <th>Threshold</th>
            <th>Days Left</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {visibleRows.map((item, index) => (
            <tr key={index}>
              <td>{item.product_name}</td>
              <td>{item.category}</td>
              <td>{item.stock_on_hand}</td>
              <td>{item.reorder_threshold}</td>
              <td>{Number(item.days_of_stock_remaining).toFixed(1)}</td>

              <td
                style={{
                  color: item.needs_reorder ? "#ef4444" : "#22c55e",
                  fontWeight: "bold",
                }}
              >
                {item.needs_reorder ? "Reorder" : "Healthy"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {rows.length > 10 && (
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginTop: "20px",
          }}
        >
          <button
            onClick={() => setShowAll(!showAll)}
            style={{
              background: "#4F8EF7",
              color: "#fff",
              border: "none",
              borderRadius: "8px",
              padding: "10px 20px",
              cursor: "pointer",
              fontWeight: "600",
            }}
          >
            {showAll ? "Show Less" : "Show All"}
          </button>
        </div>
      )}
    </div>
  );
}