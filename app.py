import urllib.request
from flask import Flask, render_template, request
from models import Ciudad
from forms import CiudadForm
import urllib
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "weather_app_flask"

@app.route("/", methods=["GET","POST"])
@app.route("/index", methods=["GET","POST"])
@app.route("/index.html", methods=["GET","POST"])
def index():
    ciudadForm = CiudadForm(obj=Ciudad())
    ciudad = None
    no_encontrado = None
    if request.method == "POST" and ciudadForm.validate_on_submit():
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={ciudadForm.ciudad.data}&appid=55b37df780fc1295f42961f68c09a597"
        try:
            with urllib.request.urlopen(url) as respuesta:
                ciudad_data = json.load(respuesta)
            if ciudad_data:
                lat = ciudad_data[0]["lat"]
                lon = ciudad_data[0]["lon"]
                weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=55b37df780fc1295f42961f68c09a597"
                with urllib.request.urlopen(weather_url) as weather_data:
                    ciudad_a_buscar = json.load(weather_data)
                    ciudad = {"nombre":ciudadForm.ciudad.data, 
                        "pais":ciudad_data[0]["state"], 
                        "temperatura":round(ciudad_a_buscar["main"]["temp"] - 273.15, 2),
                        "presion":ciudad_a_buscar["main"]["pressure"],
                        "humedad":ciudad_a_buscar["main"]["humidity"]}
        except:
            return render_template("index.html", ciudad=ciudad, form=ciudadForm, error="No se encontro esa ciudad")
        if not ciudad:
            no_encontrado = "No se encontro esa ciudad"
    return render_template("index.html", ciudad=ciudad, form=ciudadForm, error=no_encontrado)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)