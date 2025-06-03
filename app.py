from flask import Flask, render_template, request, flash, redirect
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Для flash-сообщений

DATA_DIR = 'data'
ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_excel(file_path):
    required_columns = ['Номер студенческого билета', 'ФИО', 'Курс', 'Группа', 'Средний балл']
    try:
        df = pd.read_excel(file_path)
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return False, f"Отсутствуют обязательные столбцы: {', '.join(missing_columns)}"
        return True, None
    except Exception as e:
        return False, f"Ошибка при чтении файла: {str(e)}"

def load_student_data():
    student_data = []

    if not os.path.exists(DATA_DIR):
        return student_data

    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(DATA_DIR, filename)
            try:
                df = pd.read_excel(file_path)
                for _, row in df.iterrows():
                    student_data.append({
                        'file': filename.replace('.xlsx', ''),
                        'student_id': row['Номер студенческого билета'],
                        'fio': row['ФИО'],
                        'course': row['Курс'],
                        'group': row['Группа'],
                        'avg_grade': row['Средний балл']
                    })
            except Exception as e:
                print(f"Ошибка при чтении файла {filename}: {e}")

    return student_data

def sort_data(data, sort_by, order):
    if not data:
        return data

    key_map = {
        'fio': lambda x: x['fio'].lower(),
        'course': lambda x: x['course'],
        'group': lambda x: x['group'],
        'avg_grade': lambda x: x['avg_grade']
    }

    if sort_by not in key_map:
        sort_by = 'fio'

    reverse = (order == 'desc')
    return sorted(data, key=key_map[sort_by], reverse=reverse)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Файл не выбран', 'error')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('Файл не выбран', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(DATA_DIR, filename)

            os.makedirs(DATA_DIR, exist_ok=True)

            file.save(file_path)

            is_valid, error_message = validate_excel(file_path)
            if not is_valid:
                os.remove(file_path)
                flash(error_message, 'error')
                return redirect(request.url)

            flash('Файл успешно загружен', 'success')
            return redirect(request.url)
        else:
            flash('Недопустимый формат файла. Пожалуйста, загрузите файл .xlsx', 'error')
            return redirect(request.url)

    sort_by = request.args.get('sort_by', 'fio')
    order = request.args.get('order', 'asc')
    tab = request.args.get('tab', 'all')

    data = load_student_data()

    all_students = sort_data(data, sort_by, order)

    grouped_data = {}
    for entry in data:
        group = entry['group']
        if group not in grouped_data:
            grouped_data[group] = []
        grouped_data[group].append(entry)

    for group in grouped_data:
        grouped_data[group] = sort_data(grouped_data[group], sort_by, order)

    return render_template('index.html', grouped_data=grouped_data, all_students=all_students,
                           sort_by=sort_by, order=order, tab=tab)

if __name__ == '__main__':
    app.run(debug=True)