import os
from flask import Flask, render_template

app = Flask(__name__)

shelf = dict()

for author_folder, subs, files in os.walk('books'):
    for book_file in files:
        with open(os.path.join(author_folder, book_file), 'r') as textfile:
            text = str()
            book_name = book_file.format()[:-4]
            author_name = author_folder.format()[6:]
            for line in textfile:
                text += line
            if author_name not in shelf:
                shelf[author_name] = list()
            shelf[author_name].append([book_name, text])


@app.route("/")
def main():
    return render_template('index.html', shelf_source=shelf)


@app.route("/author/<name>")
def author(name):
    return render_template('author.html', shelf_source=shelf, author_name=name)


@app.route("/author/<name>/<book>")
def book(name, book):
    book_ind = 0
    for b in shelf[name]:
        if b[0] == book:
            break
        book_ind += 1
    return render_template('book.html', shelf_source=shelf, author_name=name, book_ind=book_ind)





































'''
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123@localhost/py_sweater'
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)

    def __init__(self, text, tags):
        self.text = text.strip()
        self.tags = [
            Tag(text=tag.strip()) for tag in tags.split(',')
        ]

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), nullable=False)

    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    message = db.relationship('Message', backref=db.backref('tags', lazy=True))
db.create_all()

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html', messages=Message.query.all())

@app.route('/add message', methods=['POST'])
def add_message():
    text = request.form['text']
    tag = request.form['tag']

    db.session.add(Message(text, tag))
    db.session.commit()

    return redirect(url_for('main'))
'''