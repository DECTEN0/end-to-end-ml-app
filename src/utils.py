import os
import sys

import numpy as np 
import pandas as pd
import dill
import pickle

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

from src.exception import CustomException

def save_object(file_path, obj):
    
    """"
    Function Name : save_object
    Description : This function saves a Python object to a specified file path using dill serialization.
    Parameters :
        file_path (str): The file path where the object will be saved.
        obj (any): The Python object to be saved.
    On Failure : Raises a CustomException if any error occurs during the process.
    """

    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    """
    Function Name : evaluate_models
    Description : This function evaluates multiple machine learning models using the provided training and testing data,
                  along with hyperparameter tuning. It returns a report of model performance.   
    Parameters :
        X_train (numpy.ndarray): The training input features.
        y_train (numpy.ndarray): The training target variable.
        X_test (numpy.ndarray): The testing input features.
        y_test (numpy.ndarray): The testing target variable.
        models (dict): A dictionary containing model names as keys and model instances as values.
        param (dict): A dictionary containing model names as keys and hyperparameter grids as values.
    Returns :
        dict: A dictionary containing model names as keys and their corresponding R2 scores as values.
    On Failure : Raises a CustomException if any error occurs during the process.
    """

    try:
        report = {}

        for i in range(len(models)):
            model = list(models.values())[i]
            model_name = list(models.keys())[i]
            params = param[model_name]

            gs = GridSearchCV(model, params, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)