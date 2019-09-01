from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello!\n'

@app.route("/commodity",methods = ["GET"])
def getData():
    # Show json with date and price of currency
    start_date = pd.Timestamp(request.args.get('start_date'))
    end_date = pd.Timestamp(request.args.get('end_date'))
    commodity_type = request.args.get('commodity_type')
    if not commodity_type or not commodity_type in ['gold', 'silver'] :
        return 'commodity_type is not correct. Please enter a correct currency'
    path = 'price_data_' + commodity_type + '.csv'
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    dfrows = df.loc[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    mean = dfrows.mean()
    var = dfrows.var()
    varvalue = float("{0:.2f}".format(var['Price']))
    meanval = float("{0:.2f}".format(mean['Price']))
    dict_price = {}
    for row in dfrows.iterrows():
        Date = row[1]['Date']
        price = row[1]['Price']
        dict_price[Date._date_repr] = float("{0:.3f}".format(price))
    message = {
        'data' : dict_price,
        'mean' : meanval,
        'variance' : varvalue
    }
    return jsonify(message)

if __name__ =='__main__':
    app.run(port=8080, debug=True)
