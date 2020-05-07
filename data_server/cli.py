import os

from consolemenu import SelectionMenu

import settings
from storage import db_instance
from ml import load_np_array, remove_odd_value, create_model, \
    plot_image, X_NAMES, PRICE, REGION, REGION_CODES

db = db_instance(os.getenv('DB_URL'))
ads = remove_odd_value(load_np_array(db))


def show_start_menu():
    x_names = [name.split(',')[0] for name in X_NAMES[1:]]
    single_regression_opts = [f'Polynomial regression for Price with {name}'
                              for name in x_names]
    menu = SelectionMenu(single_regression_opts +
                         ['Polynomial regression for Price with all variables'],
                         title="Select a task to do:")
    menu.show()

    if menu.is_selected_item_exit():
        return

    index = menu.selected_option + 1
    if index > REGION:
        show_total_regression()
    else:
        show_single_regression(index)


def show_single_regression(x_index):
    x = ads[:, x_index].reshape(-1, 1)
    y = ads[:, PRICE].reshape(-1, 1)
    model = create_model(x, y)

    plot_image(x, y, model, X_NAMES[x_index])
    show_start_menu()


def show_total_regression():
    x = ads[:, 1:]
    y = ads[:, PRICE].reshape(-1, 1)

    model = create_model(x, y)
    print(REGION_CODES)
    input_values = [[input(f'{x_label} = ') for x_label in X_NAMES[1:]]]

    predicted_price = model.predict(input_values)[0][0] * 1000
    print(f'Prodicted house price is: {int(predicted_price):,}$')


if __name__ == '__main__':
    show_start_menu()
