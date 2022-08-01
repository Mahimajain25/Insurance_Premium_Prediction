from insurance.exception import Insurance_Exception
import os, sys
#from insurance.config.configuration import Configuration
from insurance.pipeline.pipeline import Pipeline
from insurance.logger import logging
from insurance.config.configuration import Configuration
from insurance.component.data_ingestion import DataIngestion
def main():
    try:
        config_path = os.path.join("config", "config.yaml")
        pipeline = Pipeline(Configuration(config_file_path=config_path))
        #pipeline = Pipeline(config=configuration)
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__=="__main__":
    main()
