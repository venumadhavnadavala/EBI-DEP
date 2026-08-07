import { useEffect, useState } from "react";
import api from "../../api/api";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

const COLORS = ["#ef4444", "#22c55e"];

export default function InventoryChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    api.get("/inventory/health").then((res) => {
      const reorder = res.data.filter((x) => x.needs_reorder).length;
      const healthy = res.data.length - reorder;

      setData([
        {
          name: "Needs Reorder",
          value: reorder,
        },
        {
          name: "Healthy Stock",
          value: healthy,
        },
      ]);
    });
  }, []);

  return (
    <div className="chart-card">
      <h2>Inventory Health</h2>

      <ResponsiveContainer width="100%" height={350}>
        <PieChart>
          <Pie
    data={data}
    dataKey="value"
    nameKey="name"
    outerRadius={120}
    label={({ name, percent }) =>
        `${name} ${(percent * 100).toFixed(1)}%`
    }
>
    {data.map((entry, index) => (
        <Cell
            key={index}
            fill={COLORS[index]}
        />
    ))}
</Pie>

          <Tooltip
    formatter={(value, name) => [`${value} Products`, name]}
/>
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}