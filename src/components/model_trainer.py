# here we train our model or how many model i use 
import os 
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor

from sklearn.ensemble import (
    AdaBoostRegressor,
    RandomForestRegressor,
    GradientBoostingRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging

from src.utils import save_obj
from src.utils import evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self,train_array , test_array):
        try:
            logging.info('spliting training and test input data ')
            X_train,Y_train,x_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models = {
                'Random Forest': RandomForestRegressor(),
                'Decision Tree': DecisionTreeRegressor(),
                'SVR': SVR(),
                'Gradient Boosting': GradientBoostingRegressor(),
                'Linear Regression':LinearRegression(),
                'KNN': KNeighborsRegressor(),
                'XGB': XGBRegressor(),
                'CatBoost': CatBoostRegressor(verbose=False),
                'AdaBoost': AdaBoostRegressor()
            }
            model_report:dict = evaluate_models(X_train,Y_train,x_test,y_test,models)
            
            ## To get best model score from dict 
            best_model_score = max(sorted(model_report.values()))
            
            ## To get best model name from dict
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            
            #here we get best model name from models
            best_model = models[best_model_name]
            
            if best_model_score < 0.6:
                raise CustomException('No best Model found')
            logging.info(f'Best found model on both training and testing dataset {best_model_name}')
            
            save_obj(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj= best_model
            )
            predicted = best_model.predict(x_test)
            r2_square = r2_score(y_test,predicted)
            
            return r2_square
        
        except Exception as e:
            raise CustomException(e,sys)