import { useEffect, useState } from "react";
import axios from "axios";

export default function CustomerTable() {
  const [customers, setCustomers] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/sales/customers/top?limit=10")
      .then((res) => setCustomers(res.data))
      .catch(console.error);
  }, []);

  return (
    <div className="table-card">
      <h2>Top Customers</h2>

      <table className="dashboard-table">
        <thead>
          <tr>
            <th>Customer</th>
            <th>Region</th>
            <th>Segment</th>
            <th>Orders</th>
            <th>Lifetime Value</th>
          </tr>
        </thead>

        <tbody>
          {customers.map((customer) => (
            <tr key={customer.customer_id}>
              <td>{customer.customer_name}</td>

              <td>{customer.region}</td>

              <td>{customer.segment}</td>

              <td>{customer.total_orders}</td>

              <td>
                ₹{" "}
                {Number(customer.lifetime_value).toLocaleString(
                  undefined,
                  {
                    maximumFractionDigits: 2,
                  }
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}