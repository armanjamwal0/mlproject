# In this file we transfome the data like cat -> num or making new columns
import sys
from datetime import datetime

import pandas as pd 
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
import os
from dataclasses import dataclass
from src.utils import save_obj

@dataclass
class DataTransformationConfig:
    prerpocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_transformer_obj(self):
        '''
        This function is responsible for data transformation 
        '''
        
        
        try:
            num_columns = ['writing_score','reading_score']
            cat_columns = [
                'gender', 
                'race_ethnicity', 
                'parental_level_of_education', 
                'lunch',
                'test_preparation_course'
            ]
            
            num_pip = Pipeline(
                [
                ('Missing Impute',SimpleImputer(strategy='median')),
                ('Scaling Data ',StandardScaler())
                ]
            )
            
            logging.info(f'Numerical columns : {num_columns}')
            
            cat_pip = Pipeline([
                ('Missing Impute',SimpleImputer(strategy='most_frequent')),
                ('Encoding',OneHotEncoder(drop='first',handle_unknown='ignore',sparse_output=False)),
                ('Scaling',StandardScaler())
            ])
            
            logging.info(f'Categorical columns : {cat_columns}')
            
            preprocessing = ColumnTransformer([
                ('num_pip',num_pip,num_columns),
                ('Cat_pip',cat_pip,cat_columns)
            ])
            
            logging.info('Preprocessing is completed ')
            
            return preprocessing
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read train and test data completed')
            
            logging.info('Obtaining preprocesing object')
            
            preprocessor_obj = self.get_data_transformer_obj()
            
            target_column_name = 'math_score'
            num_columns = ['writing_score','reading_score']
            
            input_feature_train_df = train_df.drop(columns=[target_column_name]) # this drop target columns
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns=[target_column_name]) # this drop target columns from test data 
            target_feature_test_df = test_df[target_column_name]
            
            logging.info(
                f'Applying preprocessing object on traning dataframe and testing dataframe.'
            )
            
            input_feature_train_trf = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_trf = preprocessor_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[
                input_feature_train_trf,np.array(target_feature_train_df)  # what this do it combined target and traansformed data by columns 
            ]
            
            test_arr = np.c_[
                            input_feature_test_trf,np.array(target_feature_test_df)  # what this do it combined target and traansformed data by columns 
                        ]
            logging.info(f'Saved preprocessing object.')
            
            save_obj(
                file_path = self.data_transformation_config.prerpocessor_obj_file_path,
                obj = preprocessor_obj
            )
            
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.prerpocessor_obj_file_path  # pickle file path
            )
        except Exception as e:
            raise CustomException(e,sys)