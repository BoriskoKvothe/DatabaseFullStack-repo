# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import db, Bone
import os

app = Flask(__name__)

# Absolute directory path
basedir = os.path.abspath(os.path.dirname(__file__))

# Update the database URI to use the absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cranium_bones.db')

db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    sort = request.args.get('sort', 'boneID')  # Default sort by boneID
    order = request.args.get('order', 'asc')  # Default order
    search_term = request.form.get('search_term', '')

    try:
        if request.method == 'POST' and search_term:
            bones = Bone.query.filter(Bone.name.contains(search_term) | Bone.category.contains(search_term))
        else:
            bones = Bone.query
        
        if order == 'asc':
            bones = bones.order_by(getattr(Bone, sort).asc())
        else:
            bones = bones.order_by(getattr(Bone, sort).desc())

        return render_template('list_bones.html', bones=bones.all())
    except Exception as e:
        print("Error:", e)
        return str(e)

    
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form.get('search_term', '')
        filter_option = request.form.get('filter_option', 'name')

        if filter_option == 'name':
            bones = Bone.query.filter(Bone.name.contains(search_term)).all()
        elif filter_option == 'category':
            bones = Bone.query.filter(Bone.category.contains(search_term)).all()
        else:
            bones = Bone.query.all()

        return render_template('list_bones.html', bones=bones)

    return render_template('search_bones.html')


#back-end print
@app.route('/print_section', methods=['GET', 'POST'])
def print_section():
    if request.method == 'POST':
        criteria = request.form['criteria']
        value = request.form.get('value', '')  # Optional value field

        if criteria == 'category':
            bones = Bone.query.filter(Bone.category == value).all()
        elif criteria == 'name':
            bones = Bone.query.filter(Bone.name.contains(value)).all()
        else:
            bones = Bone.query.all()

        # For backend printing
        for bone in bones:
            print(f"{bone.name} - {bone.category}")

        # For frontend display
        return render_template('print_results.html', bones=bones, criteria=criteria, value=value)

    return render_template('print_section.html')



@app.route('/add_bone', methods=['GET', 'POST'])
def add_bone():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        new_bone = Bone(name=name, category=category)
        db.session.add(new_bone)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_bones.html')


@app.route('/add_multiple', methods=['GET', 'POST'])
def add_multiple():
    if request.method == 'POST':
        bones_data = request.form['bones_data']
        # bones_data should be in a specific format, e.g., "name1,category1;name2,category2"
        for bone_info in bones_data.split(';'):
            name, category = bone_info.split(',')
            new_bone = Bone(name=name.strip(), category=category.strip())
            db.session.add(new_bone)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_multiple.html')


@app.route('/update/<int:bone_id>', methods=['GET', 'POST'])
def update_bone(bone_id):
    bone = Bone.query.get_or_404(bone_id)
    if request.method == 'POST':
        bone.name = request.form['name']
        bone.category = request.form['category']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_bones.html', bone=bone)

@app.route('/update_multiple', methods=['POST'])
def update_multiple():
    selected_bones = request.form.getlist('selected_bones')
    new_category = request.form.get('new_category')

    if selected_bones and new_category:
        for bone_id in selected_bones:
            bone_to_update = Bone.query.get(bone_id)
            if bone_to_update:
                bone_to_update.category = new_category
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/update_by_category', methods=['POST'])
def update_by_category():
    allowed_categories = ['neurocranium', 'splanchnocranium']
    old_category = request.form.get('old_category')
    new_category = request.form.get('new_category')

    if old_category and new_category and new_category in allowed_categories:
        Bone.query.filter_by(category=old_category).update({'category': new_category})
        db.session.commit()
    else:
        # Handle the error case, e.g., by flashing a message to the user
        pass

    return redirect(url_for('index'))





@app.route('/delete/<int:bone_id>')
def delete_bone(bone_id):
    bone = Bone.query.get_or_404(bone_id)
    db.session.delete(bone)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_multiple', methods=['POST'])
def delete_multiple():
    selected_bones = request.form.getlist('selected_bones')

    if selected_bones:
        for bone_id in selected_bones:
            bone_to_delete = Bone.query.get(bone_id)
            if bone_to_delete:
                db.session.delete(bone_to_delete)
        db.session.commit()

    return redirect(url_for('index'))


    
@app.route('/delete_by_category', methods=['POST'])
def delete_by_category():
    category = request.form['category']
    Bone.query.filter_by(category=category).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_by_criteria', methods=['POST'])
def delete_by_criteria():
    criteria = request.form['criteria']
    value = request.form.get('value', '')

    if criteria == 'category':
        Bone.query.filter(Bone.category == value).delete()
    elif criteria == 'name':
        Bone.query.filter(Bone.name.contains(value)).delete()

    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
