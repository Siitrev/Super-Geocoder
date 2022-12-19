
from flask import Flask, request, render_template, send_file
import pandas as pd
from geopy.geocoders import ArcGIS
import datetime



app = Flask(__name__)

def allowed_ext(filename:str):
    if filename.endswith(".csv"):
        return True
    return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download_file")
def download_file():
    return send_file(filename,as_attachment=True)

@app.route("/download",methods=["POST"])
def download():
    global filename
    if request.method == "POST":
        file = request.files["file"]
        if allowed_ext(file.filename):
            nom = ArcGIS(user_agent="geocoder")
            
            df = pd.read_csv(file)
            if not ("Address" in df.columns or "address"  in df.columns):
                return render_template("wrong_column.html")
            
            if "address" in df.columns: df.rename(columns= {"address":"Address"})
            
            df["coordinates"] = df["Address"].apply(nom.geocode)
            
            df["Latitude"] = df["coordinates"].apply(lambda x: x.latitude if x!= None else None)
            df["Longitude"] = df["coordinates"].apply(lambda x: x.longitude if x!= None else None)
            
            df = df.drop("coordinates",1)
            filename = datetime.datetime.now().strftime("uploads/"+"%Y-%m-%d-%H-%S-%d"+".csv")
            df.to_csv(filename, index=None)
            
            return render_template("download.html",tables=[df.to_html( header="true", border=0)])
        
        return render_template("wrong_ext.html")
        
        


if __name__ == "__main__":
    app.run(debug=True)