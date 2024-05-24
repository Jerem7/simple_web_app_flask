import datetime

from flask import Flask, render_template, request, make_response  #importowanie odpowiednich modułów
import os

app = Flask(__name__)


@app.route('/')  #dekorator, który definiuje funkcję, która ma być wywołana, gdy użytkownik wejdzie na stronę
def home():
    theme = request.cookies.get('theme', 'default')
    return render_template('base.html', theme=theme)


@app.route('/main')  #dekorator, który definiuje funkcję, która ma być wywołana, gdy użytkownik wejdzie na stronę główną
def main():
    student_data = {
        "name": "Jeremiasz",
        "surname": "Ż-K",
        "index": "xxxxxx"
    }
    theme = request.cookies.get('theme', 'default')  #ustawienie motywu na podstawie ciasteczka
    return render_template('main.html', student=student_data, theme=theme)


@app.route(
    '/times')  #dekorator, który definiuje funkcję, która ma być wywołana, gdy użytkownik wejdzie na stronę z czasem
def times():
    server_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    theme = request.cookies.get('theme', 'default')  #ustawienie motywu na podstawie ciasteczka
    return render_template('times.html', server_time=server_time, theme=theme)


@app.route(
    '/gallery')  #dekorator, który definiuje funkcję, która ma być wywołana, gdy użytkownik wejdzie na stronę z galerią
def gallery():
    image_folder = os.path.join('static', 'images')
    images = [f for f in os.listdir(image_folder) if
              os.path.isfile(os.path.join(image_folder, f)) and f.lower().endswith(('jpg', 'jpeg', 'png', 'gif'))]

    # logika paginacji obrazów
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_pages = (len(images) + per_page - 1) // per_page
    images_to_display = images[(page - 1) * per_page: page * per_page]

    theme = request.cookies.get('theme', 'default')  #ustawienie motywu na podstawie ciasteczka
    return render_template('gallery.html', images=images_to_display, page=page, total_pages=total_pages,
                           theme=theme)  #zwrócenie szablonu galerii z obrazami


@app.route('/set_theme/<theme>')
def set_theme(theme):  #funkcja, która ustawia ciasteczko z wybranym motywem
    response = make_response('')
    response.set_cookie('theme', theme, expires=31536000)  #wygaśnięcie ciasteczek po roku
    return response


if __name__ == '__main__':
    app.run(debug=True)  #uruchomienie aplikacji
