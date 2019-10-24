from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime

START_YEAR = 1920
ROSAS_FILE = 'vino.txt'

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    how_old=datetime.datetime.now().year - START_YEAR
)

# with open('index.html', 'w', encoding="utf8") as file:
#     file.write(rendered_page)

with open(ROSAS_FILE, "r") as my_file:
    file_contents = [wine.split(':') for wine in my_file.read().split(
        '\n') if wine != '']

    for attr, value in file_contents:
        if attr == 'Сорт':
            print(value)
