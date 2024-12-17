import pypandoc
import os


def convert_word_to_pdf(word_path, output_pdf_path):
    """
    Функция для конвертации Word (DOCX) в PDF с использованием Pandoc.

    :param word_path: Путь к файлу Word (DOCX).
    :param output_pdf_path: Путь для сохранения PDF.
    """
    try:
        output = pypandoc.convert_file(
            word_path,
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
        assert output == ""  # Проверяем, что конвертация завершилась без ошибок
        print(f"Конвертация завершена. PDF сохранен по пути: {output_pdf_path}")
    except Exception as e:
        print(f"Ошибка конвертации: {e}")


# Укажите путь к вашему файлу Word
word_path = "input.docx"
# Укажите путь для сохранения PDF
output_pdf_path = r"C:\Users\Petr\OneDrive\Рабочий стол\5 семестр\Геликон\Python\KPD\output.pdf"

# Запустите функцию
convert_word_to_pdf(word_path, output_pdf_path)
