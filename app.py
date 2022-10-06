from datetime import datetime
import secrets

from flask import Flask, request, render_template
from flask_cors import CORS

from models import FoodModel, UserModel, db, login
from sorting import selection_sort


app = Flask(__name__)
secret_key = secrets.token_urlsafe(32)
app.secret_key = secret_key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foodcamp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)

CORS(app)


@app.route('/')
def index():
    all_dishes = FoodModel.query.all()
    all_dishes_list = []

    for dish in all_dishes:
        all_dishes_list.append({'id': dish.id, 'name': dish.short_description, 'ratings': dish.ratings, 'date': datetime.strftime(dish.date, "%d.%m.%Y")})

    sorted_dishes = selection_sort(all_dishes_list, 'ratings')

    length = len(sorted_dishes) - 20
    if length < 0:
        length = 0

    most_viewed = []
    for i in range(len(sorted_dishes) - 1, length - 1, -1):
        most_viewed.append(sorted_dishes[i])

    return render_template('index.html', dishes=most_viewed), 200


@app.route('/food', methods=['GET', 'POST'])
def food():
    if request.method == 'GET':
        all_dishes = FoodModel.query.all()
        all_dishes_list = []

        for dish in all_dishes:
            all_dishes_list.append({'id': dish.id, 'name': dish.short_description, 'date': datetime.strftime(dish.date, "%d.%m.%Y")})
        
        return render_template('food.html', dishes=all_dishes_list), 200
    
    if request.method == 'POST':
        return 'POST'


@app.route('/food/<int:food_id>')
def food_by_id(food_id):
    dish = FoodModel.query.filter(FoodModel.id == food_id).first()
    dish_info = {'name': dish.short_description, 'date': datetime.strftime(dish.date, "%d.%m.%Y"), 
                'description': dish.description, 'rate': dish.ratings, 'author': dish.author}
    return render_template('food_by_id.html', dish_info=dish_info), 200


@app.route('/countries')
def countries():
    '''
    ans_ = FoodModel.query.all()
    ans = []
    for a in ans_:
        ans.append({'id': a.id, 'sh_d': a.short_description, 'date': a.date.strftime('%Y-%m-%d')})
    return jsonify(ans)
    '''
    return render_template('countries.html'), 200


@app.route('/favs')
def favourites():
    return render_template('favourites.html'), 200


@app.route('/category')
def category():
    return render_template('category.html'), 200


@app.route('/about')
def about():
    return render_template('about.html'), 200


@app.route('/faq')
def faq():
    return render_template('faq.html'), 200


@app.route('/login')
def login():
    return render_template('login.html'), 200


@app.route('/signup')
def signup():
    return render_template('signup.html'), 200


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
