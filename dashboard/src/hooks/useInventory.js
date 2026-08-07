import { useEffect, useState } from "react";
import axios from "axios";

export default function useInventory() {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/inventory/kpis/summary")
      .then((res) => setSummary(res.data))
      .catch(console.error);
  }, []);

  return summary;
}