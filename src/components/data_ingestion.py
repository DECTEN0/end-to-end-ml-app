import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig

@dataclass
class DataIngestionConfig:
    """
    Class Name : DataIngestionConfig
    Description : This class holds the configuration for data ingestion, including file paths for training, testing,
                  and raw data.
    
    Attributes :
        train_data_path (str): The file path where the training data will be saved.
        test_data_path (str): The file path where the testing data will be saved.
        raw_data_path (str): The file path where the raw data will be saved.
    """

    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")

class DataIngestion:
    """"
    Class Name : DataIngestion
    Description : This class is responsible for data ingestion, which includes reading the data from the source,
                  splitting it into training and testing sets, and saving them to specified file paths.
    Attributes :
        ingestion_config (DataIngestionConfig): An instance of DataIngestionConfig that holds the configuration for data ingestion.
    Methods :
        __init__(): Initializes the DataIngestion class and its configuration.
        initiate_data_ingestion(): Reads the data, splits it into training and testing sets, and saves them to the specified file paths.

    """

    def __init__(self):
        """"
        Method Name : __init__
        Description : This is the constructor method for the DataIngestion class. It initializes the data ingestion configuration.
        """

        self.ingestion_config=DataIngestionConfig()


    def initiate_data_ingestion(self):
        """"
        Method Name : initiate_data_ingestion
        Description : This method reads the data from the source, splits it into training and testing sets
                      and saves them to the specified file paths.
        Returns : A tuple containing the file paths of the training and testing data.
        On Failure : Raises a CustomException if any error occurs during the process.
        """

        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv('data/stud.csv')
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Data Ingestion is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys)


if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr, test_arr,_ = data_transformation.initiate_data_transformation(train_data,test_data)
    #train model
    model_trainer=ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr,test_arr))