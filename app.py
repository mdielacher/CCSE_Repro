from flask import Flask, request, jsonify
import numpy as np
import mlflow
import mlflow.sklearn

# Create a Flask app for serving predictions
app = Flask(__name__)

# Define an endpoint for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data as JSON
        input_data = request.get_json()
        
        # Extract features from input data
        PLZ = input_data['PLZ']
        Fläche = input_data['Fläche']
        Liegenschaftstyp_Nummer = input_data['Liegenschaftstyp_Nummer']
        
        # Make predictions using the logged model
        model_uri = f"runs:/{mlflow.active_run().info.run_uuid}/liegenschaften_firstTry"  # Replace with your model name
        loaded_model = mlflow.sklearn.load_model(model_uri)
        prediction = loaded_model.predict(np.array([[PLZ, Fläche, Liegenschaftstyp_Nummer]]))
        
        # Return the prediction as JSON response
        return jsonify({"prediction": float(prediction[0])}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
    