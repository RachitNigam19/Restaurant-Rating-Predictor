from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# ✅ Load the trained model and Target Encoder
best_model_dt = joblib.load("models/Restaurant_rating.pkl")  # Your trained Decision Tree model
Tencoding = joblib.load("models/target_encoding.pkl")  # TargetEncoder used for categorical encoding

@app.route("/", methods=["GET", "POST"])
def predict():
    prediction = None
    if request.method == "POST":
        try:
            # ✅ Getting form data
            price_range = int(request.form["Enter the price range of the restaurant"])
            votes = int(request.form["No of Votes the Restaurants Got?"])
            city = request.form["In Which City Restaurant is Located 📍?"]
            cuisines = request.form["Enter the cuisines the restaurant has"]
            avg_cost = int(request.form["Enter the average cost for two at the restaurant"])
            has_table_booking = 1 if request.form["has_table_booking"] == "yes" else 0
            has_online_delivery = 1 if request.form["has_online_booking_option"] == "yes" else 0
            delivering_now = 1 if request.form["delivering now"] == "yes" else 0

            # ✅ Create a DataFrame for user input
            user_input_df = pd.DataFrame([[city, cuisines, avg_cost, has_table_booking, has_online_delivery, delivering_now, price_range, votes]],
                                         columns=['City', 'Cuisines', 'Average Cost for two', 'Has Table booking', 'Has Online delivery', 'Is delivering now', 'Price range', 'Votes'])

            # ✅ Apply Target Encoding using the trained encoder
            user_input_df[['City', 'Cuisines']] = Tencoding.transform(user_input_df[['City', 'Cuisines']])

            # ✅ Convert DataFrame to NumPy array for prediction
            user_input_array = user_input_df.to_numpy()

            # ✅ Make Prediction
            prediction = best_model_dt.predict(user_input_array)[0]  # Extracting single predicted value
            prediction = round(prediction, 1)  # Rounding to 1 decimal place

        except Exception as e:
            print(f"Error: {e}")
            prediction = "Invalid Input"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
