import pypandoc
from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)

def convert_docx_to_pdf(docx_path, output_pdf_path):
    # Указание движка LaTeX и шрифта с использованием шаблона LaTeX
    output = pypandoc.convert_file(
        docx_path,
        'pdf',
        outputfile=output_pdf_path,
        extra_args=[
            '--pdf-engine=xelatex',
            '--variable', 'mainfont="Times New Roman"',
            '--template=template.tex',
            '--variable', 'linkcolor=blue',  # Цвет гиперссылок
            '--variable', 'urlcolor=blue'  # Цвет для URL
        ]
    )

    assert output == ""  # Убедитесь, что конвертация прошла без ошибок
    print(f"PDF сохранен по пути {output_pdf_path}")

@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.content_type not in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        return jsonify({"error": "Invalid file type. Only Word files are supported."}), 400

    try:
        # Сохраняем файл временно
        input_file_path = os.path.join('temp', file.filename)
        os.makedirs(os.path.dirname(input_file_path), exist_ok=True)
        file.save(input_file_path)

        # Путь для сохранения PDF
        output_pdf_path = os.path.join('temp', f'{os.path.splitext(file.filename)[0]}.pdf')

        # Конвертируем DOCX в PDF
        convert_docx_to_pdf(input_file_path, output_pdf_path)

        # Отправляем PDF в ответ
        return send_file(output_pdf_path, mimetype='application/pdf', as_attachment=True, download_name=f'{file.filename}.pdf')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
