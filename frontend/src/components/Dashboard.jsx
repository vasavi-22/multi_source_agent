import { useAgent } from "../hooks/userAgent";
import SummaryCard from "./SummaryCard";
import ProductsTable from "./ProductsTable";
import AlertsPanel from "./AlertsPanel";
import PriceChart from "./PriceChart";
import StockChart from "./StockChart";
import ForexChart from "./ForexChart";
import Loader from "./Loader";

const Dashboard = () => {
  const {
    productData,
    financeData,
    loading,
    executeProductAgent,
    executeFinanceAgent,
  } = useAgent();

  return (
    <div style={{ padding: "20px" }}>
      <h1>🤖 Multi-Source AI Agent Dashboard</h1>

      <div style={{ marginBottom: "20px" }}>
        <button onClick={executeProductAgent}>Run Product Agent</button>

        <button onClick={executeFinanceAgent} style={{ marginLeft: "10px" }}>
          Run Finance Agent
        </button>
      </div>

      {loading && <Loader />}

      {/* PRODUCT SECTION */}
      {productData && (
        <>
          <h2>🛒 Product Intelligence</h2>
          <SummaryCard summary={productData.analysis?.products?.summary} />
          <AlertsPanel alerts={productData.alerts} />
          <ProductsTable products={productData.structured_products} />
          <PriceChart products={productData.structured_products} />
        </>
      )}

      {/* FINANCE SECTION */}
      {financeData && (
        <>
          <h2>📈 Finance Intelligence</h2>

          <SummaryCard summary={financeData.analysis?.stocks?.summary} />
          <SummaryCard summary={financeData.analysis?.forex?.summary} />

          <StockChart stocks={financeData.analysis?.stocks?.data} />
          <ForexChart forex={financeData.analysis?.forex?.data} />
        </>
      )}
    </div>
  );
};

export default Dashboard;
