import { useEffect, useState } from "react";
import api from "../../api/api";

export default function ProductProfitTable() {
  const [products, setProducts] = useState([]);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    api
      .get("/inventory/profitability/top?limit=100")
      .then((res) => setProducts(res.data))
      .catch(console.error);
  }, []);

  const visibleProducts = showAll ? products : products.slice(0, 10);

  return (
    <div className="table-card">
      <h2>Top Profitable Products</h2>

      <table className="table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Category</th>
            <th>Gross Margin</th>
            <th>Units Sold</th>
            <th>Estimated Profit</th>
          </tr>
        </thead>

        <tbody>
          {visibleProducts.map((item) => (
            <tr key={item.product_id}>
              <td>{item.product_name}</td>

              <td>{item.category}</td>

              <td style={{ color: "#2ECC71", fontWeight: 600 }}>
                {Number(item.gross_margin_pct).toFixed(1)}%
              </td>

              <td>{item.net_units_sold}</td>

              <td>
                ₹{" "}
                {Number(item.estimated_net_profit).toLocaleString("en-IN", {
                  maximumFractionDigits: 2,
                })}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {products.length > 10 && (
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