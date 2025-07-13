from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))
df = pd.read_csv('Cleaned Car.csv')

companies = sorted(df['company'].unique())
fuel_types = sorted(df['fuel_type'].unique())
year_range = sorted(df['year'].unique(), reverse=True)
car_models_map = df.groupby('company')['name'].unique().apply(list).to_dict()

@app.route('/')
def home():
    return render_template('index.html', 
                           companies=companies,
                           fuel_types=fuel_types,
                           years=year_range)

@app.route('/get_models/<company>')
def get_models(company):
    models = car_models_map.get(company, [])
    return jsonify(models)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        company = request.form['company']
        car_model = request.form['car_model']
        kms_driven = int(request.form['kilometers_driven'])
        year = int(request.form['year_of_purchase'])
        fuel_type = request.form['fuel_type']


        input_df = pd.DataFrame([[company, car_model, kms_driven, year, fuel_type]],
                                columns=['company', 'name', 'kms_driven', 'year', 'fuel_type'])
        prediction = model.predict(input_df)[0]

        return render_template('index.html',
                               companies=companies,
                               fuel_types=fuel_types,
                               years=year_range,
                               prediction=int(prediction))
    except Exception as e:
        return render_template('index.html',
                               companies=companies,
                               fuel_types=fuel_types,
                               years=year_range,
                               error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
