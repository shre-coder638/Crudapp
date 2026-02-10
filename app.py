from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)
app.app_context().push()
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)
db.create_all()


@app.route('/', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        if not name or not email:
            flash('Name and Email are required fields.', 'error')
            return redirect('/')
        new_employee = Employee(name=name, email=email)
        db.session.add(new_employee)
        db.session.commit()
        flash("Employee added successfully!", "success")
        return redirect("/")
    all_employees = Employee.query.all()
    return render_template('index.html', allemp=all_employees)

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/home')
def homepage():
    all_employees = Employee.query.all()
    return render_template('Home.html', allemp=all_employees)

@app.route("/delete/<int:id>")
def delete(id):
    employee = Employee.query.filter_by(id=id).first()
    if employee:
        db.session.delete(employee)
        db.session.commit()
        flash("Employee deleted successfully!", "success")
    else:
        flash("Employee not found.", "error")
    return redirect("/")

@app.route("/update/<int:id>", methods=['GET','POST'])
def update(id):
    employee = Employee.query.filter_by(id=id).first()
    if not employee:
        flash("Employee not found.", "error")
        return redirect("/")
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        if not name or not email:
            flash('Name and Email are required fields.', 'error')
            return render_template('update.html', Employee=employee)
        employee.name = name
        employee.email = email
        db.session.commit()
        flash("Employee updated successfully!", "success")
        return redirect("/")
    return render_template('update.html', Employee=employee)
if __name__ == '__main__':
    app.run(debug=True)