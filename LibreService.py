import os
import subprocess


def convert_docx_to_pdf(docx_path, output_pdf_path):
    """
    Функция для конвертации DOCX в PDF с использованием LibreOffice.

    :param docx_path: Путь к исходному файлу DOCX.
    :param output_pdf_path: Путь для сохранения PDF.
    """
    libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"  # Путь к LibreOffice

    # Выполняем команду LibreOffice
    cmd = [
        libreoffice_path, '--headless', '--convert-to', 'pdf',
        '--outdir', os.path.dirname(output_pdf_path), docx_path

    ]

    print(f"Запуск команды: {cmd}")

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(f"Конвертация завершена. PDF сохранен по пути: {output_pdf_path}")
    else:
        print(f"Ошибка конвертации: {result.stderr}")


# путь к файлу DOCX
docx_file_path = r"C:\Users\Petr\OneDrive\Рабочий стол\5 семестр\Геликон\Python\KPD\test2.docx"
# путь для сохранения PDF
output_pdf_path = r"C:\Users\Petr\OneDrive\Рабочий стол\5 семестр\Геликон\Python\KPD\temp\output.pdf"

# Запускаем конвертацию
convert_docx_to_pdf(docx_file_path, output_pdf_path)
