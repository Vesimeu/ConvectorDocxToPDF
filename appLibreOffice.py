import os
import subprocess
from flask import Flask, request, send_file, jsonify
from flask_socketio import SocketIO, emit
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)

# Словарь для отслеживания состояния конвертации и связывания с клиентами
conversion_status = {}
sid_mapping = {}  # Связь между файлами и sid

# Функция для конвертации DOCX в PDF с использованием LibreOffice
def convert_docx_to_pdf(docx_path, output_path, output_pdf_path, sid):
    libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"

    # Выполнение команды LibreOffice для конвертации в PDF
    cmd = [
        libreoffice_path, '--headless', '--convert-to', 'pdf:writer_pdf_Export',
        '--outdir', output_path, docx_path
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        conversion_status[os.path.basename(docx_path)] = "Conversion completed"
        # Перемещаем PDF в нужное место
        new_pdf_path = os.path.join(output_path, f"{os.path.splitext(os.path.basename(docx_path))[0]}.pdf")
        os.rename(new_pdf_path, output_pdf_path)
        emit('conversion_complete', {'message': 'Conversion complete!', 'file': output_pdf_path}, room=sid)
    else:
        conversion_status[os.path.basename(docx_path)] = f"Error: {result.stderr}"
        emit('conversion_error', {'message': f"Error during conversion: {result.stderr}"}, room=sid)

# Маршрут для загрузки документа
@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.content_type not in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        return jsonify({"error": "Invalid file type. Only Word files are supported."}), 400

    try:
        # Сохраняем временно файл на сервере
        input_file_path = os.path.join('temp', file.filename)
        os.makedirs(os.path.dirname(input_file_path), exist_ok=True)
        file.save(input_file_path)

        # Путь для сохранения PDF
        output_dir = 'temp/pdfs'
        os.makedirs(output_dir, exist_ok=True)
        output_pdf_path = os.path.join(output_dir, f'{os.path.splitext(file.filename)[0]}.pdf')

        # Сохраняем sid клиента
        sid = request.cookies.get('sid')  # Передача sid через cookie
        sid_mapping[file.filename] = sid  # Сохраняем связь между файлом и sid
        conversion_status[os.path.basename(input_file_path)] = "Conversion in progress..."

        # Запуск конвертации в отдельном потоке
        conversion_thread = Thread(target=convert_docx_to_pdf, args=(input_file_path, output_dir, output_pdf_path, sid))
        conversion_thread.start()

        return jsonify({"message": "Conversion started, you will be notified once it's done."}), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Маршрут для проверки статуса конвертации
@app.route('/status/<filename>', methods=['GET'])
def check_status(filename):
    status = conversion_status.get(filename, 'Conversion in progress...')
    return jsonify({"status": status})

# Маршрут для загрузки готового PDF
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    pdf_path = os.path.join('temp/pdfs', filename)
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

# Маршрут для подключения клиентов через веб-сокеты
@socketio.on('connect')
def handle_connect():
    sid = request.sid  # Получаем уникальный идентификатор клиента для сокетов
    print(f"Client connected: {sid}")

    # Отправка sid клиенту (можно сохранить его в cookies или использовать для дальнейшего отслеживания)
    emit('sid', {'sid': sid})

# Запуск сервера
if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
