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




app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():

    nama = request.form.get('nama')
    nominal = request.form.get('nominal')
    if nama:
        create_invoice = Invoice.create(
        external_id=nama,
        amount=nominal,
        payer_email=f"{nama}@domain.com",
        description="Putri & Fery Wedding",
        )
       
        data = f'{create_invoice.invoice_url}'

        # webbrowser.open_new_tab(data)

        return redirect(data)

    return render_template('index.html')
    

@app.route('/data-orang-baik')
def data_gift():

    # get
    data = []
    invoices = Invoice.list_all()
    for x in invoices:
        data.append({
            "id": x.id,
            "nama": x.external_id,
            "status": x.status,
            "amount": "Rp {:,}".format(x.amount),
            "total": x.amount
        })
    
    filtered = [x for x in data if (x['status'] == 'PAID')]

    df = pd.DataFrame(filtered)
    total = df['total'].sum()
    total = "Rp {:,}".format(total)
    print(total)

    
    # return jsonify(filtered)
    return render_template('data.html', data=filtered, total=total)



# @app.route('/data-kehadiran')
# def data_kehadiran():

#     # get
#     data = []
#     gsheet_id = '1j68c4eLXfZHqtP8-p1OVOa9dSumjQQTdJ2ouPYRLSOs'
#     sheet_name = 'data'

#     gsheet_url = 'https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}'.format(gsheet_id, sheet_name)
#     df = pd.read_csv(gsheet_url)

#     json_records = df.to_json(orient ='records')

#     data = json.loads(json_records)
 
    
#     return "ok"
#     # return render_template('data.html', data=data)



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
