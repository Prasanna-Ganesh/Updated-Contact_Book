from Prasanna_ContactForm import db
class Contact(db.Model):
    __tablename__ = "contact"

    id = db.Column(db.Integer,primary_key=True,)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    phno = db.Column(db.Integer)
    image_file = db.Column(db.String(20))

    def __repr__(self):
        return "{} {} {} {} {}".format(self.name, self.email, self.phno, self.image_file)
db.create_all()