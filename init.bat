@echo off

:: Start the fraud detection API server
echo Starting Fraud Detection API on port 8000...
cd fraud_detection
start cmd /k "uvicorn main:app --reload --port 8000"
timeout /T 5

:: Start the credit score API server
echo Starting Credit Scoring API on port 8001...
cd ../credit_scoring
start cmd /k "uvicorn main:app --reload --port 8001"
timeout /T 5

:: Start the main API server
echo Starting Integration API on port 8002...
cd ../integration
start cmd /k "uvicorn main:app --reload --port 8002"

:: Start the main API server
echo Starting Credit Application Simulator API on port 8003...
cd ../credit_scoring
start cmd /k "uvicorn credit_application_simulator_api:app --reload --port 8003"

:: Start the main API server
echo Starting Transaction Simulator API on port 8003...
cd ../fraud_detection
start cmd /k "uvicorn transaction_simulator_api:app --reload --port 8004"

:: Start Dashboard
echo Starting Dashboard with npm...
cd ../dashboard
start cmd /k "npm run start"

:: Keep the window open
pause
