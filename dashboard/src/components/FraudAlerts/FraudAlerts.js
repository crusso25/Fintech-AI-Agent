import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

function FraudAlerts() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isPolling, setIsPolling] = useState(false); // To control polling
  const pollingInterval = useRef(null); // UseRef to store interval ID

  // Fetch recent fraudulent transactions
  const fetchTransactions = () => {
    axios.get('http://localhost:8002/fraud_detection/recent')
      .then(response => {
        setTransactions(response.data.transactions);
      })
      .catch(error => {
        console.error('Error fetching transactions:', error);
      });
  };

  // Polling for recent transactions every 5 seconds
  const startPolling = () => {
    setIsPolling(true);
    pollingInterval.current = setInterval(() => {
      console.log("Polling for new transactions...");
      fetchTransactions();
    }, 5000); // Poll every 5 seconds
  };

  const stopPolling = () => {
    setIsPolling(false);
    if (pollingInterval.current) {
      clearInterval(pollingInterval.current);
    }
  };

  // Log the transactions after they have been updated
  useEffect(() => {
    if (transactions.length > 0) {
      console.log("Updated Transactions: ", transactions);
    }
  }, [transactions]);

  // Function to start the transaction simulation
  const startSimulation = () => {
    setLoading(true);
    axios.post('http://localhost:8003/simulate_transactions', {
      rate_per_minute: 120,
      duration_minutes: 5
    })
    .then(response => {
      console.log(response.data);
      setLoading(false);
      startPolling(); // Start polling when simulation starts
    })
    .catch(error => {
      console.error('Error starting simulation:', error);
      setLoading(false);
    });
  };

  // Function to stop the simulation and polling
  const stopSimulation = () => {
    stopPolling();
    setLoading(false);
  };

  useEffect(() => {
    // Cleanup the interval when the component unmounts
    return () => {
      stopPolling();
    };
  }, []);

  return (
    <>
      <button
        variant="contained"
        color="primary"
        onClick={startSimulation}
        disabled={loading || isPolling}
      >
        {loading || isPolling ? 'Simulating...' : 'Start Transaction Simulation'}
      </button>
      <button
        variant="contained"
        color="secondary"
        onClick={stopSimulation}
        disabled={!isPolling}
      >
        Stop Simulation
      </button>
      <TableContainer component={Paper}>
        <Table aria-label="fraud alerts table">
          <TableHead>
            <TableRow>
              <TableCell>Transaction ID</TableCell>
              <TableCell>Amount</TableCell>
              <TableCell>Time</TableCell>
              <TableCell>Prediction</TableCell>
              <TableCell>Anomaly Score</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {transactions.map((transaction) => (
              <TableRow key={transaction.transaction_id}>
                <TableCell>{transaction.transaction_id}</TableCell>
                <TableCell>{transaction.amount}</TableCell>
                <TableCell>{transaction.time}</TableCell>
                <TableCell>{transaction.prediction}</TableCell>
                <TableCell>{transaction.anomaly_score}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
}

export default FraudAlerts;
