#!/bin/bash

# Start the fraud detection API server
echo "Starting Fraud Detection API on port 8000..."
cd fraud_detection
gnome-terminal -- bash -c "uvicorn main:app --reload --port 8000; exec bash"
sleep 5

# Start the credit score API server
echo "Starting Credit Scoring API on port 8001..."
cd ../credit_scoring
gnome-terminal -- bash -c "uvicorn main:app --reload --port 8001; exec bash"
sleep 5

# Start the main API server
echo "Starting Integration API on port 8002..."
cd ../integration
gnome-terminal -- bash -c "uvicorn main:app --reload --port 8002; exec bash"
sleep 5

# Start the Credit Application Simulator API server
echo "Starting Credit Application Simulator API on port 8003..."
cd ../credit_scoring
gnome-terminal -- bash -c "uvicorn credit_application_simulator_api:app --reload --port 8003; exec bash"
sleep 5

# Start the Transaction Simulator API server
echo "Starting Transaction Simulator API on port 8004..."
cd ../fraud_detection
gnome-terminal -- bash -c "uvicorn transaction_simulator_api:app --reload --port 8004; exec bash"
sleep 5

# Start the Dashboard
echo "Starting Dashboard with npm..."
cd ../dashboard
gnome-terminal -- bash -c "npm run start; exec bash"
