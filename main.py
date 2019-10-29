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


def file_reader(filename):
    with open(filename, "r", encoding='utf-8-sig') as my_file:
        return my_file.read()


def dict_converter(data_text):
    output_data = {}
    for row in data_text.split('# '):
        category = row.split('\n')[0]
        assets_in_categ = []
        for element in [
            details.strip().split('\n') for details in row.split(
                '\n\n')[1:] if len(details) > 1]:
            name, gr_type, price, img = [
                a.split(': ')[1] for a in element if len(a) > 1]
            assets_in_categ.append(
                {'name': name,
                 'gr_type': gr_type,
                 'price': price,
                 'img': img})

        output_data.update({category: assets_in_categ})
    return output_data


data_text = file_reader('products.txt')
converted_data = dict_converter(data_text)

print(converted_data)

        




