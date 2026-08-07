import { useEffect, useState } from "react";
import api from "../../api/api";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

export default function ProductCategoryChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    api
      .get("/inventory/categories/revenue")
      .then((res) => setData(res.data))
      .catch(console.error);
  }, []);

  return (
    <div className="chart-card">
      <h2>Revenue by Product Category</h2>

      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={data}>
          <CartesianGrid stroke="#444" />

          <XAxis dataKey="category" />

          <YAxis />

          <Tooltip
            formatter={(value) => [
              `₹ ${Number(value).toLocaleString()}`,
              "Revenue",
            ]}
          />

          <Bar
            dataKey="revenue"
            fill="#8b5cf6"
            radius={[6, 6, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}