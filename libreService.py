# libreService.py
import os
import subprocess

def convert_docx_to_pdf(docx_path, output_pdf_path):
    """
    Функция для конвертации DOCX в PDF с использованием LibreOffice.

    :param docx_path: Путь к исходному файлу DOCX.
    :param output_pdf_path: Путь для сохранения PDF.
    """
    libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"  # Путь к LibreOffice

    # Выполняем команду LibreOffice для конвертации в PDF
    cmd = [
        libreoffice_path, '--headless', '--convert-to', 'pdf',
        '--outdir', os.path.dirname(output_pdf_path), docx_path
    ]

    print(f"Запуск команды: {cmd}")  # Отладочный вывод для проверки команды

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(f"Конвертация завершена")
    else:
        print(f"Ошибка конвертации: {result.stderr}")
