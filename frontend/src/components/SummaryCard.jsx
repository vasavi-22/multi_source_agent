import "./SummaryCard.css";

const SummaryCard = ({ summary }) => {
  if (!summary) return null;

  return (
    <div className="summary-card">
      <div className="summary-content">
        {summary.split("\n").map((line, index) => (
          <p key={index}>{line}</p>
        ))}
      </div>
    </div>
  );
};

export default SummaryCard;
