from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://root:secret@localhost:5432/postgres"
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}, title {self.title}, description {self.description}, done {self.done}>'


@app.route('/')
def index():
    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks)


@app.route('/create', methods=['GET', 'POST'])
def create():
    task = Task()
    if request.method == 'POST':
        task = Task.query.order_by(Task.id.desc()).first()
        if task is None:
            task_id = 0
        else:
            task_id = Task.query.order_by(Task.id.desc()).first().id + 1
        title = request.form['title']
        description = request.form['description']
        done = request.form.get('done') == 'on'
        task = Task(id=task_id, title=title, description=description, done=done)
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('create.html', task=task)


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        done = request.form.get('done') == 'on'

        if title:
            task.title = title
        if description:
            task.description = description
        task.done = done

        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)


@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('delete.html', task=task)


# Run the flask app
if __name__ == '__main__':
    app.run()
