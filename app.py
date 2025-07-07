from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from datetime import datetime, date
from typing import Dict, Optional

app = Flask(__name__)

class CurrencyConverter:
    def __init__(self):
        self.rates_file = 'exchange_rates.json'
        self.api_url = 'https://api.exchangerate-api.com/v4/latest/USD'
        self.currencies = ['DKK', 'SEK', 'NOK']  # Danish, Swedish, Norwegian Krone
        
    def get_stored_rates(self) -> Optional[Dict]:
        """Load rates from file if they exist and are from today"""
        if not os.path.exists(self.rates_file):
            return None
            
        try:
            with open(self.rates_file, 'r') as f:
                data = json.load(f)
                
            # Check if rates are from today
            stored_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            if stored_date == date.today():
                return data
                
        except (json.JSONDecodeError, KeyError, ValueError):
            pass
            
        return None
    
    def fetch_fresh_rates(self) -> Dict:
        """Fetch new rates from API"""
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            api_data = response.json()
            
            # Extract only the currencies we need
            rates = {currency: api_data['rates'][currency] for currency in self.currencies}
            
            data = {
                'date': date.today().strftime('%Y-%m-%d'),
                'rates': rates
            }
            
            # Save to file
            with open(self.rates_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            return data
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch exchange rates: {str(e)}")
        except KeyError as e:
            raise Exception(f"Currency not found in API response: {str(e)}")
    
    def get_rates(self) -> Dict:
        """Get current exchange rates, fetching fresh ones if needed"""
        stored_rates = self.get_stored_rates()
        
        if stored_rates:
            return stored_rates
        else:
            return self.fetch_fresh_rates()
    
    def convert_currency(self, amount: float, target_currency: str) -> float:
        """Convert USD to target currency"""
        rates_data = self.get_rates()
        rate = rates_data['rates'][target_currency]
        return amount * rate

converter = CurrencyConverter()

@app.route('/')
def index():
    try:
        rates_data = converter.get_rates()
        rates = rates_data['rates']
        last_updated = rates_data['date']
        
        # Round rates to nearest 10th
        rounded_rates = {currency: round(rate, 1) for currency, rate in rates.items()}
        
        return render_template('index.html', 
                             rates=rounded_rates, 
                             last_updated=last_updated)
    except Exception as e:
        return render_template('index.html', 
                             error=str(e), 
                             rates=None, 
                             last_updated=None)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        amount = float(data.get('amount', 0))
        
        if amount <= 0:
            return jsonify({'error': 'Please enter a valid amount greater than 0'})
        
        results = {}
        for currency in converter.currencies:
            converted_amount = converter.convert_currency(amount, currency)
            results[currency] = round(converted_amount, 2)
        
        return jsonify({'success': True, 'results': results})
        
    except ValueError:
        return jsonify({'error': 'Please enter a valid number'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/convert_to_usd', methods=['POST'])
def convert_to_usd():
    try:
        data = request.get_json()
        amount = float(data.get('amount', 0))
        from_currency = data.get('from_currency', 'SEK')
        
        if amount <= 0:
            return jsonify({'error': 'Please enter a valid amount greater than 0'})
        
        if from_currency not in converter.currencies:
            return jsonify({'error': 'Invalid currency selected'})
        
        # Get the exchange rate (how many foreign currency per 1 USD)
        rates_data = converter.get_rates()
        foreign_to_usd_rate = rates_data['rates'][from_currency]
        
        # Convert to USD (divide by the rate)
        usd_amount = amount / foreign_to_usd_rate
        
        return jsonify({
            'success': True, 
            'usd_amount': round(usd_amount, 2),
            'from_currency': from_currency,
            'original_amount': amount
        })
        
    except ValueError:
        return jsonify({'error': 'Please enter a valid number'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/refresh', methods=['POST'])
def refresh_rates():
    try:
        # Force fetch fresh rates
        rates_data = converter.fetch_fresh_rates()
        rates = rates_data['rates']
        rounded_rates = {currency: round(rate, 1) for currency, rate in rates.items()}
        
        return jsonify({
            'success': True, 
            'rates': rounded_rates,
            'last_updated': rates_data['date']
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)