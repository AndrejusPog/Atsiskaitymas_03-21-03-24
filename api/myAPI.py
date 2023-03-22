from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'groups.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Za2sd12dA2Sasd21dwaasdsasddASDsdadsd21'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# My DB OBJ
class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column("groupname", db.String)
    
    
class Bill(db.Model):
    __tablename__ = 'bill'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column("description", db.String)
    amount = db.Column("amount", db.Integer)

    
# Schema
class GroupSchema(ma.Schema):
    class Meta:
        fields = ('id', 'groupname')

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)


class BillSchema(ma.Schema):
    class Meta:
        fields = ('description', 'amount')

bill_schema = BillSchema()
bill_schema = BillSchema(many=True)


# Crud
@app.route('/group', methods=['POST'])
def add_group():
    db.create_all()
    groupname = request.json['groupname']
    new_group = Group(groupname=groupname)
    db.session.add(new_group)
    db.session.commit()
    return group_schema.jsonify(new_group)

# cRud
@app.route('/group', methods=['GET'])
def get_all_groups():
    db.create_all()
    all_groups = Group.query.all()
    rezultatas = groups_schema.dump(all_groups)
    return jsonify(rezultatas)

# cRud
@app.route('/group/<id>', methods=['GET'])
def get_group(id):
    db.create_all()
    group = Group.query.get(id)
    return group_schema.jsonify(group)

# crUd
@app.route('/group/<id>', methods=['PUT'])
def amend_group(id):
    group = Group.query.get(id)
    group.groupname = request.json['groupname']
    db.session.commit()
    return group_schema.jsonify(group)

# cruD
@app.route('/group/<id>', methods=['DELETE'])
def delete_group(id):
    group = Group.query.get(id)
    db.session.delete(group)
    db.session.commit()
    return group_schema.jsonify(group)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
    db.create_all()