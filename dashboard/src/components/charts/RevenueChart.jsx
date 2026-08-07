import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

export default function RevenueChart({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="chart-card">
      <h2>Monthly Revenue</h2>

      <Line
        data={{
          labels: data.map((r) =>
            new Date(r.order_month).toLocaleDateString("en-US", {
              month: "short",
              year: "2-digit",
            })
          ),

          datasets: [
            {
              label: "Revenue",
              data: data.map((r) => Number(r.total_revenue)),
              borderWidth: 3,
              tension: 0.4,
              fill: true,
            },
          ],
        }}
      />
    </div>
  );
}