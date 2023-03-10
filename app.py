from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import path

app = Flask(__name__)
#sqlite -> replace with whatever you choice of db is
#/// = relative path
#//// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0) 
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # returns task and the id created with it
    # %r would = self.id
    def __repr__(self):
        return '<Task %r>' % self.id

# if db not created, create it
def create_database(app):
    if not path.exists('test.db'):
        with app.app_context():
            db.create_all()
        print('Created Database!')

create_database(app)


#---------routes---------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        #display all tasks in order of date created
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue updating your task'
    else:
        return render_template('update.html', task=task)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Issue deleting the task.'

if __name__=="__main__":
    app.run(debug=True)