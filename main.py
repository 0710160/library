from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

#db = sqlite3.connect("books-collection.db")
#cursor = db.cursor()
#cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, "
#               "title varchar(250) NOT NULL UNIQUE, "
#               "author varchar(250) NOT NULL, "
#               "rating FLOAT NOT NULL)")
#cursor.execute("INSERT INTO books VALUES(1, 'Siddhartha', 'Hermann Hesse', '10')")
#db.commit()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_books.sqlite3'
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)


if not os.path.isfile("sqlite://new_books.sqlite3"):
    db.create_all()


#all_books = []


@app.route('/')
def home():
    #print(all_books)
    #if all_books == []:
    #    return render_template("index.html", books="empty")
    #else:
    all_books = [book for book in db.session.query(Books).all()]
    return render_template("index.html", books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        rating = request.form["rating"]
        new_book = Books(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        all_books = [book for book in db.session.query(Books).all()]
        return render_template("index.html", books=all_books)
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)

