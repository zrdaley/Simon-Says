from flask import Flask, render_template
 
 
app = Flask(__name__)
 
@app.route("/")
def simon_says():
    return render_template('simon_says.html', sup="HELLO")
 
 
if __name__ == "__main__":
	app.run()