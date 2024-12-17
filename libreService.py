# libreService.py
import os
import subprocess
from io import BytesIO

def convert_docx_to_pdf(docx_bytes, output_pdf_path):
    """
    Функция для конвертации DOCX в PDF с использованием LibreOffice.

    :param docx_bytes: Поток байтов документа DOCX.
    :param output_pdf_path: Путь для сохранения PDF.
    """
    libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"  # Путь к LibreOffice

    # Временный файл для DOCX
    temp_docx_path = 'temp_input.docx'

    # Получаем директорию для сохранения PDF
    output_dir = os.path.dirname(output_pdf_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Сохраняем байтовый поток в файл
    with open(temp_docx_path, 'wb') as f:
        f.write(docx_bytes)

    # Выполняем команду LibreOffice для конвертации в PDF
    cmd = [
        libreoffice_path, '--headless', '--convert-to', 'pdf',
        '--outdir', output_dir, temp_docx_path
    ]

    print(f"Запуск команды: {cmd}")  # Отладочный вывод для проверки команды

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    pdf_output_path = None
    if result.returncode == 0:
        # Воссоздаем PDF путь, используя имя исходного DOCX файла
        pdf_output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(temp_docx_path))[0]}.pdf")
        print(f"Конвертация завершена. PDF сохранен по пути: {pdf_output_path}")
    else:
        print(f"Ошибка конвертации: {result.stderr}")

    # Удаляем временный DOCX файл
    os.remove(temp_docx_path)

    # Возвращаем путь к PDF или None, если ошибка
    return pdf_output_path
