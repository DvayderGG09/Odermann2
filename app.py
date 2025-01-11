import datetime
import os
import time

import flask_wtf
import wtforms
from flask import Flask, request, make_response, render_template, url_for, jsonify, redirect
import sqlite3
import bcrypt
import requests
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
from wtforms.validators import DataRequired, Length
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'your_secret_key'
ALLOWED_EXTENSIONS = {'png', 'jpg'}


class AddReviewForm(flask_wtf.FlaskForm):
    description = wtforms.TextAreaField(
        "Описание отзыва",
        render_kw={
            "id": "descriptionInput",
            "maxlength": 240,
            "placeholder": "Введите описание отзыва",
        },
        validators=[DataRequired(), Length(max=230)]
    )
    submit = wtforms.SubmitField(
        "Добавить отзыв",
        render_kw={"class": "SubmitAddReviewForm", "type": "submit"}
    )



def create():
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER,
            nickname TEXT,
            password TEXT,
            email TEXT,
            avatar TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            nickname TEXT,
            avatar TEXT,
            description TEXT,
            grade INTEGER
        )
    ''')
    db.commit()
    db.close()


create()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_pizza_names():
    url = "https://dodopizza.ru/peterburg"  # Убедитесь, что это правильный URL
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Ищем все секции с id 'guzhy'
        pizza_sections = soup.find_all('section', id='guzhy')

        pizzas = []
        id_pizzas = 1

        # Проходим по каждой секции
        for section in pizza_sections:
            # Находим все ссылки на пиццу в данной секции
            pizza_elements = section.select('article > main > div > a')

            for pizza in pizza_elements:
                # Извлекаем название пиццы
                name = pizza.get_text(strip=True)
                pizzas.append({'id': id_pizzas, 'name': name})
                id_pizzas += 1

        return pizzas
    else:
        print(f"Ошибка при подключении к сайту. Код ошибки: {response.status_code}")
        return []


# pizza_prices = get_pizza_names()
# print(pizza_prices)


@app.route('/', methods=['GET', 'POST'])
def index():
    nickname = request.cookies.get('nickname')
    password = request.cookies.get('password')
    email = request.cookies.get('email')

    if nickname and password:
        with sqlite3.connect('database.db') as db:
            c = db.cursor()
            c.execute("SELECT password FROM users WHERE nickname = ?", (nickname,))
            user = c.fetchone()
            if user and user[0] == password:
                return render_template("index.html", login=True, nickname=nickname)

    if email and password:
        with sqlite3.connect('database.db') as db:
            c = db.cursor()
            c.execute("SELECT password FROM users WHERE email = ?", (email,))
            user = c.fetchone()
            if user and user[0] == password:
                return render_template("index.html", login=True, nickname=nickname)

    return render_template("index.html")


@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html")


@app.route('/auth/profile')
def profile():
    nickname = request.cookies.get('nickname')
    password = request.cookies.get('password')
    email = request.cookies.get('email')

    if nickname and password:
        with sqlite3.connect('database.db') as db:
            c = db.cursor()
            c.execute("SELECT password FROM users WHERE nickname = ?", (nickname,))
            user = c.fetchone()
            if user and user[0] == password:
                c.execute("SELECT nickname, email, avatar FROM users WHERE nickname = ?", (nickname,))
                rows = c.fetchall()
                if rows:
                    nickname = [row[0] for row in rows]
                    email = [row[1] for row in rows]
                    avatar = [row[2] if row[2] is not None else "default-avatar.png" for row in rows]
                    data = list(zip(nickname, email, avatar))
                    return render_template("profile.html", login=True, data=data)

    if email and password:
        with sqlite3.connect('database.db') as db:
            c = db.cursor()
            c.execute("SELECT password FROM users WHERE email = ?", (email,))
            user = c.fetchone()
            if user and user[0] == password:
                c.execute("SELECT nickname, email, avatar FROM users WHERE email = ?", (email,))
                rows = c.fetchall()
                if rows:
                    nickname = [row[0] for row in rows]
                    email = [row[1] for row in rows]
                    avatar = [row[2] if row[2] is not None else "default-avatar.png" for row in rows]
                    data = list(zip(nickname, email, avatar))
                    return render_template("profile.html", login=True, data=data)

    return render_template("profile.html", login=False)


@app.route('/auth/login')
def login():
    return render_template("login.html")


# Проверка nickname
@app.route('/check-nickname', methods=['POST'])
def check_nickname():
    data = request.get_json()
    nickname = data.get("nickname", "")

    with sqlite3.connect('database.db') as db:
        c = db.cursor()
        c.execute("SELECT 1 FROM users WHERE nickname = ?", (nickname,))
        exists = c.fetchone() is not None

    return jsonify({"exists": exists})


# Проверка email
@app.route('/check-email', methods=['POST'])
def check_email():
    data = request.get_json()
    email = data.get("email")
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    exists = c.fetchone() is not None
    db.close()
    return jsonify({"exists": exists})


@app.route('/register-user', methods=['POST'])
def register_user():
    data = request.get_json()
    nickname = data.get("nickname")
    email = data.get("email")
    password = data.get("password")

    # Проверка, что все поля заполнены
    if not nickname or not email or not password:
        return jsonify({"success": False, "message": "Заповніть всі поля"}), 400

    # Открываем соединение с базой данных
    with sqlite3.connect('database.db') as db:
        c = db.cursor()

        # Проверка на существующий никнейм
        c.execute("SELECT 1 FROM users WHERE nickname = ?", (nickname,))
        if c.fetchone():
            return jsonify({"success": False, "message": "Нікнейм уже існує"}), 409

        # Получаем максимальный id и увеличиваем на 1 для нового пользователя
        c.execute("SELECT MAX(id) FROM users")
        max_id = c.fetchone()[0]
        new_id = (max_id + 1) if max_id else 1  # Если база пуста, id = 1

        # Добавляем нового пользователя в базу данных с новым id
        c.execute("INSERT INTO users (id, nickname, email, password) VALUES (?, ?, ?, ?)",
                  (new_id, nickname, email, password))
        db.commit()

        response = make_response(jsonify({"success": True}))
        response.set_cookie('nickname', nickname, max_age=60 * 60 * 24 * 30)  # збереження на 30 днів
        response.set_cookie('email', email, max_age=60 * 60 * 24 * 30)
        response.set_cookie('password', password, max_age=60 * 60 * 24 * 30)

    return jsonify({"success": True}), 201


@app.route('/check-login', methods=['POST'])
def check_login():
    data = request.get_json()
    login = data.get("login")
    password = data.get("password")
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute("SELECT email FROM users WHERE email = ?", (login,))
    email = c.fetchone()
    if email is not None:
        if email[0] == login:
            c.execute("SELECT password FROM users WHERE email = ?", (login,))
            data_password = c.fetchone()
            if data_password[0] == password:
                exists = "is-login"
                if not request.cookies.get('nickname') or not request.cookies.get(
                        'password') or not request.cookies.get('email'):
                    response = make_response(jsonify({"exists": exists}))
                    response.set_cookie('email', login, max_age=60 * 60 * 24 * 30)
                    response.set_cookie('password', password, max_age=60 * 60 * 24 * 30)
                    c.execute("SELECT nickname FROM users WHERE email = ?", (login,))
                    data_nickname = c.fetchone()
                    response.set_cookie('nickname', data_nickname[0], max_age=60 * 60 * 24 * 30)
                    return response
            else:
                exists = "wrong-password"
    else:
        c.execute("SELECT nickname FROM users WHERE nickname = ?", (login,))
        nickname = c.fetchone()
        if nickname is not None:
            if nickname[0] == login:
                c.execute("SELECT password FROM users WHERE nickname = ?", (login,))
                data_password = c.fetchone()
                if data_password[0] == password:
                    exists = "is-login"
                    if not request.cookies.get('nickname') or not request.cookies.get(
                            'password') or not request.cookies.get('email'):
                        response = make_response(jsonify({"exists": exists}))
                        response.set_cookie('nickname', login, max_age=60 * 60 * 24 * 30)
                        response.set_cookie('password', password, max_age=60 * 60 * 24 * 30)
                        c.execute("SELECT email FROM users WHERE nickname = ?", (login,))
                        data_email = c.fetchone()
                        response.set_cookie('email', data_email[0], max_age=60 * 60 * 24 * 30)

                        return response
                else:
                    exists = "wrong-password"
            else:
                exists = "no-login"
        else:
            exists = "no-login"
    db.close()
    return jsonify({"exists": exists})


@app.route('/comments/', methods=['GET', 'POST'])
def comments():
    form = AddReviewForm()
    if form.validate_on_submit():
        description = form.description.data
        star_full_count = int(request.form['starsSelected'])
        div_self_nickname = request.cookies.get('nickname', 'Гость')
        avatar_path = request.form.get('avatar_path')
        parsed_url = urlparse(avatar_path)
        avatar_name = os.path.basename(parsed_url.path)
        print(star_full_count, description, div_self_nickname, avatar_name)
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("INSERT INTO reviews (nickname, avatar, description, grade) VALUES (?, ?, ?, ?)",
                  (div_self_nickname, avatar_name, description, star_full_count))
        db.commit()
        db.close()
        return redirect(url_for('comments'))

    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute("SELECT nickname, grade, description, avatar FROM reviews")
    rows = c.fetchall()
    review_nickname = [row[0] for row in rows]
    review_grade = [int(row[1]) for row in rows]
    review_description = [row[2] for row in rows]
    review_avatar = [row[3] for row in rows]
    data = list(zip(review_nickname, review_grade, review_description, review_avatar))
    db.close()

    nickname = request.cookies.get('nickname')
    password = request.cookies.get('password')
    email = request.cookies.get('email')

    if nickname and password:
        with sqlite3.connect('database.db') as db:
            c = db.cursor()
            c.execute("SELECT password FROM users WHERE nickname = ?", (nickname,))
            user = c.fetchone()
            if user and user[0] == password:
                c.execute("SELECT avatar, nickname FROM users WHERE nickname = ?", (nickname,))
                rows = c.fetchall()
                user_avatar = [row[0] if row[0] is not None else "default-avatar.png" for row in rows]
                user_nickname = [row[1] for row in rows]
                user_data = list(zip(user_avatar, user_nickname))
                return render_template('comments.html', form=form, data=data, self_data=user_data, login=True)

    if email and password:
        with sqlite3.connect('database.db') as db:
            c = db.cursor()
            c.execute("SELECT password FROM users WHERE email = ?", (email,))
            user = c.fetchone()
            if user and user[0] == password:
                c.execute("SELECT avatar, nickname FROM users WHERE email = ?", (email,))
                rows = c.fetchall()
                user_avatar = [row[0] if row[0] is not None else "default-avatar.png" for row in rows]
                user_nickname = [row[1] for row in rows]
                user_data = list(zip(user_avatar, user_nickname))
                return render_template('comments.html', form=form, data=data, self_data=user_data, login=True)

    return render_template("comments.html", data=data, login=False)


@app.route('/updateAvatar', methods=['POST'])
def update_avatar():
    if 'avatar' not in request.files:
        return jsonify({'answer': False, 'message': 'Файл не найден'})

    file = request.files['avatar']
    email = request.form.get('email')

    if file.filename == '':
        return jsonify({'answer': False, 'message': 'Файл не был выбран'})

    if file and allowed_file(file.filename):
        db = sqlite3.connect('database.db')
        c = db.cursor()
        c.execute("SELECT avatar FROM users WHERE email = ?", (email,))
        row = c.fetchone()
        if row[0]:
            avatar_name = row[0]
            if os.path.exists(os.path.join('static', 'avatars', avatar_name)):
                os.remove(os.path.join('static', 'avatars', avatar_name))
        file_extension = os.path.splitext(secure_filename(file.filename))[1]
        timestamp = int(time.time())
        filename = f"{timestamp}{file_extension}"
        file_path = os.path.join('static/avatars', filename)
        file.save(file_path)
        c.execute("UPDATE users SET avatar = ? WHERE email = ?", (filename, email))
        db.commit()
        db.close()
        return jsonify({'answer': True})
    else:
        return jsonify({'answer': False, 'message': 'Доступны только эти форматы файла : png, jpg'})


@app.route('/AddReview', methods=['POST'])
def AddReview():
    nickname = request.form.get('nickname')
    avatar = request.form.get('avatar')
    description = request.form.get('description')
    grade = request.form.get('grade')
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute("INSERT INTO reviews (nickname, avatar, description, grade) VALUES (?, ?, ?, ?)",
              (nickname, avatar, description, grade))
    db.commit()
    db.close()

    return jsonify({'answer': True})


if __name__ == "__main__":
    app.run(debug=False)
