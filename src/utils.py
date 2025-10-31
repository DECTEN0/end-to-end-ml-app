import os
import sys

import numpy as np 
import pandas as pd
import dill
import pickle


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