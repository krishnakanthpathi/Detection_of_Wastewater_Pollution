# Detection of Wastewater Pollution - Project Documentation

This document provides an in-depth overview of the **Detection of Wastewater Pollution** Django application architecture, key features, data models, and its integration with Machine Learning (ML) algorithms.

---

## 🏗 System Architecture overview

The project is built on the Django web framework and utilizes a standard Model-View-Template (MVT) architecture. It is divided functionally into two main constituent applications:
1. **remote_user**: Handles the end-user facing interfaces.
2. **service_provider**: Serves as the administrative dashboard and model management interface.

### Project Directory Structure
- `detection_of_wastewater_pollution/`: Core Django settings and routing configurations.
- `remote_user/`: Views and models associated with regular clients interacting with the system.
- `service_provider/`: Views associated with the backend administrators assessing logs, accuracy, and reports.
- `templates/`: Contains all HTML templates organized by application context (`RUser` and `SProvider`).
- `Datasets.csv` & `Predicted_data.csv`: Used respectively for original training data and output data logs.

---

## 📱 Application Modules & Features

### 1. Remote User (`remote_user`)
This application is designed for clients who want to predict wastewater pollution levels across multiple monitoring locations.

**Key Features:**
- **User Authentication**: Login and registration logic utilizing `ClientRegister_Model`.
- **Profile Management**: Viewing profile details post-authentication.
- **Pollution Prediction**: The core function, `Predict_WasteWater_Pollution_Type`, operates via a user form taking multiple water quality metrics (e.g., pH, BOD, Temperature) indicating location coordinates (`Fid`). The submitted data is vector-transformed and pushed through an **Ensemble Voting Classifier** (aggregating predictions from RF, ANN, SVM, Decision Tree, and KNN) to classify if the wastewater pollution is `High` (1) or `No Pollution` (0).
- **Data Log Generation**: Every prediction runs an insert onto the database (`predict_water_type` model) helping to continuously append to the project's real-life corpus.

### 2. Service Provider (`service_provider`)
Admin personnel interact with this interface to maintain the integrity of users, observe analytical parameters, and re-train the ML models.

**Key Features:**
- **Admin Authentication**: Hardcoded access (`admin/admin`).
- **User Dashboard**: Overview of registered `remote_users`.
- **Model Training and Evaluation (`train_model`)**: An intensive function that pulls directly from `Datasets.csv`, processes features against the `Label`, and subsequently fits five distinct machine learning algorithms simultaneously. It tracks evaluation metrics (Accuracy, Classification Report, Confusion Matrix) and saves evaluation ratios to the schema (`detection_accuracy`) for graphical representations.
- **Analytical Charts**: Generates graphical evaluations of models' accuracy ratios across various charts (`charts`, `charts1`, `likeschart`). 
- **Data Exporting (`Download_Predicted_DataSets`)**: Compiles a dynamically formatted native `.xls` Excel file of all user predictions historically performed on the platform using `xlwt`. 

---

## 🧠 Machine Learning Integration

The core research concept relies on analyzing several hydro-chemical features to predict a binary output state regarding wastewater presence. 

**Dependent Features Analyzed:**
- Temperature 
- Dissolved Oxygen (mg/L)
- pH
- Conductivity (µmhos/cm)
- Biochemical Oxygen Demand (BOD mg/L)
- Nitrate/Nitrite (mg/L)
- Fecal and Total Coliform (MPN/100ml)

**Algorithms Implemented (`scikit-learn`):**
1. **Random Forest Classifier**: High dimensional resilience.
2. **Artificial Neural Networks (ANN/MLP)**: Deep learning representation using `MLPClassifier`.
3. **Support Vector Machines (LinearSVC)**: Maximal margin boundaries.
4. **Decision Tree Classifier**: Feature-level splits for categorical bounds.
5. **K-Nearest Neighbors (KNN)**: Spatial distance clustering.

**Model Pipeline:**
1. **Training Phase**: `service_provider` routes trigger `train_model()`, performing an 80/20 train/test split. It evaluates standalone accuracies to gauge model drift.
2. **Inference Phase (Ensemble)**: `remote_user` routes bundle all aforementioned distinct standalone models into a `VotingClassifier` during inference (`Predict_WasteWater_Pollution_Type`), yielding the most democratically confident result for the end-user input. Count vectorization (`CountVectorizer`) is utilized on the `Fid` identifier before merging pipelines.

---

## 🗄 Database Schema 

The system predominantly interfaces with a MySQL backend running four main entities:

1. **`ClientRegister_Model`**: Validates users alongside their profiles, geography, and contacts.
2. **`predict_water_type`**: Houses the persistent logs of all variables logged by users during a prediction, essentially serving as real-time tracking of water quality parameters plus the prediction result.
3. **`detection_accuracy`**: Temporary tracking of the latest training accuracy percentages for each algorithm, mapped uniquely for graphing views.
4. **`detection_ratio`**: A generalized tally measuring the global volume percentage of 'High Wastewater Pollution' queries relative to the absolute system total. 

---

## 🔄 Execution Flow Summary

1. User registers/logs via **`remote_user`** and submits a water sampling parameter form.
2. Under the hood, **`Predict_WasteWater_Pollution_Type`** reads the dataset, splits data, initiates the `VotingClassifier`, infers the results, stores all data in the **`predict_water_type`** table, and finally presents 'High' or 'No' Wastewater Pollution.
3. Concurrently, a Service Provider accesses their portal to assess charts analyzing the historical precision and performance of the utilized algorithms based on periodic **`train_model`** operations manually re-triggered from the interface to adjust metrics across **`detection_accuracy`**.
4. Extrapolated analytical insights are dumped directly through **`Download_Predicted_DataSets`** for offline geographical planning and investigation.
