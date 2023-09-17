from flask import Flask, render_template
from app import create_app

app = create_app()

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")



if __name__ == '__main__':
	app.run(host="0.0.0.0", port=3000, debug=True)