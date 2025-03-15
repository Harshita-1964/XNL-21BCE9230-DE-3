import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [fraudData, setFraudData] = useState([]);
  const [fraudTrends, setFraudTrends] = useState([]);
  
  // Fetch fraud data from backend API
  useEffect(() => {
    axios.get('/api/fraud_data')
      .then(response => setFraudData(response.data))
      .catch(error => console.error("Error fetching fraud data:", error));

    axios.get('/api/fraud_trends')
      .then(response => setFraudTrends(response.data))
      .catch(error => console.error("Error fetching fraud trends:", error));
  }, []);

  return (
    <div className="App">
      <h1>Fraud Analytics Dashboard</h1>
      <div>
        <h2>Fraud Data</h2>
        <table>
          <thead>
            <tr>
              <th>Transaction ID</th>
              <th>Amount</th>
              <th>Fraud Score</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {fraudData.map((fraud, index) => (
              <tr key={index}>
                <td>{fraud.transaction_id}</td>
                <td>{fraud.amount}</td>
                <td>{fraud.fraud_score}</td>
                <td>{fraud.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div>
        <h2>Fraud Trends</h2>
        <ul>
          {fraudTrends.map((trend, index) => (
            <li key={index}>{trend.date}: {trend.fraud_cases_count} cases</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
