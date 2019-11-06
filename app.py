from flask import Flask,render_template #when you want to serve html file and pass the file as a string

app = Flask(__name__)


@app.route('/') #home route by default i.e /
def hello_world():
    return render_template("index.html")

@app.route('/product') #creates a new route
def product():
    return render_template("product.html")
@app.route('/inventories')
def inventories():
    return render_template('inv.html')


if __name__ == '__main__':
    app.run()
