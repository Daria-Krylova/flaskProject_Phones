from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


# Установите соединение с базой данных
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Vintage38",
            database="mobile_phones"
        )
        return connection
    except mysql.connector.Error as err:
        print("Ошибка при подключении к базе данных:", err)
        return None


# Добавление нового мобильного телефона
def add_phone(connection, manufacturer, model, release_year, screen_size):
    try:
        cursor = connection.cursor()
        sql = "INSERT INTO phones (manufacturer, model, release_year, screen_size) VALUES (%s, %s, %s, %s)"
        values = (manufacturer, model, release_year, screen_size)
        cursor.execute(sql, values)
        connection.commit()
        cursor.close()
        print("Мобильный телефон успешно добавлен.")
    except mysql.connector.Error as err:
        print("Ошибка при добавлении мобильного телефона:", err)


# Получение списка всех мобильных телефонов
def get_all_phones(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM phones")
        phones = cursor.fetchall()
        cursor.close()

        if not phones:
            return []
        else:
            return phones
    except mysql.connector.Error as err:
        print("Ошибка при получении данных из базы данных:", err)
        return []


# Главная страница
@app.route('/')
def index():
    connection = connect_to_database()
    if connection:
        return render_template('index.html')
    else:
        return "Ошибка при подключении к базе данных."


# Обработчик для добавления мобильного телефона
@app.route('/add_phone', methods=['POST'])
def add_phone_view():
    manufacturer = request.form.get('manufacturer')
    model = request.form.get('model')
    release_year = request.form.get('release_year')
    screen_size = request.form.get('screen_size')

    connection = connect_to_database()
    if connection:
        add_phone(connection, manufacturer, model, release_year, screen_size)
    return redirect(url_for('list_phones'))


# Страница со списком мобильных телефонов
@app.route('/list_phones')
def list_phones():
    connection = connect_to_database()
    if connection:
        phones = get_all_phones(connection)
        return render_template('list_phones.html', phones=phones)
    else:
        return "Ошибка при подключении к базе данных."


if __name__ == "__main__":
    app.run(debug=True)
