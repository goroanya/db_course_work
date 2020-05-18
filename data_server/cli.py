import numpy as np
from consolemenu import SelectionMenu

from ml import load_np_array, create_linear_model, create_polynomial_model, \
    plot_image, X_NAMES, PRICE, REGION, REGION_CODES
from storage import get_collection

collection = get_collection()
ads = load_np_array(collection)


def show_start_menu():
    opts = ['Regression for Price with Area',
            'Regression for Price with Number of rooms',
            'Regression for Price with Region',
            'Regression for Price with all variables']
    menu = SelectionMenu(opts, title="Select a task to do:")
    menu.show()

    if menu.is_selected_item_exit():
        return

    index = menu.selected_option + 1
    menu = SelectionMenu(['Linear regression', 'Polynomial regression'],
                         title='Select regression type',
                         show_exit_option=False)
    menu.show()

    regression_type = 'linear' if menu.selected_option == 0 else 'polynomial'
    if index > REGION:
        show_total_regression(regression_type)
    else:
        show_single_regression(index, regression_type)


def show_single_regression(x_index, regression_type):
    x = ads[:, x_index].reshape(-1, 1)
    y = ads[:, PRICE].reshape(-1, 1)
    model = create_linear_model(x, y)\
        if regression_type == 'linear'\
        else create_polynomial_model(x, y)
    plot_image(x, y, model, X_NAMES[x_index], regression_type)
    show_start_menu()


def show_total_regression(regression_type):
    x = ads[:, 1:]
    y = ads[:, PRICE].reshape(-1, 1)

    model = create_linear_model(x, y)\
        if regression_type == 'linear'\
        else create_polynomial_model(x, y)

    print(REGION_CODES)
    input_values = [[input(f'{x_label} = ') for x_label in X_NAMES[1:]]]

    predicted_price = model.predict(np.array(input_values, dtype=int))[0][0] * 1000
    print(f'Predicted house price is: {int(predicted_price):,}$')

    input('\nPress ENTER...')
    show_start_menu()


if __name__ == '__main__':
    show_start_menu()
