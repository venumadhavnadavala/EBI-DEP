import { useEffect, useState } from "react";
import api from "../../api/api";

export default function ReturnAnalysisTable() {
  const [rows, setRows] = useState([]);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    api
      .get("/inventory/returns/analysis")
      .then((res) => setRows(res.data))
      .catch(console.error);
  }, []);

  const visibleRows = showAll ? rows : rows.slice(0, 10);

  return (
    <div className="table-card">
      <h2>Return Analysis</h2>

      <table className="table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Reason</th>
            <th>Returned</th>
            <th>Sold</th>
            <th>Return Rate</th>
          </tr>
        </thead>

        <tbody>
          {visibleRows.map((item) => (
            <tr key={`${item.product_id}-${item.reason}`}>
              <td>{item.product_name}</td>

              <td>{item.reason}</td>

              <td>{item.units_returned}</td>

              <td>{item.units_sold}</td>

              <td
                style={{
                  color:
                    item.return_rate > 0.05
                      ? "#ef4444"
                      : "#22c55e",
                  fontWeight: "600",
                }}
              >
                {(item.return_rate * 100).toFixed(2)}%
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