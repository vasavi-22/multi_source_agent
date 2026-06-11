import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

const StockChart = ({ stocks }) => {
  if (!stocks) return null;

  return (
    <div style={{ marginTop: "20px" }}>
      <h3>📊 Stock Trend</h3>
      <LineChart width={700} height={300} data={stocks}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="close" />
      </LineChart>
    </div>
  );
};

export default StockChart;
