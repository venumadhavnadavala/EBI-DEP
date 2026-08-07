import { useEffect, useState } from "react";
import api from "../api/api";

import RevenueChart from "../components/charts/RevenueChart";
import SalesRegionChart from "../components/charts/SalesRegionChart";
import CustomerTable from "../components/tables/CustomerTable";
import SalespersonTable from "../components/tables/SalespersonTable";
import AIInsights from "../components/dashboard/AIInsights";

export default function Sales() {
  const [revenueData, setRevenueData] = useState([]);

  useEffect(() => {
    api
      .get("/sales/revenue/monthly")
      .then((res) => setRevenueData(res.data))
      .catch(console.error);
  }, []);

  return (
    <div className="dashboard">

      <h1>Sales Analytics</h1>

      <RevenueChart data={revenueData} />

      <SalesRegionChart />

      <CustomerTable />

      <SalespersonTable />

      <AIInsights />

    </div>
  );
}