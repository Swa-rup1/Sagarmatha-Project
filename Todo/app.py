from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}-{self.title}"


with app.app_context():
    db.create_all()



@app.route("/",methods=["GET","POST"])
def homo_todo():
    # allTodo = db.session.execute(db.select(Todo)).scalars().all()
    allTodo = Todo.query.all()
    if(request.method=="POST"):
        queryStr=request.form["search"]
        posts=Todo.query.filter(Todo.title.contains(queryStr)).all()
        print(posts)
        return render_template('index.html', allTodo=posts)


    return render_template('index.html', allTodo=allTodo)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/create-todo", methods=['GET', 'POST'])
def create_todo():
    if (request.method == "POST"):
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

        return redirect("/")


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update_todo(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if (request.method == "POST"):
        title = request.form['title']
        desc = request.form['desc']
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()

        return redirect("/")
    return render_template('update.html', todo=todo)


@app.route("/delete/<int:sno>", methods=['GET'])
def delete_todo(sno):
    # todo = db.session.execute(db.select(Todo).filter_by(sno=sno)).scalar_one()
    todo = Todo.query.filter_by(sno=sno).first()
    print(todo)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

