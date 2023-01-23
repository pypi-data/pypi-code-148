import math
import numpy as np
import matplotlib.pyplot as plt
def log_utility(good_utility, price, consumer_income):
    return math.log(good_utility - price / consumer_income)
def U(goods_a, goods_b,β=1/3):
    return goods_a**β * goods_b**(1-β)
def utility(comsumption, γ):
    return comsumption**(1-γ)/(1-γ)
def main():
    print("hello")
    fig, ax = plt.subplots()
    A = np.linspace(1, 100, 100)
    ax.plot(A, utility(A,0.7))
    ax.set_xlabel("A")
    ax.set_ylabel("utility")
    plt.show()
if __name__ == '__main__':
    main()