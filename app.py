from flask import Flask, request, jsonify
import sqlite3




app = Flask(__name__)

@app.route('/api')
def hello_world():
    return 'API for weather data!'


conn = sqlite3.connect('weather.db', check_same_thread=False)




@app.route('/api/weather', methods=['GET'])
def get_weather():


    # get query parameters
    station_id = request.args.get('station_id')
    date = request.args.get('date')

    # get page parameters
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    
    # build the query
    query = 'SELECT * FROM weather_data'
    if station_id:
        query += f' WHERE station_id = {station_id}'
    if date:
        query += f' WHERE date = {date}'
    else:
        query += f' LIMIT {per_page} OFFSET {offset} '

    # execute the query
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    results = []
    
    for row in rows:
        results.append({
            'date': row[2],
            'station_id': row[1],
            'max_temp': row[3],
            'min_temp': row[4],
            'precipitation': row[5]
        })
    return jsonify(results)



@app.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():

    # get page parameters
    page = request.args.get('page', default=1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    # get query parameters
    station_id = request.args.get('station_id')


    # build the query
    query = 'SELECT * FROM weather_data_analysis'
    if station_id:
        query += f' WHERE station_id = {station_id}'
    else:
        query += f' LIMIT {per_page} OFFSET {offset} '


    # execute the query
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    results = []

    for row in rows:
        results.append({
            'year': row[0],
            'station_id': row[1],
            'avg_max_temp': row[2],
            'avg_min_temp': row[3],
            'total_precipitation': row[4]
        })
    return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)