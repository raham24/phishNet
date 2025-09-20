# PhishNet

A browser extension that provides real-time phishing protection using machine learning to detect and warn users about potentially malicious websites.

## Features

- **Real-time URL Analysis**: Automatically scans websites as you browse using a trained decision tree classifier
- **User Authentication**: Secure login system with hashed password storage
- **Whitelist Management**: Add trusted websites to bypass scanning
- **Statistics Dashboard**: View your browsing safety statistics with visual charts
- **Customizable Notifications**: Configure alerts for different types of website classifications
- **Protection Toggle**: Easy on/off switch for the protection system

## Architecture

PhishNet consists of three main components:

### 1. Browser Extension (Frontend)
- **Popup Interface**: Main control panel with protection toggle and navigation
- **Login System**: User authentication interface
- **Settings Page**: Notification preferences and configuration
- **Statistics Page**: Visual dashboard showing safe vs. phishing attempts
- **Whitelist Manager**: Interface for managing trusted websites

### 2. Flask Backend API
- **URL Prediction**: Machine learning-based phishing detection
- **User Management**: Authentication and user data handling
- **Whitelist Operations**: Add/remove trusted websites
- **Statistics**: Track and retrieve user browsing safety data

### 3. PostgreSQL Database
- **User Table**: Stores user credentials with hashed passwords
- **Whitelist Table**: User-specific trusted websites
- **Phishing Attempts Table**: History of analyzed URLs and predictions

## Installation

### Prerequisites
- Python 3.7+
- PostgreSQL database
- Chrome/Chromium browser
- Required Python packages (see requirements below)

### Backend Setup

1. **Install Python Dependencies**
```bash
pip install flask flask-cors psycopg2 scikit-learn pandas numpy requests beautifulsoup4 python-whois joblib
```

2. **Database Setup**
Set up PostgreSQL with the following configuration:
- Database: `postgres`
- User: `postgres` 
- Password: `password`

Create the required tables:
```sql
-- User table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);

-- Whitelist table
CREATE TABLE "whiteList" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id),
    whitelisted_url VARCHAR(255) NOT NULL
);

-- Phishing attempts table
CREATE TABLE "phishingAttempts" (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    phishing_url VARCHAR(255) NOT NULL,
    decision_tree_prediction INTEGER NOT NULL,
    user_id INTEGER REFERENCES "user"(id)
);
```

3. **Start the Flask Server**
```bash
python main.py
```
The server will run on `http://localhost:5000`

### Browser Extension Setup

1. **Load the Extension**
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the extension directory

2. **Required Files**
   - Ensure you have the trained model file `rfc.pkl` in the root directory
   - Add your PhishNet logo as `PhishNET.png`

## Usage

### First Time Setup
1. Click the PhishNet extension icon
2. Create an account or log in with existing credentials
3. Toggle protection ON from the main popup

### Daily Use
- Browse normally - PhishNet automatically analyzes visited websites
- Receive notifications based on your settings:
  - **Green**: Safe websites
  - **Red**: Potential phishing sites
  - **Blue**: Whitelisted sites (trusted)

### Managing Whitelists
1. Click "Whitelisting" from the main popup
2. Enter full URLs in the format: `https://www.example.com`
3. Use "Add" to whitelist or "Remove" to unwhitelist sites

### Viewing Statistics
- Access the Statistics page to see:
  - Pie chart of safe vs. phishing attempts
  - List of recently visited websites
  - Overall protection effectiveness

## API Endpoints

- `POST /login` - User authentication
- `POST /predict` - URL analysis and prediction
- `POST /addwl` - Add website to whitelist
- `POST /rmwl` - Remove website from whitelist
- `POST /test` - Get user's whitelist
- `POST /getsafe` - Get safe website statistics
- `POST /updatelist` - Get list of analyzed websites

## Machine Learning Model

PhishNet uses a Random Forest Classifier trained on various URL features:
- IP address presence
- URL length
- Shortening service detection
- SSL certificate status
- Domain age
- Subdomain analysis
- Google indexing status

The model returns:
- `1`: Safe website
- `0`: Unsafe website  
- `-1`: Phishing website

## File Structure

```
PhishNet/
├── manifest.json              # Extension manifest
├── main.py                    # Flask backend server
├── loginpage.py              # User authentication logic
├── parse.py                  # URL feature extraction
├── rfc.pkl                   # Trained ML model
├── LoginPage.html            # Login interface
├── PopUp.html               # Main extension popup
├── settings.html            # Settings page
├── stats.html              # Statistics dashboard
├── wl.html                 # Whitelist management
├── styles.css              # Stylesheet
└── scripts/
    ├── background.js        # Extension background processes
    ├── login_script.js      # Login page logic
    ├── popup_script.js      # Main popup functionality
    ├── settings.js          # Settings page logic
    ├── stats_scripts.js     # Statistics page logic
    └── wl.js               # Whitelist management logic
```

## Security Features

- **Password Hashing**: Uses SHA-256 for secure password storage
- **SQL Injection Protection**: Parameterized queries prevent SQL injection
- **User Isolation**: Each user's data is properly segregated
- **HTTPS Validation**: Checks for secure connections

## Customization

### Notification Settings
Configure which types of notifications you receive:
- Whitelist notifications
- Phishing site alerts  
- Safe site confirmations

### Model Retraining
To update the machine learning model:
1. Prepare new training data
2. Retrain the model using scikit-learn
3. Save as `rfc.pkl` and replace the existing file

## Troubleshooting

### Common Issues

**Extension not working:**
- Ensure the Flask server is running on port 5000
- Check browser console for JavaScript errors
- Verify database connection

**Database connection errors:**
- Confirm PostgreSQL is running
- Check database credentials in the code
- Ensure required tables exist

**Prediction errors:**
- Verify `rfc.pkl` model file exists
- Check that all required Python packages are installed
- Review server logs for detailed error messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please check the repository for license details.

## Support

For issues and questions:
- Check the troubleshooting section above
- Review server logs for error details
- Ensure all dependencies are properly installed
