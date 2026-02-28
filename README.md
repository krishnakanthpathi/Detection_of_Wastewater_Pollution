# Detection of Wastewater Pollution

This is a Django-based web application for predicting wastewater pollution using machine learning models (Random Forest, ANN, SVM, Decision Tree, KNeighbors) and tracking user data.

## Installation Instructions (macOS)

### Prerequisites
- [Python 3.11](https://www.python.org/downloads/release/python-3110/) (Required for `scikit-learn` and `numpy` versions)
- [Homebrew](https://brew.sh/) (for installing MySQL system dependencies)
- MySQL Server (for the database backend)

### 1. Install System Dependencies
Install `mysql-client` and `pkg-config` using Homebrew to allow the `mysqlclient` python package to compile successfully:
```bash
brew install pkg-config mysql-client
```

### 2. Set Up Virtual Environment
Create and activate a virtual environment using Python 3.11:
```bash
# Create the environment
python3.11 -m venv .venv

# Activate the environment
source .venv/bin/activate
```

### 3. Install Python Dependencies
Set the necessary environment variables for the MySQL client, then install the packages from `requirements.txt`:
```bash
export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
pip install -r service_provider/requirements.txt
```

### 4. Database Setup
Create the MySQL database named `detection_of_wastewater_pollution`. Run this in your MySQL console or terminal:
```bash
mysql -u root -e "CREATE DATABASE IF NOT EXISTS detection_of_wastewater_pollution;"
```

If your database requires a password for the `root` user, edit the `DATABASES` section in `detection_of_wastewater_pollution/settings.py` to match your credentials.

Apply the database migrations. Because this project contains pre-existing tables, we use the `--fake` flag to sync the renamed Django apps (`remote_user` and `service_provider`):
```bash
python manage.py migrate remote_user --fake
python manage.py migrate service_provider --fake
python manage.py migrate
```

### 5. Run the Server
Start the Django development server:
```bash
python manage.py runserver
```

You can now access the project at `http://127.0.0.1:8000/`.

---

## 🔗 Available Routes

Once the server is running, you can access the following URLs depending on your role.

### Remote User (Client Interface)
- **Login / Home**: `http://127.0.0.1:8000/`
- **Register**: `http://127.0.0.1:8000/Register1/`
- **View Profile**: `http://127.0.0.1:8000/ViewYourProfile/`
- **Predict Pollution**: `http://127.0.0.1:8000/Predict_WasteWater_Pollution_Type/`

### Service Provider (Admin Dashboard)
*(Use `admin` as both username and password)*
- **Admin Login**: `http://127.0.0.1:8000/serviceproviderlogin/`
- **View All Registered Users**: `http://127.0.0.1:8000/View_Remote_Users/`
- **Train Machine Learning Models**: `http://127.0.0.1:8000/train_model/`
- **View All Prediction Logs**: `http://127.0.0.1:8000/View_Prediction_Of_WasteWater_Pollution_Type/`
- **View Prediction Analytics**: `http://127.0.0.1:8000/View_Prediction_Of_WasteWater_Pollution_Type_Ratio/`
- **Export Dataset (`.xls`)**: `http://127.0.0.1:8000/Download_Predicted_DataSets/`---

## Installation Instructions (Windows)

### Prerequisites
- [Python 3.11](https://www.python.org/downloads/release/python-3110/) (Make sure to check "Add Python to PATH" during installation)
- MySQL Server (for the database backend)
- [Microsoft Visual C++ 14.0 or greater](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (often required when compiling `mysqlclient` and some ML dependencies on Windows)

### 1. Set Up Virtual Environment
Open your Command Prompt or PowerShell, navigate to the project directory, and create a virtual environment:
```cmd
python -m venv .venv
```

Activate the virtual environment:
- **Command Prompt:** `\.venv\Scripts\activate.bat`
- **PowerShell:** `.\.venv\Scripts\Activate.ps1`

### 2. Install Python Dependencies
Once activated, install the required packages. (Windows does not usually require `pkg-config`, but having the C++ Build Tools installed is recommended in case `mysqlclient` requires compilation):
```cmd
pip install -r service_provider\requirements.txt
```

### 3. Database Setup
Create the MySQL database named `detection_of_wastewater_pollution`. Run this in your MySQL console:
```sql
CREATE DATABASE IF NOT EXISTS detection_of_wastewater_pollution;
```

Apply the database migrations with the `--fake` flag to sync the renamed Django apps (`remote_user` and `service_provider`):
```cmd
python manage.py migrate remote_user --fake
python manage.py migrate service_provider --fake
python manage.py migrate
```

### 4. Run the Server
Start the Django development server:
```cmd
python manage.py runserver
```

You can now access the project at `http://127.0.0.1:8000/`.
