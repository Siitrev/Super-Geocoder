
from flask import Flask, request, render_template, send_file
import pandas as pd
from geopy.geocoders import ArcGIS



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
    return send_file("yourFile.csv",as_attachment=True)

@app.route("/download",methods=["POST"])
def download():
    if request.method == "POST":
        file = request.files["file"]
        if allowed_ext(file.filename):
            nom = ArcGIS(user_agent="geocoder")
            
            df = pd.read_csv(file)
            if not ("Address" in df.columns or "address"  in df.columns):
                return render_template("wrong_column.html")
            
            if "address" in df.columns: df.rename(columns= {"address":"Address"})
            
            df["Latitude"] = [nom.geocode(x).latitude for x in df["Address"]]
            df["Longitude"] = [nom.geocode(x).longitude for x in df["Address"]]
            
            df.to_csv("yourFile.csv")
            
            return render_template("download.html",tables=[df.to_html(classes='data', header="true", border=0)])
        
        return render_template("wrong_ext.html")
        
        


if __name__ == "__main__":
    app.run(debug=True)