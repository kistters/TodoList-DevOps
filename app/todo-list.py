from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mailer import Mailer, Email


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask:123@172.27.0.1/TODO_LIST'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config.update(
    #EMAIL SETTINGS
    MAILER_HOST='mailhog',
    MAILER_PORT=1025,
    MAILER_DEFAULT_SENDER='docker@docker.dev',
    MAILER_USERNAME = '',
    MAILER_PASSWORD = ''
    )

smtp = Mailer(app)
db   = SQLAlchemy(app)

class Task(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done    = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content    = content
        self.done       = False

    def __repr__(self):
        return '<Content %s>' % self.content

db.create_all()

@app.route('/')
def tasks_list():
    tasks = Task.query.all()
    return render_template('task-list.html', tasks=tasks)

@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
       return redirect('/')

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    mail = Email(
        subject= "Task %s" % (content),
        text=content,
        to=['maumau@docker.com', 'contato@docker.com'],
        from_addr='anonymous@kws.com'
    )

    smtp.send(mail)

    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/')
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect('/')

@app.route('/docker')
def docker():
    return render_template('form.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
