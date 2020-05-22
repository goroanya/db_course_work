import os

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge
from scipy import stats
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

PRICE, AREA, ROOMS, REGION = 0, 1, 2, 3
X_NAMES = ['Price, 1000$', 'Area, m^2', 'Number of rooms', 'Region']
REGION_CODES = dict()


def load_np_array(collection):
    ads = []
    from_db = list(collection.find())
    for index, ad in enumerate(from_db):
        os.system('clear')
        print(f'Loading database info: {100 * index // len(from_db)}%')
        new_ad = np.array([ad['price'], ad['area'], ad['number_of_rooms'], -1], dtype=int)
        ads.append(new_ad)
    ads = np.array(ads)
    ads[:, PRICE] = ads[:, PRICE] / 1000

    region_names = [ad['region'] for ad in collection.find()]
    names_set = set(region_names)
    global REGION_CODES
    for index, region_name in enumerate(names_set):
        REGION_CODES[region_name] = len(names_set) + index
    codes = [REGION_CODES[region_name] for region_name in region_names]
    ads[:, REGION] = np.array(codes)

    ads = remove_odd_value(ads, AREA)
    ads = remove_odd_value(ads, PRICE)
    ads = remove_odd_value(ads, ROOMS)
    return sort_by_avg_region_price(ads)


def sort_by_avg_region_price(ads):
    region_codes = ads[:, REGION]
    avg_prices = dict()
    for code in set(region_codes):
        avg_price = np.average(ads[np.equal(ads[:, REGION], code)])
        avg_prices[code] = avg_price

    sorted_codes = []
    for code in sorted(ads[:, REGION], key=lambda r: avg_prices[r]):
        if code not in sorted_codes:
            sorted_codes.append(code)

    for index, code in enumerate(sorted_codes):
        name = find_region_name_by_code(code)
        REGION_CODES[name] = index
        for ad in ads:
            if ad[REGION] == code:
                ad[REGION] = index

    return ads


def find_region_name_by_code(given_code):
    for name, code in REGION_CODES.items():
        if code == given_code:
            return name


def remove_odd_value(df, prop_name):
    std_dev = 3
    z_scores = stats.zscore(df[:, prop_name])
    return df[np.abs(z_scores) < std_dev]


def create_linear_model(x, y):
    model = LinearRegression()
    model.fit(x, y)
    return model


def create_polynomial_model(x, y):
    degree = 3
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(x, y)
    return model


def plot_image(x, y, model, x_axis_name, regression_type):
    # change xticks and dpi
    if x_axis_name == 'Region':
        plt.figure(figsize=(15, 8), dpi=100)
        labels = [l if len(l) < 10 else f'{l[:8]}..'
                  for l in list(REGION_CODES.keys())]
        ticks = list(REGION_CODES.values())
        plt.xticks(ticks, labels, fontsize=9, rotation=90)
    else:
        plt.figure(figsize=(8, 6), dpi=140)
    # set label for axix
    plt.ylabel(X_NAMES[PRICE])
    plt.xlabel(x_axis_name)
    # plot training data
    plt.scatter(x, y, s=1, label='Training points')
    # plot predicted values
    x_plot = np.linspace(0, max(x)).reshape(-1, 1)
    plt.plot(x_plot, model.predict(x_plot), color='red', label='Predicted values')
    plt.legend(loc='upper left')

    window_title = f'{regression_type} Price to {x_axis_name.split(",")[0]}'
    plt.draw()
    file_name = f'output/{window_title.replace(" ", "_")}.png'
    plt.savefig(file_name)
    plt.gcf().canvas.set_window_title(window_title)
    plt.show()
    plt.close()
