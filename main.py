from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime


START_YEAR = 1920
ACTIONS = 'inventory_list.txt'


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
            asset_element_cleaned = {
                element.split(':')[0].strip():
                    element.split(':')[-1].strip() for element in asset_element
                }
            print(asset_element_cleaned)
            if 'Выгодное предложение' in asset_element_cleaned:
                assets_in_category.append(
                    {'name': asset_element_cleaned['Название'],
                     'grape_type': asset_element_cleaned['Сорт'],
                     'price': asset_element_cleaned['Цена'],
                     'img': asset_element_cleaned['Картинка'],
                     'special_offer': True})
            else:
                name, grape_type, price, img = asset_element_cleaned
                assets_in_category.append(
                    {'name': asset_element_cleaned['Название'],
                     'grape_type': asset_element_cleaned['Сорт'],
                     'price': asset_element_cleaned['Цена'],
                     'img': asset_element_cleaned['Картинка'],
                     'special_offer': None})
            output_data[category] = assets_in_category

    return output_data


if __name__ == "__main__":

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    data_text = read_file(ACTIONS)
    converted_data = convert_to_dict(data_text)

    rendered_page = template.render(
        how_old=datetime.datetime.now().year - START_YEAR,
        converted_data=converted_data
        )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
