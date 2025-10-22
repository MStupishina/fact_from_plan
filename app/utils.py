from catboost import CatBoostRegressor
import joblib
import pandas as pd

from app.data_base.models import HistoryPredictions
from app.data_base.session import SessionLocal

model_cat_loaded = CatBoostRegressor()
model_cat_loaded.load_model("models/CatBoosts_new.cbm")
parameters = ['TYPE_PRODUCT', 'PROJECT', 'DIVISION_NAME', 'STANDART_NAME',
       'DOC_TYPE_NAME', 'TYPE_WORK_NAME', 'FUNCTIONAL_NAME', 'TYPE_DOC_NEW',
       'VIEW_DOC_NEW']
num_parameters = ['OPERPLAN_LABOR', 'STANDART_LABOR', 'PLAN_LABOR',
                  'CASH']
label_encoders = joblib.load("models/label_encoders_new.pkl")

def predict(work):
    features = {}
    source_features = {}
    try:
        for param in parameters:
            value = getattr(work, param)
            source_features[param] = value
            encoded_value = label_encoders[param].transform([value])
            features[param]=encoded_value

        for param in num_parameters:
            value = getattr(work, param)
            features[param] = value
            source_features[param] = value
        df = pd.DataFrame([features])
        fact_labor = model_cat_loaded.predict(df)
        fact_labor_true = None if "FACT_LABOR" not in source_features else float(source_features.get("FACT_LABOR"))
        error = None
        if fact_labor_true is not None:
            error = float(fact_labor) - fact_labor_true
        with SessionLocal() as session:
            history_predict = HistoryPredictions(
                type_product=source_features.get("TYPE_PRODUCT"),
                project=source_features.get("PROJECT"),
                division_name=source_features.get("DIVISION_NAME"),
                standart_name=source_features.get("STANDART_NAME"),
                doc_type_name=source_features.get("DOC_TYPE_NAME"),
                type_work_name=source_features.get("TYPE_WORK_NAME"),
                functional_name=source_features.get("FUNCTIONAL_NAME"),
                type_doc_new=source_features.get("TYPE_DOC_NEW"),
                view_doc_new=source_features.get("VIEW_DOC_NEW"),
                operplan_labor=float(source_features.get("OPERPLAN_LABOR")),
                standart_labor=float(source_features.get("STANDART_LABOR")),
                plan_labor=float(source_features.get("PLAN_LABOR")),
                cash=float(source_features.get("CASH")),
                fact_labor_true=fact_labor_true,
                fact_labor_predict=float(fact_labor),
                error=error
            )
            session.add(history_predict)
            session.commit()
        return True, float(fact_labor)
    except Exception as e: return False, str(e)


def predict_test(work):
    try:
        data_test = pd.read_csv("data_set/data_set_11.08.25_2.csv", sep=";", decimal=",")
        test_encoded_data = [data_test.at[work.work_test, column] for column in parameters]
        test_num_data = [data_test.at[work.work_test, column] for column in num_parameters]
        features = {}

        for param,data in zip(parameters, test_encoded_data):
            encoded_value = label_encoders[param].transform([data])
            features[param] = encoded_value

        for param,data in zip(num_parameters, test_num_data):
            features[param] = data
        df = pd.DataFrame([features])
        fact_labor = model_cat_loaded.predict(df)
        return True, float(fact_labor)
    except Exception as e: return False, str(e)


def predict_test_plus(works_plus: list, data_test=None):
    if data_test is None:
        data_test = pd.read_csv("data_set/data_set_11.08.25_2.csv", sep=";", decimal=",")
    features_list=[]
    source_features_list=[]
    fact_true_list = []
    for i in works_plus:
        try:
            test_encoded_data = [data_test.at[i, column] for column in parameters]
            test_num_data = [data_test.at[i, column] for column in num_parameters]
            features = {}
            source_features = {}
            for param, data in zip(parameters, test_encoded_data):
                source_features[param] = data
                encoded_value = label_encoders[param].transform([data])
                features[param] = encoded_value

            for param, data in zip(num_parameters, test_num_data):
                features[param] = data
                source_features[param] = data
            fact_labor_true = None if "FACT_LABOR" not in source_features else float(source_features.get("FACT_LABOR"))
            fact_true_list.append(fact_labor_true)
            features_list.append(features)
            source_features_list.append(source_features)
        except Exception as e: print('Нет данных', e)
    df = pd.DataFrame(features_list)
    fact_labor_predict = model_cat_loaded.predict(df)
    results=[]
    with SessionLocal() as session:
        for feature, fact_true, fact_predict in zip(source_features_list, fact_true_list,fact_labor_predict):
            error = None
            if fact_true is not None:
                error = float(fact_predict - fact_true)
            results.append({
                'plan_labor': float(feature['PLAN_LABOR']),
                'fact_labor_true': fact_true,
                'fact_labor_predict': float(fact_predict),
                'error': error
            })

            history_predict = HistoryPredictions(
                type_product=feature.get("TYPE_PRODUCT"),
                project=feature.get("PROJECT"),
                division_name=feature.get("DIVISION_NAME"),
                standart_name=feature.get("STANDART_NAME"),
                doc_type_name=feature.get("DOC_TYPE_NAME"),
                type_work_name=feature.get("TYPE_WORK_NAME"),
                functional_name=feature.get("FUNCTIONAL_NAME"),
                type_doc_new=feature.get("TYPE_DOC_NEW"),
                view_doc_new=feature.get("VIEW_DOC_NEW"),
                operplan_labor=float(feature.get("OPERPLAN_LABOR")),
                standart_labor=float(feature.get("STANDART_LABOR")),
                plan_labor=float(feature.get("PLAN_LABOR")),
                cash=float(feature.get("CASH")),
                fact_labor_true=fact_true,
                fact_labor_predict=float(fact_predict),
                error=error
            )
            session.add(history_predict)
        session.commit()
    return results

