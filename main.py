from flask import Flask, render_template, redirect, url_for, request
import mysql.connector
import pickle
import numpy as np
import pandas as pd
import os


app = Flask(__name__)
# app.config["UPLOAD_FOLDER"]='static/'
classifier = pickle.load(open("diabetes_prediction.pkl","rb"))
scaler = pickle.load(open("scaler.pkl","rb"))

# app.config["UPLOAD_FOLDER"]='static/'
model = pickle.load(open("heart_disease_predictor.pkl","rb"))



conn = mysql.connector.connect(host="localhost", password="Saif@9696", user="root", database="saif_db")
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/tc")
def tc():
    return render_template("tc.html")

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login_validation",methods=["POST"])
def login_validation():
    email = request.form.get("email")
    password = request.form.get("password")

    cursor.execute(""" SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}' """
                   .format(email, password)) 
    
    users = cursor.fetchall()
    if len(users)>0:
        return render_template('dashboard.html')
    else:
        return render_template('login.html')
    
@app.route('/add_user', methods =['POST'])
def add_user():
    name =request.form.get("uname")
    email=request.form.get("uemail")
    password = request.form.get("upassword")

    cursor.execute(""" INSERT INTO `users` (`ID`,`name`,`email`,`password`)
                   VALUES(NULL, '{}', '{}', '{}')""".format(name,email,password))
    
    conn.commit()

    return "User registered Successfully"


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route('/disindex')
def disindex():
    return render_template("disindex.html")

@app.route('/diabetes')
def diabetes():
    return render_template("diabetes.html")

@app.route('/heart')
def heart():
    return render_template("heart.html")   


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == 'POST':
        preg = int(request.form['pregnancies'])
        glucose = int(request.form['glucose'])
        bp = int(request.form['bloodpressure'])
        st = int(request.form['skinthickness'])
        insulin = float(request.form['insulin'])
        bmi = float(request.form['bmi'])
        dpf = float(request.form['dpf'])
        age = int(request.form['age'])

        input_data=(preg,glucose,bp,st,insulin,bmi,dpf,age)

# change the input data to numpyarray
        input_data_as_numpy_array=np.asarray(input_data)

# reshape the arrayas we are predicting for one instance
        input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

#standardized the input data
        std_data = scaler.transform(input_data_reshaped)
        print(std_data)

        prediction=classifier.predict(std_data)
        print(prediction)

        if (prediction[0]==0):
                result= "Patient has a low risk of Diabetes"
        else:
                result= "Patient has a high risk of Diabetes"

        return render_template('diab_result.html', result = result)


@app.route("/predictheart", methods=['GET', 'POST'])
def predictheart():
    if request.method == 'POST':
        age = int(request.form['age'])
        sex = int(request.form['sex'])
        CP = int(request.form.get ['Chest pain'])
        BP = int(request.form['blood pressure'])
        cholestrol = int(request.form['cholestrol'])
        Blood_sugar = int(request.form['blood sugar'])
        restecg = int(request.form['sem'])
        Heart_rate = int(request.form['HR'])
        Exang = int(request.form['exercise induced'])
        Old_peak = int(request.form['old peak'])
        slope = int(request.form['slope'])
        CA = int(request.form['ca'])
        thal = int(request.form['thalassmia'])
    

        input_data = (age,sex,CP,BP,cholestrol,Blood_sugar,restecg,Heart_rate,Exang,
        Old_peak,slope,CA,thal)

        # chnage the input data to a numpy array
        input_data_as_numpy_array=np.asarray(input_data)

        # reshape the numpy array as we are predicting only one instance
        input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

        prediction =  model.predict(input_data_reshaped)
        print(prediction)

        if (prediction[0]==0):
            result1 = "Person has a low risk of Heart Disease."
        else:
            result1 = "Person has a high risk of Heart Disease."

        return render_template('heart_result.html', result1 = result1)

@app.route("/logout")        
def logout():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True) 
