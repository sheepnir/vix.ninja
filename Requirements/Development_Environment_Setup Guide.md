# VIX.Ninja - Development Environment Setup Guide

This guide will walk you through setting up your development environment for the VIX.Ninja project on macOS using zsh, VSCode, and Python virtual environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Python Environment Setup](#python-environment-setup)
3. [VSCode Configuration](#vscode-configuration)
4. [Interactive Brokers Gateway Setup](#interactive-brokers-gateway-setup)
5. [Project Initialization](#project-initialization)
6. [Frontend Environment Setup](#frontend-environment-setup)
7. [Database Setup](#database-setup)
8. [Running the Application](#running-the-application)

## Prerequisites

Ensure you have the following installed on your Mac:

- Homebrew (package manager)
- Git
- Python 3.8+
- Node.js and npm
- VSCode

If you need to install any of these, here are the commands:

```zsh
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Git
brew install git

# Install Python
brew install python

# Install Node.js and npm
brew install node

# Install VSCode
brew install --cask visual-studio-code
```

## Python Environment Setup

### Create a Project Directory

```zsh
# Create a directory for your project
mkdir vix.ninja
cd vix.ninja

# Initialize git repository
git init
```

### Set Up Python Virtual Environment

```zsh
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Your terminal prompt should change to indicate the active environment
# (venv) username@hostname:~/vix.ninja$

# To deactivate the virtual environment when working on other projects
# Simply run:
deactivate

# After deactivation, your terminal prompt will return to normal
# username@hostname:~/vix.ninja$
```

### Create a .zshrc Alias (Optional)

For convenience, you can add an alias to your `.zshrc` file to activate the virtual environment:

```zsh
# Open .zshrc file
nano ~/.zshrc

# Add the following line
alias venv-vix="source ~/vix.ninja/venv/bin/activate"

# Save and exit (Ctrl+O, Enter, Ctrl+X)

# Apply changes
source ~/.zshrc
```

Now you can activate the environment by typing `venv-vix` from anywhere.

### Install Required Python Packages

Create a `requirements.txt` file:

```zsh
touch requirements.txt
```

Add the following packages to `requirements.txt`, using versions compatible with Python 3.13:

```
# Core dependencies
numpy>=2.0.0
pandas>=2.1.3
Flask>=2.2.5
Flask-RESTful>=0.3.10
Flask-Cors>=4.0.0
matplotlib>=3.8.0
ib-insync>=0.9.85
yfinance>=0.2.30
SQLAlchemy>=2.0.0

# Development tools
pytest>=7.4.0
black>=23.10.0
```

Install the packages:

```zsh
# Install packages with verified Python 3.13 compatibility
pip install -r requirements.txt

# Update pip as suggested in the error message
pip install --upgrade pip
```

Based on the most current information, NumPy 2.0.0 and above officially supports Python 3.13 with NumPy 2.1.0 and 2.2.0 releases specifically adding full Python 3.13 compatibility. Also note that certain packages like pandas may have compatibility issues with newer NumPy versions, so the requirements specify pandas 2.1.3 or newer to avoid known compatibility issues.

## VSCode Configuration

### Install Recommended Extensions

Launch VSCode and install the following extensions:

1. Python (Microsoft)
2. Pylance
3. Python Docstring Generator
4. ESLint
5. Prettier
6. React Extension Pack
7. TypeScript Vue Plugin
8. GitLens

You can install them via the command line:

```zsh
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension njpwerner.autodocstring
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension jawandarajbir.react-vscode-extension-pack
code --install-extension Vue.volar
code --install-extension eamodio.gitlens
```

### Configure Python Settings

Open VSCode in your project directory:

```zsh
code .
```

Create a `.vscode` directory with a `settings.json` file:

```zsh
mkdir -p .vscode
touch .vscode/settings.json
```

Add the following configuration to `settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.terminal.activateEnvironment": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## Interactive Brokers Gateway Setup

### Install IB Gateway

1. Download IB Gateway for Mac from the [Interactive Brokers website](https://www.interactivebrokers.com/en/index.php?f=16457)
2. Follow the installation instructions
3. Register for a demo account if you don't already have an account

### Configure IB Gateway

1. Launch IB Gateway
2. Log in with your credentials
3. Configure API settings:
   - Enable Active X and Socket Clients
   - Set socket port to 7496 for live or 7497 for paper trading
   - Disable read-only API

## Project Initialization

### Set Up Project Structure

Create the basic project structure:

```zsh
# Create directories
mkdir -p backend/app/{api,models,services,utils}
mkdir -p backend/config
mkdir -p backend/tests
mkdir -p frontend/src/{components,hooks,pages,services,styles,utils}
```

### Create Basic Configuration Files

Create a `.gitignore` file:

```zsh
touch .gitignore
```

Add the following to `.gitignore`:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
venv/

# TypeScript/JavaScript
node_modules/
npm-debug.log
yarn-debug.log
yarn-error.log
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
coverage/
build/

# VS Code
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json

# macOS
.DS_Store
.AppleDouble
.LSOverride
Icon
._*
.Spotlight-V100
.Trashes

# SQLite
*.sqlite
*.db
```

## Flask Backend Setup

### Create Flask Application

Create `backend/app/__init__.py`:

```zsh
touch backend/app/__init__.py
```

Add the following content to the file:

```python
from flask import Flask
from flask_cors import CORS

def create_app(config_name="development"):
    app = Flask(__name__)
    CORS(app)

    # Import and register blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
```

Create `backend/app/api/__init__.py`:

```zsh
touch backend/app/api/__init__.py
```

Add the following content:

```python
from flask import Blueprint

api_bp = Blueprint('api', __name__)

from app.api import routes
```

Create `backend/app/api/routes.py`:

```zsh
touch backend/app/api/routes.py
```

Add the following content:

```python
from app.api import api_bp
from flask import jsonify

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "API is operational"})
```

Create `backend/run.py`:

```zsh
touch backend/run.py
```

Add the following content:

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## Frontend Environment Setup

### Initialize React App with TypeScript

Navigate to the frontend directory and create a new React app with TypeScript:

```zsh
cd frontend
npx create-react-app . --template typescript
```

### Install Additional Frontend Dependencies

```zsh
npm install axios react-router-dom @types/react-router-dom d3 @types/d3 recharts
npm install tailwindcss postcss autoprefixer --save-dev
```

### Configure Tailwind CSS

Initialize Tailwind CSS:

```zsh
npx tailwindcss init -p
```

Update `tailwind.config.js`:

```javascript
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

Add Tailwind directives to `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Database Setup

### Initialize SQLite Database

Create a directory for the database:

```zsh
mkdir -p backend/instance
```

Create a database initialization script:

```zsh
touch backend/app/models/database.py
```

Add the following content:

```python
import sqlite3
import os
from flask import g

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'vix_ninja.sqlite')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE_PATH,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()

    # Create tables
    db.execute('''
    CREATE TABLE IF NOT EXISTS vix_futures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME NOT NULL,
        contract_month TEXT NOT NULL,
        price REAL NOT NULL,
        open_interest INTEGER,
        volume INTEGER,
        UNIQUE(timestamp, contract_month)
    )
    ''')

    db.execute('''
    CREATE TABLE IF NOT EXISTS vix_index (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME NOT NULL,
        value REAL NOT NULL,
        UNIQUE(timestamp)
    )
    ''')

    db.commit()

# Call init_db to ensure tables exist
init_db()
```

## Interactive Brokers Service Setup

Create a service for IB Gateway:

```zsh
touch backend/app/services/ib_service.py
```

Add the following content:

```python
from ib_insync import IB, Future
import datetime
import logging

logger = logging.getLogger(__name__)

class IBService:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ib = IB()

    def connect(self):
        """Connect to IB Gateway"""
        try:
            if not self.ib.isConnected():
                self.ib.connect(self.host, self.port, clientId=self.client_id)
                logger.info(f"Connected to IB Gateway on {self.host}:{self.port}")
                return True
            return True
        except Exception as e:
            logger.error(f"Failed to connect to IB Gateway: {e}")
            return False

    def disconnect(self):
        """Disconnect from IB Gateway"""
        if self.ib.isConnected():
            self.ib.disconnect()
            logger.info("Disconnected from IB Gateway")

    def get_vix_futures(self):
        """Get VIX futures data"""
        if not self.ib.isConnected():
            self.connect()

        futures_data = []

        # Get current month and year
        now = datetime.datetime.now()

        # Loop through the next 9 months to get all VIX futures
        for i in range(9):
            future_date = now + datetime.timedelta(days=30 * i)
            future_symbol = f"VX{future_date.strftime('%Y%m')}"

            contract = Future('VIX', future_date.strftime('%Y%m'), 'CFE')

            try:
                self.ib.qualifyContracts(contract)
                ticker = self.ib.reqMktData(contract)
                self.ib.sleep(1)  # Give time for data to arrive

                if ticker.lastGreeks:
                    futures_data.append({
                        'contract': future_symbol,
                        'price': ticker.last if ticker.last > 0 else ticker.close,
                        'bid': ticker.bid,
                        'ask': ticker.ask,
                        'volume': ticker.volume,
                        'open_interest': ticker.openInterest
                    })
            except Exception as e:
                logger.error(f"Error fetching data for {future_symbol}: {e}")

        return futures_data
```

## Yahoo Finance Service Setup

Create a service for Yahoo Finance:

```zsh
touch backend/app/services/yahoo_service.py
```

Add the following content:

```python
import yfinance as yf
import logging

logger = logging.getLogger(__name__)

class YahooService:
    @staticmethod
    def get_vix_index():
        """Get current VIX index value from Yahoo Finance"""
        try:
            vix_ticker = yf.Ticker("^VIX")
            vix_data = vix_ticker.history(period="1d")

            if not vix_data.empty:
                current_value = vix_data['Close'].iloc[-1]
                return {
                    'value': current_value,
                    'timestamp': vix_data.index[-1].to_pydatetime()
                }
            else:
                logger.error("No VIX data returned from Yahoo Finance")
                return None
        except Exception as e:
            logger.error(f"Error fetching VIX data from Yahoo Finance: {e}")
            return None
```

## Running the Application

### Start the Backend

```zsh
# From the project root directory
cd backend
source ../venv/bin/activate  # If not already activated
python run.py
```

The Flask backend should start and be accessible at `http://localhost:5000`.

### Start the Frontend

```zsh
# From the project root directory
cd frontend
npm start
```

The React frontend should start and be accessible at `http://localhost:3000`.

## Next Steps

Now that your development environment is set up, you can proceed with implementing the specific features of your VIX futures term structure visualization application according to the PRD.

The next components to develop would be:

1. Implement the term structure calculation logic
2. Create the visualization components
3. Set up the data refresh schedules
4. Develop the trading signals algorithms
5. Build the user interface with React and TypeScript

Happy coding!
