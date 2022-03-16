from flask import Flask, render_template, request, jsonify
import src.livebettingmachine as BettingMachine
import os

app = Flask(__name__)

@app.route('/api')
def routes():
    routes = {
        "/api/nba/livespread": ["quarter", "time", "lead", "livespread", "openspread"]
    }

    return jsonify(routes)

@app.route('/api/nba/livespread')
def nbaLivespread():
    params = request.args
    quarter = int(params['quarter'])
    time = params['time']
    lead = float(params['lead'])
    livespread = float(params['livespread'])
    openspread = float(params['openspread'])

    p, r = BettingMachine.LiveBetSpread(quarter, time, lead, livespread, openspread)

    return jsonify({"probability": p, "count": len(r), "results": r})

@app.route('/ui/nba/livespread', methods=['POST', 'GET'])
def home():
    
    game_data = {
        "quarter": 0,
        "minutes": 12,
        "seconds": 00,
        "awayscore": 0,
        "homescore": 0,
        "livespread": 0,
        "openspread": 0,
    }

    bet_result = "booyah"
    results = []

    if request.method == 'POST':
        game_data = request.form
        seconds = int(game_data["seconds"])
        minutes = int(game_data["minutes"])
        time = str(minutes) + ":" + (str(seconds) if seconds > 9 else ("0" + str(seconds))) + ".0"
        quarter = int(game_data["quarter"])
        lead = int(game_data["awayscore"]) - int(game_data["homescore"])
        livespread = float(game_data["livespread"])
        openspread = float(game_data["openspread"])

        print(game_data)

        if(quarter != 0): 
            bet_result, results = BettingMachine.LiveBetSpread(quarter, time, lead, livespread, openspread)

        print(bet_result)
        
    return render_template("nba-livespread.html", data=game_data, result=bet_result, count=len(results))

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),  
        port=int(os.getenv('PORT', 4444))) 
