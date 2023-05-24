from flask import render_template, redirect, url_for
from . import app
from .models import News, Category, db
from .forms import NewsForm, CategoryForm


@app.route('/')
def index():
    news = News.query.all()
    categories = Category.query.all()
    return render_template("index.html", news=news, categories=categories)


@app.route('/news_detail/<int:id>')
def news_detail(id):
    news = News.query.get(id)
    categories = Category.query.all()
    return render_template("news_detail.html", news=news, categories=categories)


@app.route('/main_page/<name>')
def main_page(name):
    return f"Добро пожаловать {name}"


@app.route('/add_news', methods=["GET", "POST"])
def add_news():
    form = NewsForm()
    categories = Category.query.all()
    if form.validate_on_submit():
        news = News()
        news.title = form.title.data
        news.text = form.text.data
        news.category_id = form.category.data
        db.session.add(news)
        db.session.commit()

        return redirect(url_for("news_detail", id=news.id))
    return render_template("add_news.html", form=form, categories=categories)


@app.route('/add_category', methods=["GET", "POST"])
def add_category():
    form = CategoryForm()
    categories = Category.query.all()
    if form.validate_on_submit():
        category = Category()
        category.title = form.title.data
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_category.html", form=form, categories=categories)


@app.route('/category/<int:id>')
def news_in_category(id):
    category = Category.query.get(id)
    news = category.news
    category_name = category.title
    categories = Category.query.all()
    return render_template('categories.html', news=news, category_name=category_name, categories=categories)
