# モジュール読み込み
from flask import Flask, render_template, request
import mysql.connector
import unicodedata

app = Flask(__name__)


# db接続情報
def conn_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='a8119002',
        db='yacht',
    )
    return conn


# index.htmlを表示
@app.route('/index.html')
def index():
    return render_template('index.html')


# show.htmlを表示
@app.route('/show.html')
def show():
    return render_template('show.html')


# index.html postで受け取る
@app.route('/input', methods=['post'])
def input():
    place = request.form.get('place')
    direction = request.form.get('direction')
    speed = request.form.get('speed')
    wave = request.form.get('wave')
    weather = request.form.get('weather')
    practice = request.form.get('practice')
    others = request.form.get('others')
    data = [place, direction, speed, wave, weather, practice, others]
    try:
        sql = """insert into test_wind_data (place, direction, speed, wave, weather, practice, others) values(%s, %s, %s, %s, %s, %s, %s);"""
        conn = conn_db()
        cursor = conn.cursor()
        cursor.execute(sql, (data))
        conn.commit()
        print('input成功です')
    except (mysql.connector.errors.ProgrammingError) as e:
        print('書き込みエラーだぜ')
        print(e)
    return render_template('end.html')


# index.html postで受け取る テスト
# @app.route('/index', methods=['post'])
# def input():
#     place = request.form.get('place')
#     direction = request.form.get('direction')
#     speed = request.form.get('speed')
#     wave = request.form.get('wave')
#     weather = request.form.get('weather')
#     practice = request.form.get('practice')
#     others = request.form.get('others')
#     try:
#         sql = """select * from test_wind_data where place = %s and direction = %s and speed = %s and wave = %s and weather = %s and practice = %s and others = %s;"""
#         conn = conn_db()
#         cursor = conn.cursor()
#         cursor.execute(sql, (place, direction, speed, wave, weather, practice, others))
#         rows = cursor.fetchall()
#         print('テスト成功です')
#     except (mysql.connector.errors.ProgrammingError) as e:
#         print('テストエラーだぜ')
#         print(e)
#     return render_template('index.html', rows=rows)


# index.html postで受け取る テスト2
# @app.route('/input', methods=['post'])
# def input():
#     try:
#         place = request.form.get('place')
#         direction = request.form.get('direction')
#         data = [place, direction]
#         sql = """insert into test_wind_data (place, direction, speed, wave, weather, practice, others) values(%s, %s, 4, 2.0, '快晴', '', '');"""
#         conn = conn_db()
#         cursor = conn.cursor()
#         cursor.execute(sql, (data))
#         conn.commit()
#         print('input成功です')
#     except (mysql.connector.errors.ProgrammingError) as e:
#         print('書き込みエラーだぜ')
#         print(e)
#     return render_template('end.html')


# show.html postで受け取る
@app.route('/show', methods=['post'])
def serch():
    date = request.form.get('date')
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    place = request.form.get('place')
    try:
        sql = """select hour(datetime), minute(datetime), place, direction, speed, wave, weather, practice, others from test_wind_data where year(datetime) = %s and month(datetime) = %s and day(datetime) = %s and place = %s ;"""
        conn = conn_db()
        cursor = conn.cursor()
        cursor.execute(sql, (year, month, day, place))
        rows = cursor.fetchall()
        print('select成功です')
    except (mysql.connector.errors.ProgrammingError) as e:
        print('読み込みエラーだぜ')
        print(e)
    return render_template('show.html', rows=rows)


# 呪文
if __name__ == "__main__":
    app.run(debug=True)
