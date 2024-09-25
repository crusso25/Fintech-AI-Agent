// src/components/Navbar/Navbar.js

import React from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6">
          FinAI Dashboard
        </Typography>
        <Button color="inherit" component={Link} to="/fraud-alerts">Fraud Alerts</Button>
        <Button color="inherit" component={Link} to="/credit-scores">Credit Scores</Button>
        <Button color="inherit" component={Link} to="/system-metrics">System Metrics</Button>
        <Button color="inherit" component={Link} to="/logs">Logs Viewer</Button>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
