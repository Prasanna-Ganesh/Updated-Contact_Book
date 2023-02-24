from flask import render_template,request,flash,redirect,url_for
from werkzeug.utils import secure_filename
from Prasanna_ContactForm.webforms import AdduserForm
from Prasanna_ContactForm import app,db
from Prasanna_ContactForm.models import Contact
import os

@app.route("/")
def index():
    return render_template("index.html")

@app.context_processor
def intro():
     form = AdduserForm()
     return dict(form=form)

@app.route("/add_user", methods=["GET","POST"])
def add_user():
    form =AdduserForm()
    if form.validate_on_submit():
        user = Contact(name= form.name.data,email=form.email.data,phno=form.phno.data)
        db.session.add(user)
        db.session.commit()
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.session.commit()
            flash('Contact & Image successfully uploaded')
            all=Contact.query.all()
            return render_template('all_contact.html', filename=filename,form=form,user=user,all=all)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
    return render_template('add_user.html',form=form)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route("/edit_user/<int:id>",methods=["GET","POST"])
def edit_user(id):
    contact_to_update = Contact.query.get(id)
    if request.method=="POST":
        contact_to_update.name = request.form['name']
        contact_to_update.phno = request.form['phno']
        contact_to_update.email = request.form['email']
        try:
            db.session.commit()
            all = Contact.query.all()
            if 'contact_to_update.file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['contact_to_update.file']
            if file.filename == '':
                flash('No image selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                db.session.commit()
                flash('Contact & Image successfully updated')
                return render_template('all_contact.html', filename=filename,all=all)
            else:
                flash('Allowed image types are - png, jpg, jpeg, gif')
                return redirect(request.url)
            flash("Contact Edited successfully", "success")

            return redirect("/index")
        except:
            return "There was an Problem in updating"
    else:
        return render_template('edit_user.html',contact_to_update=contact_to_update)

    return render_template('edit_user.html')

@app.route("/delete_user",methods=["GET","POST"])
def delete_user():
    if request.method=="POST":
        name = request.form['name']
        d = Contact.query.filter_by(name=name).first()
        db.session.delete(d)
        db.session.commit()
        all=Contact.query.all
        flash("Contact Deleted successfully", "warning")
        return redirect(url_for("list"),all=all)
    else:
        flash("Contact Not Found","dark")
    return render_template('delete_user.html')
@app.route("/delete_user_id<int:id>",methods=["GET","POST"])
def delete_user_id(id):
    del_by_id = Contact.query.get(id)
    try:
        db.session.delete(del_by_id)
        db.session.commit()
        flash("Contact Deleted Successfully")
        return redirect("/all_contact")
    except:
        return "There was an problem while deleting"

    return render_template('delete_user_id.html',del_by_id=del_by_id)

@app.route("/list.html")
def list():
    page = request.args.get('page', 1, type=int)
    all = Contact.query.order_by(Contact.name).paginate(page=page, per_page=5)
    return render_template('list.html', all=all)

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if Contact.query.filter(Contact.name == request.args.get("name")):
            name = request.args.get("name")
            a = Contact.query.filter_by(name=name).all()
            db.session.commit()
            return render_template('search.html', all=a)

        else:
            flash('No such contact', 'error')
            return render_template('index.html')

    return render_template('search.html')


@app.route("/all_contact")
def all_contact():
    all = Contact.query.all()
    return render_template('all_contact.html',all=all)

if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)
