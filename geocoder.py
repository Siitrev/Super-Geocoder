from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download",methods=["POST"])
def download():
    if request.method == "POST":
        return render_template("download.html")


if __name__ == "__main__":
    app.run(debug=True)