from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime

START_YEAR = 1920

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    how_old = datetime.datetime.now().year - START_YEAR
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)