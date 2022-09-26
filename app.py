from flask import Flask, render_template, jsonify
import json
import requests
from flask import request, Response, redirect, url_for
from datetime import date 
import os
import pandas as pd
import gspread as gs
import xendit
from xendit import Invoice
from csv import writer
import webbrowser



xendit.api_key = "xnd_development_8pMOeEGQZsU7nniCemOfYX9A7c8pzVo7atEdecbo7odP5XzWapMdftLNgUieayL"

gsheet_id = '1j68c4eLXfZHqtP8-p1OVOa9dSumjQQTdJ2ouPYRLSOs'
sheet_name = 'data'

gsheet_url = 'https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}'.format(gsheet_id, sheet_name)
# df = pd.read_csv(gsheet_url)
# a = df.head()


app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():

    nama = request.form.get('nama')
    nominal = request.form.get('nominal')
    if nama:
        create_invoice = Invoice.create(
        external_id=nama,
        amount=nominal,
        payer_email="fery@domain.com",
        description="fery & putri wedding",
        )

        data = f'{create_invoice.invoice_url}'

        # webbrowser.open_new_tab(data)

        return redirect(data)

    return render_template('index.html')
    

@app.route('/create-payment')
def create_payment():
    # create
    create_invoice = Invoice.create(
    external_id="fery-6",
    amount=20000,
    payer_email="fery@domain.com",
    description="fery & putri wedding",
    )

    # print(create_invoice.invoice_url)

    # get
    invoice = Invoice.get(
    invoice_id=create_invoice.id,
    )
    print(invoice)

    return "ok"



@app.route('/payment', methods=["POST"])
def payment():
    xenditXCallbackToken = 'qucKGWOCHHGQfbpogv5a2IhJLGXwOgO9Vo1ofCk0xz2gQkTK'
    data = []
    headers = request.headers['x-callback-token']
    reqHeaders = request.get_json()
    print(headers)
    xIncomingCallbackTokenHeader = headers if headers else ""

    if xIncomingCallbackTokenHeader == xenditXCallbackToken:

        id = reqHeaders['id']
        external_id = reqHeaders['external_id']
        status = reqHeaders['status']

        data.append({
            'id': id,
            'status': status,
            'externalId': external_id

        })
        print(data)
        
    else:
    # Request is not from xendit, reject and throw http status forbidden
        response = Response(status=403)
        response(403)

    responsess = Response(status=200)
    return responsess



if __name__ == "__main__":
    app.run(debug=True)
