# SellScaleHood Financial App

SellScaleHood is a simple stock trading simulation application built with a Flask backend and a React frontend. It allows users to search for stocks, view their details, and simulate buying and selling stocks.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.7+
- Node.js 12+
- npm (usually comes with Node.js)

## Backend Setup

1. Clone the repository (if you haven't already):

   ```
   git clone <repository-url>
   cd sellscalehood
   ```

2. Navigate to the backend directory:

   ```
   cd backend
   ```

3. Create a virtual environment:

   ```
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

6. Run the Flask application:
   ```
   python app.py
   ```

The backend should now be running on `http://localhost:5000`.

## Frontend Setup

1. Open a new terminal window and navigate to the frontend directory:

   ```
   cd frontend
   ```

2. Install the required npm packages:

   ```
   npm install
   ```

3. Start the React development server:
   ```
   npm start
   ```

The frontend should now be running on `http://localhost:3000`.

## Using the Application

1. Open your web browser and go to `http://localhost:3000`.
2. Use the search bar to look up stock symbols (e.g., AAPL for Apple Inc.).
3. View the stock details, including current price and price change.
4. Enter a quantity and use the "Buy" or "Sell" buttons to simulate trades.
5. View your portfolio to see your current holdings.
