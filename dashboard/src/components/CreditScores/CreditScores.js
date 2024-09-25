// src/components/CreditScores/CreditScores.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { DataGrid } from '@mui/x-data-grid';

function CreditScores() {
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    // Fetch recent credit scoring results from the integration API
    axios.get('http://localhost:8002/credit_scoring/recent')
      .then(response => {
        setApplications(response.data.applications);
      })
      .catch(error => {
        console.error('Error fetching credit scores:', error);
      });
  }, []);

  const columns = [
    { field: 'application_id', headerName: 'Application ID', width: 150 },
    { field: 'applicant_name', headerName: 'Applicant Name', width: 200 },
    { field: 'credit_score', headerName: 'Credit Score', width: 150 },
    { field: 'date', headerName: 'Date', width: 200 },
  ];

  return (
    <div style={{ height: 400, width: '100%' }}>
      <DataGrid rows={applications} columns={columns} pageSize={5} />
    </div>
  );
}

export default CreditScores;
