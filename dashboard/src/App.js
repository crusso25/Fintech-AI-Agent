// src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FraudAlerts from './components/FraudAlerts/FraudAlerts';
import CreditScores from './components/CreditScores/CreditScores';
import SystemMetrics from './components/SystemMetrics/SystemMetrics';
import LogsViewer from './components/LogsViewer/LogsViewer';
import Navbar from './components/Navbar/Navbar';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/fraud-alerts" element={<FraudAlerts />} />
        <Route path="/credit-scores" element={<CreditScores />} />
        <Route path="/system-metrics" element={<SystemMetrics />} />
        <Route path="/logs" element={<LogsViewer />} />
        <Route path="/" element={<FraudAlerts />} />
      </Routes>
    </Router>
  );
}

export default App;
