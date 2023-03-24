from app import db, Group

group1 = Group(name="Vilnius")
group2 = Group(name="Kaunas")
group3 = Group(name="Klaipeda")
group4 = Group(name="Panevezys")

db.create_all()
db.session.add_all([group1, group2, group3, group4])
db.session.commit()