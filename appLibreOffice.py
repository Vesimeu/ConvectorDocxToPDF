# appLibreOffice.py
import os
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from libreService import convert_docx_to_pdf  # Импортируем функцию из libreService

app = Flask(__name__)

# Маршрут для конвертации DOCX в PDF
@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    # Проверка на правильный тип файла (DOCX)
    if file.content_type not in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        return jsonify({"error": "Invalid file type. Only Word files are supported."}), 400

    try:
        # Сохраняем временно файл на сервере
        input_file_path = os.path.join('temp', secure_filename(file.filename))
        os.makedirs(os.path.dirname(input_file_path), exist_ok=True)
        file.save(input_file_path)

        # Путь для сохранения PDF
        output_pdf_path = os.path.join('temp', f"{os.path.splitext(secure_filename(file.filename))[0]}.pdf")

        # Вызываем функцию конвертации из libreService
        convert_docx_to_pdf(input_file_path, output_pdf_path)

        # Отправляем PDF в ответ
        return send_file(output_pdf_path, mimetype='application/pdf', as_attachment=True,
                         download_name=f'{file.filename}.pdf')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
