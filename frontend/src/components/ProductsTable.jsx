const ProductsTable = ({ products }) => {
  return (
    <table border="1">
      <thead>
        <tr>
          <th>Name</th>
          <th>Price</th>
          <th>Store</th>
        </tr>
      </thead>
      <tbody>
        {products?.map((p, index) => (
          <tr key={index}>
            <td>{p.product_node.name}</td>
            <td>£{p.product_node.price}</td>
            <td>{p.product_node.store}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ProductsTable;
