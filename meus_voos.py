from flask import Flask
from flask import render_template

from pyinfraero.airport import Airport

app = Flask(__name__)
#url_for('static', filename='style.css')

@app.route('/')
def index():
    voos = Airport("SBGL").get_flights()
    return render_template('aeroporto.html', voos=voos)

@app.route('/aeroporto/<airport_code>')
def aeroporto(airport_code):
   voos = Airport("SBGL").get_flights()
   return render_template('aeroporto.html', locals() )

if __name__ == '__main__':
    app.debug = True
    app.run() #app.run(host='0.0.0.0')
    
    