import { useEffect, useState } from "react";
import axios from "axios";

import {
  BarChart,
  Bar,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts";

export default function SalesRegionChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/sales/revenue/monthly")
      .then((res) => {
        const grouped = {};

        res.data.forEach((row) => {
          if (!grouped[row.region]) {
            grouped[row.region] = 0;
          }

          grouped[row.region] += Number(row.total_revenue);
        });

        const chartData = Object.keys(grouped).map((region) => ({
          region,
          revenue: grouped[region],
        }));

        setData(chartData);
      })
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="chart-card">
      <h2>Revenue by Region</h2>

      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={data}>
          <CartesianGrid stroke="#374151" />

          <XAxis dataKey="region" />

          <YAxis
            tickFormatter={(value) => value.toLocaleString()}
          />

          <Tooltip
            formatter={(value) => [
              `₹ ${Number(value).toLocaleString()}`,
              "Revenue",
            ]}
          />

          <Bar
            dataKey="revenue"
            fill="#4f8cff"
            radius={[8, 8, 0, 0]}
            animationDuration={1000}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}