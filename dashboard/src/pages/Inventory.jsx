import InventoryChart from "../components/charts/InventoryChart";
import ProductCategoryChart from "../components/charts/ProductCategoryChart";
import InventoryTable from "../components/tables/InventoryTable";
import ProductProfitTable from "../components/tables/ProductProfitTable";
import ReturnAnalysisTable from "../components/tables/ReturnAnalysisTable";
import AIInsights from "../components/dashboard/AIInsights";

export default function Inventory() {
  return (
    <div className="dashboard">

      <h1>Inventory Analytics</h1>

      <InventoryChart />

      <ProductCategoryChart />

      <InventoryTable />

      <ProductProfitTable />

      <ReturnAnalysisTable />

      <AIInsights />

    </div>
  );
}