import os
import json
import requests
import csv
from flask import render_template, Flask, request

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
data_as_dict=data[0]

rates=data_as_dict.get("rates")

with open("rates.csv", "w", newline="", encoding='utf-8') as csvfile:
    fieldnames=["currency","code","bid","ask"]
    writer=csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    for i in rates:
        writer.writerow({"currency":i.get("currency"), "code":i.get("code"), "bid":i.get("bid"),"ask":i.get("ask")})


app=Flask(__name__)

@app.route("/exchange", methods=["GET", "POST"])

def exchange():
    output=""
    if request.method=="POST":
        data=request.form
        user_choice_currency=data.get("currency")
        amount=data.get("amount")
        for i in rates:
            if user_choice_currency==i.get("code"):
                price=float(amount)*i.get("ask")
                output=f"Koszt {amount}{user_choice_currency} to {round(price, 2)}PLN"

    return render_template("form.html", output=output)
if __name__ == '__main__':
    app.run(debug=True)