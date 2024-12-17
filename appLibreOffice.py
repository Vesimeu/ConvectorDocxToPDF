# appLibreOffice.py
import os
from flask import Flask, request, send_file, jsonify
from libreService import convert_docx_to_pdf

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    # Проверка на правильный тип файла (DOCX)
    if file.content_type not in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        return jsonify({"error": "Invalid file type. Only Word files are supported."}), 400

    try:
        # Получаем поток байтов
        docx_bytes = file.read()

        # Путь для сохранения PDF
        output_pdf_path = os.path.join('temp', f"{os.path.splitext(file.filename)[0]}.pdf")

        # Вызываем функцию конвертации из libreService
        pdf_file_path = convert_docx_to_pdf(docx_bytes, output_pdf_path)

        # Если PDF файл успешно создан, отправляем его клиенту
        if pdf_file_path:
            return send_file(pdf_file_path, mimetype='application/pdf', as_attachment=True,
                             download_name=f'{file.filename}.pdf')
        else:
            return jsonify({"error": "Error during PDF conversion"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
