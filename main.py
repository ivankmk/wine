# -*- coding: utf-8 -*-
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import sys


START_YEAR = 1920


def read_file(filename):
    with open(filename, "r", encoding='utf-8-sig') as my_file:
        return my_file.read()


def convert_to_dict(data_text):
    output_data = {}
    for row in data_text.split('# '):
        category = row.split('\n')[0]
        assets_in_category = []
        assets = [asset.strip().split('\n') for asset in row.split(
            '\n\n')[1:] if len(asset) > 1]
        for asset_element in assets:
            element_cleaned = {
                element.split(':')[0].strip():
                    element.split(':')[-1].strip() for element in asset_element
                }

            assets_in_category.append(
                {'name': element_cleaned['Название'],
                 'grape_type': element_cleaned['Сорт'],
                 'price': element_cleaned['Цена'],
                 'img': element_cleaned['Картинка'],
                 'special_offer': 'Выгодное предложение' in element_cleaned})

            output_data[category] = assets_in_category

    return output_data


if __name__ == "__main__":

    input_file = sys.argv[1]

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    raw_inventory = read_file(input_file)
    prepared_inventory = convert_to_dict(raw_inventory)

    rendered_page = template.render(
        how_old=datetime.datetime.now().year - START_YEAR,
        prepared_inventory=prepared_inventory
        )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
