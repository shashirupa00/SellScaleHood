# Import necessary libraries
from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Portfolio model for database
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    ticker = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Function to check if a stock exists
def stock_exists(ticker):
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get('currentPrice') or stock.info.get('regularMarketPrice')
        return price is not None and price > 0
    except:
        return False

# Route to get stock information
@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        exists = stock_exists(ticker)
        price = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        
        return jsonify({
            'symbol': ticker.upper(),
            'name': info.get('longName', 'N/A'),
            'price': price,
            'exists': exists
        })
    except Exception as e:
        app.logger.error(f"Error fetching stock info for {ticker.upper()}: {str(e)}")
        return jsonify({
            'symbol': ticker.upper(),
            'name': 'N/A',
            'price': 0,
            'exists': False
        }), 200

# Route to buy stocks
@app.route('/api/buy', methods=['POST'])
def buy_stock():
    data = request.json
    ticker = data['ticker']
    quantity = data['quantity']
    user_id = 1  # Placeholder for user authentication

    # Check if the stock exists before buying
    if not stock_exists(ticker):
        return jsonify({'error': 'Cannot buy non-existent stock'}), 400

    # Update or create portfolio entry
    holding = Portfolio.query.filter_by(user_id=user_id, ticker=ticker).first()
    if holding:
        holding.quantity += quantity
    else:
        new_holding = Portfolio(user_id=user_id, ticker=ticker, quantity=quantity)
        db.session.add(new_holding)

    db.session.commit()
    return jsonify({'message': 'Stock purchased successfully'})

# Route to sell stocks
@app.route('/api/sell', methods=['POST'])
def sell_stock():
    data = request.json
    ticker = data['ticker']
    quantity = data['quantity']
    user_id = 1  # Placeholder for user authentication

    # Check if the stock exists before selling
    if not stock_exists(ticker):
        return jsonify({'error': 'Cannot sell non-existent stock'}), 400

    # Check if user has enough stocks to sell
    holding = Portfolio.query.filter_by(user_id=user_id, ticker=ticker).first()
    if holding and holding.quantity >= quantity:
        holding.quantity -= quantity
        if holding.quantity == 0:
            db.session.delete(holding)
        db.session.commit()
        return jsonify({'message': 'Stock sold successfully'})
    else:
        return jsonify({'error': 'Insufficient stocks to sell'}), 400

# Route to get user's portfolio
@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    try:
        user_id = 1  # Placeholder for user authentication
        portfolio = Portfolio.query.filter_by(user_id=user_id).all()
        portfolio_data = [{'ticker': item.ticker, 'quantity': item.quantity} for item in portfolio]
        return jsonify(portfolio_data)
    except Exception as e:
        app.logger.error(f"Error fetching portfolio: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching the portfolio'}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)