from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from joblib import load

model = load("titanic_survival_prediction_model.pkl")

app = Flask(__name__)
CORS(app)

def predict_survival(pclass, sex, Fare, SibSp, Age):
    # Convert sex to binary
    sex = 1 if sex == 'male' else 0

    features = pd.DataFrame({
        'Pclass': [pclass],
        'Sex': [sex],
        'Fare': [Fare],
        'SibSp': [SibSp],
        'Age': [Age]
    })

    prediction = model.predict(features)
    return 'Survived' if prediction == 1 else 'Did not survive'

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    pclass = data.get('pclass')
    sex = data.get('sex')
    Fare = data.get('Fare')
    SibSp = data.get('SibSp')
    Age = data.get('Age')
    if pclass is None or sex is None or Fare is None or SibSp is None:
        return jsonify({'error': 'Missing data'}), 400

    result = predict_survival(pclass, sex, Fare, SibSp, Age)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
