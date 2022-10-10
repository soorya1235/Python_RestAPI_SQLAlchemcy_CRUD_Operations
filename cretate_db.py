from flask import Flask, jsonify,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Myapp(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(500))
    toppings = db.Column(db.String(500))
    crust = db.Column(db.String(500))


class MyAppSchema(ma.Schema):
    class Meta:
        fields = ('order_id', 'size', 'toppings', 'crust')


my_app_schema = MyAppSchema(many=True)

@app.route("/")
def hello_world():
    return "Hello Worlddd"


'''
Get Data
'''
@app.route('/order')
def get_order():
    query = Myapp.query.all()
    result = my_app_schema.dump(query)
    return jsonify(result)


'''
Create
'''
@app.route('/order',methods=["post"])
def post_data():
    req = request.get_json()
    order_id=req["order_id"]
    size=req["size"]
    toppings=req["toppings"]
    crust=req["crust"]
    new_entry=Myapp(order_id=order_id,size=size,toppings=toppings,crust=crust)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for("get_order"))


'''
Delete
'''
@app.route('/order/<oid>',methods=["delete"])
def delete_data(oid):
    entry=Myapp.query.get_or_404(oid)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("get_order"))


'''
Update
'''
@app.route('/order/<oid>',methods=["PUT"])
def update_data(oid):
    req = request.get_json()
    entry = Myapp.query.get(oid)
    entry.size=req["size"]
    entry.toppings=req["toppings"]
    entry.crust=req["crust"]
    db.session.add(entry)
    db.session.commit()
    return redirect(url_for("get_order"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
