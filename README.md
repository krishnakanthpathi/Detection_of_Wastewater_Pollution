# Detection of Wastewater Pollution

This is a Django-based web application for predicting wastewater pollution using machine learning models (Random Forest, ANN, SVM, Decision Tree, KNeighbors) and tracking user data.

## Complete Installation Guide

### Prerequisites
- [Python 3.11](https://www.python.org/downloads/release/python-3110/) (Required for `scikit-learn` and `numpy` versions. On Windows, ensure "Add Python to PATH" is checked)
- MySQL Server (for the database backend)

### 1. System Dependencies

**macOS:**
Requires [Homebrew](https://brew.sh/). Install `mysql-client` and `pkg-config` to allow the `mysqlclient` python package to compile successfully:
```bash
brew install pkg-config mysql-client
```

**Windows:**
- [Microsoft Visual C++ 14.0 or greater](https://visualstudio.microsoft.com/visual-cpp-build-tools/) is often required when compiling `mysqlclient` and some ML dependencies.

**Linux (Ubuntu/Debian):**
Install the required development headers:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv pkg-config default-libmysqlclient-dev build-essential
```

### 2. Set Up Virtual Environment

Create and activate a virtual environment.

**macOS / Linux:**
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
\.venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

**macOS:**
Set the necessary environment variables for the MySQL client, then install the required packages:
```bash
export PKG_CONFIG_PATH="/opt/homebrew/opt/mysql-client/lib/pkgconfig"
pip install -r service_provider/requirements.txt
```

**Windows / Linux:**
Install the required packages directly:
```bash
pip install -r service_provider/requirements.txt
```
*(Note for Windows users: you can also use `pip install -r service_provider\requirements.txt` if using Command Prompt).*

### 4. Database Setup

Create the MySQL database named `detection_of_wastewater_pollution`. You can do this by running the following command in your MySQL console or terminal:
```sql
CREATE DATABASE IF NOT EXISTS detection_of_wastewater_pollution;
```

**Note:** If your database requires a password for the `root` user, edit the `DATABASES` section in `detection_of_wastewater_pollution/settings.py` to match your local credentials.

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
- **Export Dataset (`.xls`)**: `http://127.0.0.1:8000/Download_Predicted_DataSets/`
