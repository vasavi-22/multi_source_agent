import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const PriceChart = ({ products }) => {
  const data = products?.map((p) => p.product_node);

  return (
    <div>
      <h3>Price Comparison</h3>
      <BarChart width={600} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="price" />
      </BarChart>
    </div>
  );
};

export default PriceChart;
