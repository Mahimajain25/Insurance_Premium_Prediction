import logging
import os, sys
from insurance.exception import Insurance_Exception
from insurance.logger import logging
from insurance.entity.config_entity import DataIngestionConfig
from google_drive_downloader import GoogleDriveDownloader as gdd
from insurance.entity.artifact_entity import DataIngestionArtifact
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
from insurance.util.util import *
from insurance.config.configuration import Configuration
import zipfile


class DataIngestion():

    def __init__(self,data_ingestion_config:DataIngestionConfig ):
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20} ")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise Insurance_Exception(e,sys) from e

    def get_data_ingestion_config(self):
        try:
            conn = Configuration()
            get_data_ingestion_config = conn.get_data_ingestion_config()
            return get_data_ingestion_config
        except Exception as e:
            raise Insurance_Exception(e,sys) from e

    def download_insurance_premium_data(self):
        try:
            get_data_ingestion_config = self.get_data_ingestion_config()

            #extracting zip folder path
            zip_download_dir = get_data_ingestion_config.zip_download_data

            #extracting and transforming the url to get the file_id
            dataset_download_url = get_data_ingestion_config.dataset_download_url
            url = 'https://drive.google.com/uc?id=' + dataset_download_url.split('/')[-2]
            unformated_id = url.split('/')[3]
            file_id = unformated_id.split('=')[1]

            #path and file name
            zip_download_dir = zip_download_dir + '\\insurance.zip'
            logging.info(f"Downloading file from :[{dataset_download_url}] into :[{zip_download_dir}]")
            # downloading zip file from google
            gdd.download_file_from_google_drive(file_id= file_id,
                                              dest_path=zip_download_dir)
            logging.info(f"File :[{zip_download_dir}] has been downloaded successfully.")

            # extratcting raw folder path
            raw_data_dir = get_data_ingestion_config.raw_data_dir

            #extracting csv file from zip file
            logging.info(f"Extracting zip file: [{zip_download_dir}] into dir: [{raw_data_dir}]")
            with zipfile.ZipFile(zip_download_dir, 'r') as zip_ref:
                zip_ref.extractall(raw_data_dir)
            logging.info(f"Extraction completed")
        except Exception as e:
            raise Insurance_Exception(e,sys) from e

    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            self.download_insurance_premium_data()
            ## retriving data
            get_data_ingestion_config = self.get_data_ingestion_config()
            raw_data_dir = get_data_ingestion_config.raw_data_dir
            ingested_train_dir = get_data_ingestion_config.ingested_train_dir
            ingested_test_dir = get_data_ingestion_config.ingested_test_dir

            file_name = os.listdir(raw_data_dir)[0]

            insurance_premium_file_path = os.path.join(raw_data_dir, file_name)

            logging.info(f"Reading csv file: [{insurance_premium_file_path}]")
            insurance_premium_data_frame = pd.read_csv(insurance_premium_file_path)

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index, test_index in split.split(insurance_premium_data_frame,
                                                       insurance_premium_data_frame['smoker']):
                strat_train_set = insurance_premium_data_frame.loc[train_index]
                strat_test_set = insurance_premium_data_frame.loc[test_index]

            train_file_path = os.path.join(ingested_train_dir,
                                           file_name)

            test_file_path = os.path.join(ingested_test_dir,
                                          file_name)

            if strat_train_set is not None:
                os.makedirs(ingested_train_dir, exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path, index=False)

            if strat_test_set is not None:
                os.makedirs(ingested_test_dir, exist_ok=True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested=True,
                                                            message=f"Data ingestion completed successfully."
                                                            )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise Insurance_Exception(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            return self.split_data_as_train_test()
            #res = self.split_data_as_train_test()
            #print(res.train_file_path)
        except Exception as e:
            raise Insurance_Exception(e, sys) from e


    def __del__(self):
        logging.info(f"{'>>' * 20}Data Ingestion log completed.{'<<' * 20} \n\n")

#di = DataIngestion(DataIngestionConfig)
#di.download_insurance_premium_data()
#di.split_data_as_train_test()
#di.initiate_data_ingestion()