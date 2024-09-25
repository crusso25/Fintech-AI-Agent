import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

function FraudAlerts() {
  const [transactions, setTransactions] = useState([]);

  // Fetch recent fraudulent transactions
  useEffect(() => {
    console.log("requesting...");
    axios.get('http://localhost:8002/fraud_detection/recent')
      .then(response => {
        setTransactions(response.data.transactions);
      })
      .catch(error => {
        console.error('Error fetching transactions:', error);
      });
  }, []);

  // Log the transactions after they have been updated
  useEffect(() => {
    if (transactions.length > 0) {
      console.log("Updated Transactions: ", transactions);
    }
  }, [transactions]); // This useEffect runs whenever 'transactions' changes

  return (
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
  );
}

export default FraudAlerts;
