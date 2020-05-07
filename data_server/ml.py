import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Ridge
from scipy import stats
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

PRICE, AREA, ROOMS, REGION = 0, 1, 2, 3
X_NAMES = ['Price, 1000$', 'Area, m^2', 'Number of rooms', 'Region']
REGION_CODES = dict()


def load_np_array(db):
    ads = [np.array([ad['price'], ad['area'], ad['number_of_rooms'], -1], dtype=int)
           for ad in db.advertisements.find()]
    ads = np.array(ads)
    ads[:, PRICE] = ads[:, PRICE] / 1000

    region_names = [ad['region'] for ad in db.advertisements.find()]
    global REGION_CODES
    for index, region_name in enumerate(set(region_names)):
        REGION_CODES[region_name] = index
    codes = [REGION_CODES[region_name] for region_name in region_names]
    ads[:, REGION] = np.array(codes)

    return ads


def remove_odd_value(df):
    std_dev = 3
    return df[(np.abs(stats.zscore(df)) < float(std_dev)).all(axis=1)]


def create_model(x, y):
    degree = 3
    model = make_pipeline(PolynomialFeatures(degree), Ridge())
    model.fit(x, y)
    return model


def plot_image(x, y, model, x_axis_name):
    # change xticks and dpi
    if x_axis_name == 'Region':
        plt.figure(figsize=(20, 6), dpi=160)
        labels = list(REGION_CODES.keys())
        ticks = list(REGION_CODES.values())
        plt.xticks(ticks, labels, fontsize=5)
    else:
        plt.figure(figsize=(8, 6), dpi=80)
    # set label for axix
    plt.ylabel(X_NAMES[PRICE])
    plt.xlabel(x_axis_name)
    # plot training data
    plt.scatter(x, y, s=1, label='Training points')
    # plot predicted values
    x_plot = np.linspace(0, max(x)).reshape(-1, 1)
    plt.plot(x_plot, model.predict(x_plot), color='red', label='Predicted values')
    plt.legend(loc='upper left')

    plt.draw()
    plt.savefig(f'output/Price_to_{x_axis_name.split(",")[0].replace(" ", "_")}.png')
    plt.show()
    plt.close()
