import { useEffect, useState } from "react";
import axios from "axios";

export default function SalespersonTable() {
  const [employees, setEmployees] = useState([]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/sales/employees/performance")
      .then((res) => setEmployees(res.data))
      .catch(console.error);
  }, []);

  return (
    <div className="table-card">
      <h2>Salesperson Performance</h2>

      <table className="dashboard-table">
        <thead>
          <tr>
            <th>Employee</th>
            <th>Region</th>
            <th>Orders</th>
            <th>Revenue</th>
            <th>Average Order</th>
          </tr>
        </thead>

        <tbody>
  {employees.map((emp) => (
    <tr key={emp.employee_id}>
      <td>{emp.employee_name}</td>

      <td>{emp.region}</td>

      <td>{emp.orders_closed}</td>

      <td>
        ₹ {Number(emp.revenue_generated).toLocaleString("en-IN")}
      </td>

      <td>
        ₹{" "}
        {(
          Number(emp.revenue_generated) /
          Number(emp.orders_closed)
        ).toFixed(2)}
      </td>
    </tr>
  ))}
</tbody>
      </table>
    </div>
  );
}