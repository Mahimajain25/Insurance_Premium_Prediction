import os,sys
from insurance.entity.config_entity import *
from insurance.entity.artifact_entity import *
from insurance.exception import Insurance_Exception
from insurance.util.util import *
from insurance.logger import logging
from insurance.constant import *
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import numpy as np


class feature_generator(BaseEstimator,TransformerMixin) :

    def __init__(self):
        try:
           pass
        except Exception as e:
            raise Insurance_Exception(e,sys) from e

    def fit(self,X,y=None):
        return self

    def transform(self, X, y=None):
        try:
            ## coverting numpy to pandas and renaming the col headers
            X = pd.DataFrame.from_records(X)
            X = X.rename({0: 'sex', 1: 'smoker', 2: 'region'}, axis=1)
            # Transforming categorical to numerical
             # male = 1, female =0
            X['sex'] = X['sex'].map({'male': 1, 'female': 0})
             # New Col smoker cat yes = 1, no = 0
            X['smoker_cat'] = X['smoker'].map({'yes': 1, 'no': 0})
            X = X.drop(columns='smoker', axis=1)
             # sw =1 ,SE = 2, NW = 3, NE =4
            X['region'] = X['region'].map({'southwest': 1, 'southeast': 2, 'northwest': 3, 'northeast': 4})
            return X
        except Exception as e:
            raise Insurance_Exception(e,sys) from e

class DataTransformation:

    def __init__(self,data_transformation_config:DataTransformationConfig,
                 data_ingestion_artifact:DataIngestionArtifact,data_validation_artifact:DataValidationArtifact):
        try:
            logging.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30} ")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise Insurance_Exception(e,sys) from e

    def get_transformer_object(self):
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path
            dataset_schema = read_yaml_file(schema_file_path)
            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]
            categorical_columns = dataset_schema[CATEGORICAL_COLUMN_KEY]

            cat_pipline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy="most_frequent")),
                ('feature_generator',feature_generator())
            ])

            num_pipeline = Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='median'))
            ])

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preproccessing = ColumnTransformer([
               ( 'num_pipeline', num_pipeline,numerical_columns),
                ('cat_pipeline',cat_pipline,categorical_columns)
            ])

            return preproccessing
        except Exception as e:
            raise Insurance_Exception(e,sys) from e

    def initiate_data_transformation(self):
        try:
            logging.info(f"Obtaining preprocessing object.")
            preprocessing_obj = self.get_transformer_object()

            logging.info(f"Obtaining training and test file path.")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path

            logging.info(f"Loading training and test data as pandas dataframe.")
            train_df = load_data(file_path=train_file_path, schema_file_path=schema_file_path)

            test_df = load_data(file_path=test_file_path, schema_file_path=schema_file_path)

            schema_file_path = self.data_validation_artifact.schema_file_path

            schema = read_yaml_file(file_path=schema_file_path)

            target_column_name = schema[TARGET_COLUMN_KEY]

            logging.info(f"Splitting input and target feature from training and testing dataframe.")
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv", ".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv", ".npz")

            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            logging.info(f"Saving transformed training and testing array.")

            save_numpy_array_data(file_path=transformed_train_file_path, array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path, array=test_arr)

            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_path

            logging.info(f"Saving preprocessing object.")
            save_object(file_path=preprocessing_obj_file_path, obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
                                                                      message="Data transformation successfull.",
                                                                      transformed_train_file_path=transformed_train_file_path,
                                                                      transformed_test_file_path=transformed_test_file_path,
                                                                      preprocessed_object_file_path=preprocessing_obj_file_path

                                                                      )
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise Insurance_Exception(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 30}Data Transformation log completed.{'<<' * 30} \n\n")


