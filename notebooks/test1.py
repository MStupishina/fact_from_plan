import math

from catboost import CatBoostRegressor
import joblib
import pandas as pd

from sklearn.metrics import mean_squared_error

model_cat_loaded = CatBoostRegressor()
model_cat_loaded.load_model("CatBoosts_new.cbm")
features={}
label_encoders = joblib.load("../models/label_encoders_new.pkl")

parameters=['TYPE_PRODUCT', 'PROJECT', 'DIVISION_NAME', 'DOC_TYPE_NAME', 'STANDART',
       'FUNCTIONAL_NAME', 'NEW_TYPE_DOC']
parameters_new = ['TYPE_PRODUCT', 'PROJECT', 'DIVISION_NAME', 'STANDART_NAME',
       'DOC_TYPE_NAME', 'TYPE_WORK_NAME', 'FUNCTIONAL_NAME', 'TYPE_DOC_NEW',
       'VIEW_DOC_NEW']
data_test = pd.read_csv("../data_set/data_set_11.08.25_2.csv", sep=";", decimal=",")
print(data_test.at[0,'TYPE_PRODUCT'])
data_test.dropna(inplace=True, subset=['PLAN_LABOR','FACT_LABOR'])
mask=(data_test["PLAN_LABOR"]<=80)&(data_test["FACT_LABOR"]<=100)
data_test=data_test.loc[mask]
mse=mean_squared_error(data_test['PLAN_LABOR'],data_test['FACT_LABOR'])
print(math.sqrt(mse))
test_data=[data_test.at[31, column] for column in parameters]

# test_data=['РД', 'Курская-2 АЭС бл. 1,2', 'ОТА БКП-3', 'AT. Задание заводу на программно-технический комплекс (ПТК)',
#            'Задание заводу на ПТК','Электротехника и системы автоматизации', 'Комплект РД. ЗЗИ']
# for param in parameters:
#     encoded_value = label_encoders[param].transform([input(f'Введите значение параметра {param}:')])
#     features[param]=encoded_value
for param,data in zip(parameters_new, test_data):
    encoded_value = label_encoders[param].transform([data])
    features[param]=encoded_value
plan_labor = float(input('Введите плановые трудозатраты '))
features['PLAN_LABOR']=plan_labor
df=pd.DataFrame([features])
y_pred = model_cat_loaded.predict(df)
print(y_pred)