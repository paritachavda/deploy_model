import pandas as pd
from flask import request, jsonify, Blueprint
import pickle
from data_preprocessing import preprocess_data

# Create Flask Blueprint
prediction_api = Blueprint('prediction_api', __name__)

# Load model
with open('./model/model.pkl','rb') as mod:
    model = pickle.load(mod)


@prediction_api.route('/predict', methods=['POST'])
def predict():

    # Request json data
    data = pd.DataFrame(request.json)

    # Prepare the data for model
    data = preprocess_data(data)

    # Make prediction
    prediction = model.predict(data)
    # Create labels based on predictions (Thresold specified by business partner)
    label = [1 if i >= 0.712 else 0 for i in prediction]
    # Return the required result
    return jsonify({'Probability': list(prediction), 'Label': list(label), 'Variables': list(data.columns)})
