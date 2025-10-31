import sys
from dataclasses import dataclass


import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer


from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    """
    Class Name : DataTransformationConfig
    Description : This class holds the configuration for data transformation, including the file path for the preprocessor object.
    
    Attributes :
        preprocessor_obj_file_path (str): The file path where the preprocessor object will be saved.
    """

    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    """"
    Class Name : DataTransformation
    Description : This class is responsible for data transformation, which includes creating a preprocessing pipeline
                  and applying it to the training and testing data.
    Attributes :
        data_transformation_config (DataTransformationConfig): An instance of DataTransformationConfig that holds the configuration for data transformation.
    Methods :
        __init__(): Initializes the DataTransformation class and its configuration.
        get_data_transformer_object(): Creates and returns a preprocessing pipeline for numerical and categorical features.
    """

    def __init__(self):
        """"
        Method Name : __init__
        Description : This is the constructor method for the DataTransformation class. It initializes the data transformation configuration.
        """

        self.data_transformation_config=DataTransformationConfig()


    def get_data_transformer_object(self):
        """"
        Method Name : get_data_transformer_object
        Description : This method creates and returns a preprocessing pipeline for numerical and categorical features.
        Returns : A ColumnTransformer object that applies the preprocessing pipelines to the respective feature types.
        On Failure : Raises a CustomException if any error occurs during the process.
        """

        try:
            logging.info("Data Transformation initiated")

            # Define which columns are numerical and which are categorical
            numerical_columns = ['writing_score', 'reading_score']
            categorical_columns = ['gender', 'race_ethnicity', 'parental_level_of_education',
                                   'lunch', 'test_preparation_course']
            
            # Create a pipeline for numerical features
            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])

            # Create a pipeline for categorical features
            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder', OneHotEncoder()),
                ('scaler', StandardScaler(with_mean=False))
            ])

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # Combine both pipelines into a ColumnTransformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num_pipeline', num_pipeline, numerical_columns),
                    ('cat_pipeline', cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        
        except Exception as e:
            logging.info("Error in Data Transformation")
            raise CustomException(e,sys)

    def initiate_data_transformation(self, train_path, test_path):
        """"
        Method Name : initiate_data_transformation
        Description : This method applies the preprocessing pipeline to the training and testing data.
        Returns : A tuple containing the transformed training array, transformed testing array, and the preprocessor object.
        On Failure : Raises a CustomException if any error occurs during the process.
        """
        
        try:
            # Read the training and testing data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessor object")

            preprocessor_obj = self.get_data_transformer_object()

            target_column_name = 'math_score'
            numerical_columns = ['writing_score', 'reading_score']

            # Separate input features and target variable for training data
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            # Separate input features and target variable for testing data
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            # Apply the preprocessing pipeline to the training and testing input features
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            logging.info("Applying preprocessing object on training and testing datasets.")

            # Combine the transformed input features with the target variable
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Saved preprocessor object.")

            # Save the preprocessor object to a file
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            logging.info("Error in initiate_data_transformation")
            raise CustomException(e,sys)