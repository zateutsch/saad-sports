from flask import Flask, render_template, request
import src.livebettingmachine as BettingMachine
app = Flask(__name__)



@app.route('/', methods=['POST', 'GET'])
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

    if request.method == 'POST':
        game_data = request.form
        seconds = int(game_data["seconds"])
        minutes = int(game_data["minutes"])
        time = str(minutes) + ":" + (str(seconds) if seconds > 9 else ("0" + str(seconds))) + ".0"
        quarter = int(game_data["quarter"])
        awayscore = int(game_data["awayscore"])
        homescore = int(game_data["homescore"])
        livespread = float(game_data["livespread"])
        openspread = float(game_data["openspread"])

        print(game_data)

        if(quarter != 0): 
            bet_result = BettingMachine.LiveBetSpread(quarter, time, awayscore, homescore, livespread, openspread)

        print(bet_result)
        
    return render_template("index.html", data=game_data, result=bet_result)

if __name__ == '__main__':
    app.run(debug=True)