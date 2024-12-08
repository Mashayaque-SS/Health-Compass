# Health Compass

**Health Compass** is a web application designed to predict health risks for heart disease and diabetes using machine learning models. The app provides a user-friendly interface for accessing predictions, health insights, and doctor recommendations, combining the power of data science and web technologies.

---

## Features

- **Heart Disease Prediction**: Utilizes a Logistic Regression model tuned with `GridSearchCV`.
- **Diabetes Prediction**: Powered by a Random Forest Classifier.
- **Well-being Insights**: Offers preventative measures and lifestyle tips.
- **Doctor Recommendations**: Fetches nearby doctors using APIs and provides a static list of recommended doctors.
- **Profile Management**: Stores and displays user health history and predictions.
- **Admin Dashboard**: Admin can monitor user data and activity.

---

## Tech Stack

- **Backend**: Flask
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning Models**: Logistic Regression and Random Forest Classifier
- **Data**: Kaggle datasets (Heart Disease and Diabetes)
- **Environment Management**: Conda (Miniconda3)
- **APIs Used**: Foursquare, OpenCage

---

## Project Structure

Health_Compass/

├── env/             # Conda environment with required libraries

├── flask/           # Flask backend and frontend files

         ├── env/                 # Environment folder of flask containing python and its libraries

         ├── static/              # CSS, JavaScript, and images

         ├── templates/           # HTML templates

         ├── app.py               # Flask application entry point

         ├── db_setup.py/         # Database setup python file

         ├── health_compass.db/   # actual database of health compass

         ├── diabetes_model.pkl/  # Diabetes model 

         └── tuned_logistic_regression_model.pkl     # Heart disease model

├── datasets/        # Kaggle datasets

         ├── heart_disease.csv
         
         ├── diabetes.csv
         
├── models/          # Saved machine learning models

         ├── heart disease model(tuned_logistic_regression_model.pkl)
         
         ├── diabetes model(diabetes_model.pkl)
         
├── notebooks/       # Jupyter notebooks for model training and testing

         ├── heart disease notebook(heart-disease.ipynb)
         
         ├── diabetes notebook(diabetes.ipynb)

└── README.md        # Project README

---

## Flow Chart

![image](https://github.com/user-attachments/assets/a20ec204-143a-4faf-9951-ace44b297226)

---

## Screenshots

