from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection, init_db

app = Flask(__name__)

init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    isbn = request.form['isbn']
    category = request.form['category']

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO books (title, author, isbn, category, status) VALUES (?, ?, ?, ?, ?)',
                     (title, author, isbn, category, 'Available'))
        conn.commit()
    except Exception as e:
        print(f"Error adding book: {e}")
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_book(id):
    title = request.form['title']
    author = request.form['author']
    isbn = request.form['isbn']
    category = request.form['category']
    status = request.form['status']

    conn = get_db_connection()
    conn.execute('''
        UPDATE books 
        SET title = ?, author = ?, isbn = ?, category = ?, status = ? 
        WHERE id = ?
    ''', (title, author, isbn, category, status, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_book(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
