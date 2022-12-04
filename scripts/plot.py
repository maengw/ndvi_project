import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas
import statistics


if __name__ == "__main__":

    # data = pandas.read_csv('/home/woo/PycharmProjects/immlproject/ndvidata2.csv', header=0)
    data = pandas.read_csv('/home/woo/PycharmProjects/immlproject/N_NDVI_RELATION.csv', header=0)
    cola = list(data.Nitrogens)
    cola = [round(num, 2) for num in cola]
    cola_len = len(cola)
    cola_sum = sum(cola)
    mean = cola_sum / cola_len
    std = statistics.pstdev(cola)
    # print('std=', std)
    # print('mean=', mean)
    binnums = int(round(np.sqrt(cola_len)))
    # print(binnums)
    plt.hist(cola, bins=binnums)
    plt.title('Nitrogen Percentage PLOT')
    plt.xlabel('Nitrogen %')
    plt.ylabel('Counts')
    mean = round(mean,3)
    std = round(std,3)
    plt.text(1.9, 30, 'mean :%s' %mean)
    plt.text(1.9, 28, 'std : %s' %std)
    plt.show()
