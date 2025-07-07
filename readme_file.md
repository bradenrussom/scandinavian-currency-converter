# USD to Scandinavian Currencies Converter

A simple web application that converts US Dollars to Swedish Krona (SEK), Danish Krone (DKK), and Norwegian Krone (NOK) with real-time exchange rates.

## Features

- 📊 **Daily Rate Updates**: Exchange rates are fetched once per day and cached locally
- 🔄 **Real-time Conversion**: Convert any USD amount to all three Scandinavian currencies
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🏦 **Current Rates Display**: Shows current exchange rates rounded to the nearest 10th
- 🔄 **Manual Refresh**: Option to manually refresh rates if needed

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd scandinavian-currency-converter
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create the templates directory:**
   ```bash
   mkdir templates
   ```

5. **Move the HTML file:**
   Place the `index.html` file in the `templates/` directory.

### Running the Application

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   Navigate to `http://localhost:5000`

The application will automatically fetch exchange rates on the first visit and cache them for the day.

## Project Structure

```
scandinavian-currency-converter/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── templates/
│   └── index.html     # Web interface
└── exchange_rates.json # Auto-generated rates cache
```

## API Usage

The application uses the free [ExchangeRate-API](https://exchangerate-api.com/) service to fetch current exchange rates. No API key is required for basic usage.

## Features Explained

### Daily Rate Caching
- Rates are fetched once per day on first usage
- Cached in `exchange_rates.json` file
- Automatically refreshed the next day

### Supported Currencies
- **SEK** - Swedish Krona 🇸🇪
- **DKK** - Danish Krone 🇩🇰  
- **NOK** - Norwegian Krone 🇳🇴

### Web Interface
- Clean, modern design with gradient backgrounds
- Responsive layout for mobile devices
- Real-time conversion without page reload
- Manual refresh button for updating rates

## Deployment

### Local Development
The app runs on `http://localhost:5000` by default.

### Production Deployment
For production deployment, consider:
- Using a proper WSGI server like Gunicorn
- Setting up environment variables for configuration
- Using a more robust database for rate storage
- Adding SSL/HTTPS

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### Common Issues

1. **No rates displayed**: Check your internet connection and try refreshing
2. **Old rates**: Use the "Refresh Rates" button to get updated rates
3. **Connection errors**: The API might be temporarily unavailable

### Error Handling
- Network errors are gracefully handled
- Invalid inputs are validated
- Helpful error messages are displayed to users

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

If you encounter any issues or have questions, please open an issue on GitHub.