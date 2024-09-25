// src/components/SystemMetrics/SystemMetrics.js

import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import axios from 'axios';

function SystemMetrics() {
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    // Fetch system metrics from the integration API
    axios.get('http://localhost:8002/system_metrics')
      .then(response => {
        setMetrics(response.data.metrics);
      })
      .catch(error => {
        console.error('Error fetching system metrics:', error);
      });
  }, []);

  return (
    <LineChart
      width={800}
      height={400}
      data={metrics}
      margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="timestamp" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="request_rate" stroke="#8884d8" />
      <Line type="monotone" dataKey="response_time" stroke="#82ca9d" />
    </LineChart>
  );
}

export default SystemMetrics;
