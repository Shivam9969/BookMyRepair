from flask import render_template, session, request, redirect, url_for, flash, current_app
from bookmyrepair import app, db, photos
from bookmyrepair.products.models import Category, Addservice
from .forms import Addservices
import secrets
import os


@app.route('/addcat', methods=['GET', 'POST'])
def addcat():
    if request.method == "POST":
        getcat = request.form.get('category')
        category = Category(name=getcat)
        db.session.add(category)
        db.session.commit()
        flash(f'The brand {getcat} was added to your database', 'success')
        return redirect(url_for('addcat'))
    return render_template('products/addcat.html')


@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == "POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('products/updatecat.html', updatecat=updatecat)


@app.route('/deletecat/<int:id>', methods=['GET', 'POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        flash(f"The category {category.name} was deleted from your database", "success")
        db.session.commit()
        return redirect(url_for('adminhome'))
    flash(f"The brand {category.name} can't be  deleted from your database", "warning")
    return redirect(url_for('adminhome'))


@app.route('/addservices', methods=['GET', 'POST'])
def addservices():
    form = Addservices(request.form)
    categories = Category.query.all()
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        desc = form.discription.data
        category = request.form.get('category')
        image_1 = photos.save(request.files['image_1'], name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files['image_2'], name=secrets.token_hex(10) + ".")
        addserv = Addservice(name=name, price=price, desc=desc,
                             category_id=category, image_1=image_1, image_2=image_2)
        db.session.add(addserv)
        flash(f'The service {name} was added in database', 'success')
        db.session.commit()
        return redirect(url_for('adminhome'))

    return render_template('products/addservices.html', form=form, categories=categories)


@app.route('/updateservice/<int:id>', methods=['GET', 'POST'])
def updateservice(id):
    form = Addservices(request.form)
    service = Addservice.query.get_or_404(id)
    categories = Category.query.all()
    category = request.form.get('category')
    if request.method == "POST":
        service.name = form.name.data
        service.price = form.price.data
        service.desc = form.discription.data
        service.category_id = category
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/Images/" + service.image_1))
                service.image_1 = photos.save(request.files['image_1'], name=secrets.token_hex(10) + ".")
            except:
                service.image_1 = photos.save(request.files['image_1'], name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/Images/" + service.image_2))
                service.image_2 = photos.save(request.files['image_2'], name=secrets.token_hex(10) + ".")
            except:
                service.image_2 = photos.save(request.files['image_2'], name=secrets.token_hex(10) + ".")

        flash('The service was updated', 'success')
        db.session.commit()
        return redirect(url_for('adminhome'))

    form.name.data = service.name
    form.price.data = service.price
    form.discription.data = service.desc
    category = service.category.name
    return render_template('products/updateservice.html', form=form, categories=categories, service=service)


@app.route('/deleteservice/<int:id>', methods=['POST'])
def deleteservice(id):
    service = Addservice.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + service.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + service.image_2))
        except Exception as e:
            print(e)
        db.session.delete(service)
        db.session.commit()
        flash(f'The Service {service.name} was delete from your record', 'success')
        return redirect(url_for('adminhome'))
    flash(f'Can not delete the Service', 'success')
    return redirect(url_for('adminhome'))


@app.route("/Book")
def book():
    services = Addservice.query.filter(Addservice.id)
    return render_template('products/index.html', services=services)


def categories():
    categories = Category.query.join(Addservice, (Category.id == Addservice.category_id)).all()
    return categories


@app.route('/service/<int:id>')
def single_page(id):
    service = Addservice.query.get_or_404(id)
    return render_template('products/single_page.html', service=service, categories=categories())
