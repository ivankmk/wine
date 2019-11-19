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
        assets_in_categ = []
        for asset_element in [
            asset.strip().split('\n') for asset
                in row.split('\n\n')[1:] if len(asset) > 1]:
            asset_element = [
                element.split(':')[-1].strip() for element in asset_element]
            if 'Выгодное предложение' in asset_element:
                name, gr_type, price, img, spec_offer = asset_element
                assets_in_categ.append(
                    {'name': name,
                     'gr_type': gr_type,
                     'price': price,
                     'img': img,
                     'spec_offer': True})
            else:
                name, gr_type, price, img = asset_element
                assets_in_categ.append(
                    {'name': name,
                     'gr_type': gr_type,
                     'price': price,
                     'img': img,
                     'spec_offer': None})
            output_data.update({category: assets_in_categ})
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
