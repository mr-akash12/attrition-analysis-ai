
import joblib
import pandas as pd
from langchain.tools import tool

model = joblib.load("rf_pipeline_model.pkl")

@tool
def predict_employee_attrition(
    satisfaction_level: float,
    last_evaluation: float,
    number_project: int,
    average_montly_hours: int,
    time_spend_company: int,
    department: str,
    salary: str
):
    """
    Predict whether an employee will leave the company based on input features.
    """

    df = pd.DataFrame([[
        satisfaction_level,
        last_evaluation,
        number_project,
        average_montly_hours,
        time_spend_company,
        department,
        salary
    ]], columns=[
        'satisfaction_level','last_evaluation','number_project',
        'average_montly_hours','time_spend_company','Department','salary'
    ])

    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]

    return f"Prediction: {'Will Leave' if pred==1 else 'Will Stay'} (Confidence: {round(prob*100,2)}%)"