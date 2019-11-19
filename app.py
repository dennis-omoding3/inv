from flask import Flask, render_template, request, redirect, \
    url_for  # when you want to serve html file and pass the file as a string
from flask_sqlalchemy import SQLAlchemy
import pygal
import psycopg2
from update_record import New_stock

from configs import Development

# flask object
app = Flask(__name__)
app.config.from_object(Development)

# sqlalchemy instance
db = SQLAlchemy(app)  # pass the name of the flask object ie app

from models.inventories import InventoryModel
from models.sales import SalesModel


@app.before_first_request
def create_table():
    db.create_all()


# home page


@app.route('/', methods=['GET'])  # home route by default i.e /
def hello_world():
    pie_chart = pygal.Pie()
    pie_chart.title = 'inventory charts'
    pie_chart.add('products', InventoryModel.getTypeCount("product"))
    pie_chart.add('services', InventoryModel.getTypeCount("service"))
    pie_type = pie_chart.render_data_uri()

    conn = psycopg2.connect("dbname='test100' user='postgres' host='localhost' password='colonel3' port=5433")
    cur = conn.cursor()
    cur.execute("""SELECT (sum(i.bp*s.sl_qt)) as subtotal, extract( month from s.time_created ) as sales_month from sales as s join inventories as i on s.inv_id=i.id group by sales_month order by sales_month """)
    rows = cur.fetchall()

    months=[ 'jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    sales=[]
    for row in rows:
        # x.append(row[1])
        sales.append(row[0])
    line_chart = pygal.Bar()
    line_chart.title = 'monthly sales data'
    line_chart.x_labels = map(str, months)
    line_chart.add('subtotal', sales)
    line_chart=line_chart.render_data_uri()





    return render_template("index.html", pie_type=pie_type, line_chart=line_chart)






@app.route('/product')  # creates a new route
def product():
    return render_template("product.html")


@app.route('/inventories', methods=['GET', 'POST'])
def inventories():
    invquery = InventoryModel.query.all()

    if request.method == 'POST':
        inv_name = request.form['inventory']
        inv_type = request.form['type']
        bp = request.form['buying_price']
        sp = request.form['selling_price']
        stock = request.form['stock']
        rp = request.form['reorder_point']

        inv = InventoryModel(inv_name=inv_name, inv_type=inv_type, bp=bp, sp=sp, stock=stock, rp=rp)
        db.session.add(inv)

        db.session.commit()
        print("success")


        return redirect(url_for('inventories'))


    return render_template('inv.html', inventories=invquery)





@app.route('/sales', methods=['POST'])
def sales():
    slsquery = SalesModel.query.all()
    if request.method == 'POST':
        sl_qt = request.form['quantity']
        inv_id = request.form['inv_id']

        if InventoryModel.update_stock(id=inv_id, sl_qt=int(sl_qt)):
            print("success")
            sls = SalesModel(sl_qt=sl_qt, inv_id=inv_id)

            db.session.add(sls)
            db.session.commit()
        else:
            print("insufficient stock")


        print("success")
        return redirect(url_for('inventories'))


@app.route('/edit', methods=['POST'])
def edit_record():
    if request.method == 'POST':
        id = request.form['inv_id']
        inv_name = request.form['inventory']
        inv_type = request.form['type']
        bp = request.form['buying_price']
        sp = request.form['selling_price']
        stock = request.form['stock']
        rp = request.form['reorder_point']

        InventoryModel.edit_record(id=id, inv_name=inv_name, inv_type=inv_type, bp=bp, sp=sp, stock=stock, rp=rp)
        print('success')

        return redirect(url_for('inventories'))


# @app.route('/delete', methods=['GET','POST'])
# def delete_record():
#     invquery = InventoryModel.query.all()
#
#     if request.method == 'POST':
#         inv_name = request.form['inventory']
#         inv_type = request.form['type']
#         bp = request.form['buying_price']
#         sp = request.form['selling_price']
#         stock = request.form['stock']
#         rp = request.form['reorder_point']
#
#         InventoryModel.delete_entry(id=id, inv_name=inv_name, inv_type=inv_type, bp=bp, sp=sp, stock=stock, rp=rp)
#
#         print("record deleted!")


        # view sales


@app.route('/Inventory/<int:id>/Sales')
def view_sales(id):
    inv = InventoryModel.query.filter_by(id=id).first()
    inv_sales = inv.sales
    return render_template('Sales.html', sales=inv_sales, name=inv.inv_name)


if __name__ == '__main__':
    app.run(debug=True)
