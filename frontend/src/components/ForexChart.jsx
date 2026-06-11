import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

const ForexChart = ({ forex }) => {
  if (!forex) return null;

  return (
    <div style={{ marginTop: "20px" }}>
      <h3>💱 Forex Trend</h3>
      <LineChart width={700} height={300} data={forex}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="rate" />
      </LineChart>
    </div>
  );
};

export default ForexChart;
