
# Insurance Premium Prediction
- The goal of this project is to give people an estimate of how much they need based on their individual health situation. 
-  After that, customers can work with any health insurance carrier and its plans and perks while keeping the projected cost from our study in mind. 
- This can assist a person in concentrating on the health side of an insurance policy rather han the ineffective part.
## Deployment link
Heroku Deployment
- https://insurance-premium-prediction-0.herokuapp.com/
![Screenshot landing](https://raw.githubusercontent.com/Mahimajain25/Insurance_Premium_Prediction/main/z_project_image/Insurance_landing_page.png)
## Approach

- **Exploratory Data Analysis :** Analysed the dataset in google colab using pandas, numpy, matplotlib library.  [EDA file](https://github.com/Mahimajain25/Insurance_Premium_Prediction/blob/main/Insurance_premium_EDA.ipynb)
- **Data Ingestion :** Data is ingested from the google drive link. GoogleDriveDownloader library is used to extract the data. Data is splited using stratifiedshufflesplit (scikit learn lib).
- **Data Validation :** Data is validated based on the schema file and Data drift is analysis with HTML web page.
- **Data Transformation :** Categorical features are converted into numberical feature using custom Transformer.
- **Model Training :** Machine learning alorithm used :
    i) linear regression 
    ii) DecisionTreeRegressor
    iii) RandomForestRegressor
    iv) GradientBoostingRegressor  
- **Model Evaluation :** Selecting the best model out of above model based on root mean squared error and accuracy of train and test data.
- **Model Push :** Push the best model in the production if production model accuracy is low

### **Technologies used**
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

### **Tools used**
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)
## Contact

- linkedin - https://www.linkedin.com/in/mahima-jain-41b540191/
- gmail - mahimaj25@gmail.com
