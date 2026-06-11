import { useState } from "react";
import { runProductAgent, runFinanceAgent } from "../api/agentApi";

export const useAgent = () => {
  const [productData, setProductData] = useState(null);
  const [financeData, setFinanceData] = useState(null);
  const [loading, setLoading] = useState(false);

  const executeProductAgent = async () => {
    setLoading(true);
    try {
      const result = await runProductAgent();
      setProductData(result);
    } catch (error) {
      console.error("Product agent error:", error);
    } finally {
      setLoading(false);
    }
  };

  const executeFinanceAgent = async () => {
    setLoading(true);
    try {
      const result = await runFinanceAgent();
      setFinanceData(result);
    } catch (error) {
      console.error("Finance agent error:", error);
    } finally {
      setLoading(false);
    }
  };

  return {
    productData,
    financeData,
    loading,
    executeProductAgent,
    executeFinanceAgent,
  };
};
