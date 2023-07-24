from flask import Flask

app = Flask(__name__)

@app.route("/",methods= ["POST","GET","SET","DELETE","PUT"])
def a_pi():
    return {"API":"Response Positive"}



if __name__ == "__main__":
    app.run(debug=True,port=2000)

