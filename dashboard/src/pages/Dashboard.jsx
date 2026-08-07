import { useEffect, useState } from "react";
import api from "../api/api";
import KPICard from "../components/dashboard/KPICard";
import "../styles/dashboard.css";
import RevenueChart from "../components/charts/RevenueChart";
import SalesRegionChart from "../components/charts/SalesRegionChart";
import CustomerTable from "../components/tables/CustomerTable";
import SalespersonTable from "../components/tables/SalespersonTable";
import InventoryChart from "../components/charts/InventoryChart";
import ProductCategoryChart from "../components/charts/ProductCategoryChart";
import InventoryTable from "../components/tables/InventoryTable";
import AIInsights from "../components/dashboard/AIInsights";
import ProductProfitTable from "../components/tables/ProductProfitTable";
import ReturnAnalysisTable from "../components/tables/ReturnAnalysisTable";


function Dashboard(){

    const [sales,setSales]=useState({});
    const [inventory,setInventory]=useState({});
    const [revenueData, setRevenueData] = useState([]);

   useEffect(() => {

    api.get("/sales/kpis/summary")
        .then((res) => {
            console.log("Sales API:", res.data);
            setSales(res.data);
        })
        .catch((err) => {
            console.error("Sales Error:", err);
        });

    api.get("/inventory/kpis/summary")
        .then((res) => {
            console.log("Inventory API:", res.data);
            setInventory(res.data);
        })
        .catch((err) => {
            console.error("Inventory Error:", err);
        });
    api.get("/sales/revenue/monthly")
       .then((res) => {
        setRevenueData(res.data);
  })
  .catch(console.error);

}, []);

    return(

        <div className="dashboard">

            <h1>Executive Dashboard</h1>

            <div className="kpi-grid">

                <KPICard
                    title="Revenue"
                    value={sales.total_revenue ?? "--"}
                    color="#4F8EF7"
                />

                <KPICard
                    title="Orders"
                    value={sales.total_orders ?? "--"}
                    color="#2ECC71"
                />

                <KPICard
                    title="Avg Order"
                    value={sales.avg_order_value ?? "--"}
                    color="#F39C12"
                />

                <KPICard
                    title="Products to Reorder"
                    value={inventory.products_needing_reorder ?? "--"}
                    color="#E74C3C"
                />
                <KPICard
    title="Average Margin"
    value={
        inventory.avg_margin !== undefined
            ? `${(inventory.avg_margin * 100).toFixed(1)} %`
            : "--"
    }
    color="#2ECC71"
/>
            </div>
            <RevenueChart data={revenueData} />
            <SalesRegionChart />
            <InventoryChart />
            <ProductCategoryChart />
            <InventoryTable />
            <ProductProfitTable />
            <ReturnAnalysisTable />
            <AIInsights />
            <CustomerTable />
            <SalespersonTable />
        </div>

    );

}

export default Dashboard;