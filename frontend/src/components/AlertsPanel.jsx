const AlertsPanel = ({ alerts }) => {
  if (!alerts || alerts.length === 0) {
    return <p>✅ No alerts triggered</p>;
  }

  return (
    <div>
      <h3>Alerts</h3>
      {alerts.map((alert, index) => (
        <p key={index}>
          {alert.name} below threshold (£{alert.price})
        </p>
      ))}
    </div>
  );
};

export default AlertsPanel;
