import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField } from '@mui/material';

function CreditScores() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isPolling, setIsPolling] = useState(false); 
  const pollingInterval = useRef(null);
  const [open, setOpen] = useState(false);
  const [formData, setFormData] = useState({
    person_age: '',
    person_income: '',
    person_emp_length: '',
    loan_amnt: '',
    loan_int_rate: '',
    loan_percent_income: '',
    cb_person_cred_hist_length: '',
    person_home_ownership: '',
    loan_intent: '',
    loan_grade: ''
  });
  const [creditScore, setCreditScore] = useState(null);
  const [error, setError] = useState(null);

  const fetchApplications = () => {
    axios.get('http://localhost:8002/credit_scoring/recent')
      .then(response => {
        setApplications(response.data.applications);
      })
      .catch(error => {
        console.error('Error fetching credit applications:', error);
      });
  };

  const startPolling = () => {
    setIsPolling(true);
    pollingInterval.current = setInterval(() => {
      console.log("Polling for new credit applications...");
      fetchApplications();
    }, 5000); 
  };

  const stopPolling = () => {
    setIsPolling(false);
    if (pollingInterval.current) {
      clearInterval(pollingInterval.current);
    }
  };

  
  const startSimulation = () => {
    setLoading(true);
    axios.post('http://localhost:8003/simulate_credit_applications', {
      rate_per_minute: 60,
      duration_minutes: 5
    })
    .then(response => {
      console.log(response.data);
      setLoading(false);
      startPolling(); 
    })
    .catch(error => {
      console.error('Error starting simulation:', error);
      setLoading(false);
    });
  };

  const stopSimulation = () => {
    stopPolling();
    setLoading(false);
  };

  useEffect(() => {
    return () => {
      stopPolling();
    };
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = () => {
    axios.post('http://localhost:8002/credit_score', formData)
      .then(response => {
        setCreditScore(response.data.credit_score);
        setError(null);
      })
      .catch(error => {
        setError(error.response ? error.response.data.error : 'An error occurred');
      });
    setOpen(false);
  };

  return (
    <>
      <Button variant="contained" color="primary" onClick={() => setOpen(true)}>
        Get Credit Score
      </Button>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Enter Credit Application Details</DialogTitle>
        <DialogContent>
          <TextField name="person_age" label="Age" fullWidth value={formData.person_age} onChange={handleChange} />
          <TextField name="person_income" label="Income" fullWidth value={formData.person_income} onChange={handleChange} />
          <TextField name="person_emp_length" label="Employment Length" fullWidth value={formData.person_emp_length} onChange={handleChange} />
          <TextField name="loan_amnt" label="Loan Amount" fullWidth value={formData.loan_amnt} onChange={handleChange} />
          <TextField name="loan_int_rate" label="Interest Rate" fullWidth value={formData.loan_int_rate} onChange={handleChange} />
          <TextField name="loan_percent_income" label="Percent Income" fullWidth value={formData.loan_percent_income} onChange={handleChange} />
          <TextField name="cb_person_cred_hist_length" label="Credit History Length" fullWidth value={formData.cb_person_cred_hist_length} onChange={handleChange} />
          <TextField name="person_home_ownership" label="Home Ownership" fullWidth value={formData.person_home_ownership} onChange={handleChange} />
          <TextField name="loan_intent" label="Loan Intent" fullWidth value={formData.loan_intent} onChange={handleChange} />
          <TextField name="loan_grade" label="Loan Grade" fullWidth value={formData.loan_grade} onChange={handleChange} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)} color="secondary">Cancel</Button>
          <Button onClick={handleSubmit} color="primary">Submit</Button>
        </DialogActions>
      </Dialog>

      {creditScore && <div>Credit Score: {creditScore}</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}

      <Button
        variant="contained"
        color="primary"
        onClick={startSimulation}
        disabled={loading || isPolling}
        style={{ marginRight: '10px', marginTop: '20px' }}
      >
        {loading || isPolling ? 'Simulating...' : 'Start Credit Simulation'}
      </Button>
      <Button
        variant="contained"
        color="secondary"
        onClick={stopSimulation}
        disabled={!isPolling}
        style={{ marginTop: '20px' }}
      >
        Stop Simulation
      </Button>

      <TableContainer component={Paper} style={{ marginTop: '20px' }}>
        <Table aria-label="credit applications table">
          <TableHead>
            <TableRow>
              <TableCell>Application ID</TableCell>
              <TableCell>Applicant Name</TableCell>
              <TableCell>Credit Score</TableCell>
              <TableCell>Date</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {applications.map((application) => (
              <TableRow key={application.application_id}>
                <TableCell>{application.application_id}</TableCell>
                <TableCell>{application.applicant_name}</TableCell>
                <TableCell>{application.credit_score}</TableCell>
                <TableCell>{application.date}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
}

export default CreditScores;
