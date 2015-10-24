#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse

import numpy
from matplotlib import pyplot

from lib import plot

from lib.polynomials import phi, f, f_str

def read_data(datadir):
    # Reading data
    x = numpy.loadtxt(os.path.join(datadir, "x.txt"))
    y = numpy.loadtxt(os.path.join(datadir, "y.txt"))

    # Shuffling data
    data = numpy.array([x,y])
    data = data.transpose()
    numpy.random.shuffle(data)
    x, y = data.transpose()

    y = numpy.matrix(y).T

    return x, y

def least_square(X, y):
    return numpy.linalg.solve(X*X.T, X*y)

def risk(X, y, theta):
    return numpy.linalg.norm(y - X.T * theta)**2 / X.shape[1]

def cross_validation(X, y, k):
    average_risk = 0

    for j in range(0, X.shape[1], k):
        if j == 0:
            X_test, X_train = numpy.hsplit(X, [j+k])
            y_test, y_train = numpy.vsplit(y, [j+k])
        elif j + k >= X.shape[1]:
            X_train, X_test = numpy.hsplit(X, [j])
            y_train, y_test = numpy.vsplit(y, [j])
        else:
            X_train1, X_test, X_train2 = numpy.hsplit(X, [j, j+k])
            X_train = numpy.hstack((X_train1, X_train2))

            y_train1, y_test, y_train2 = numpy.vsplit(y, [j, j+k])
            y_train = numpy.vstack((y_train1, y_train2))

        theta = least_square(X_train, y_train)
        average_risk += risk(X_test, y_test, theta)

    return average_risk * k / X.shape[1]

def best_degree(x, y, phi, dmax, folds):
    for d in range(0, dmax+1):
        if d == 0:
            X = numpy.matrix(phi(0, x))
        else:
            X = numpy.vstack((X, phi(d, x)))

        yield cross_validation(X, y, folds), d

def main(datadir, dmax, folds, plot_precision):
    colors = pyplot.rcParams["axes.color_cycle"]

    # Input
    print("-> Reading data in folder \"{}\"".format(datadir))
    x, y = read_data(datadir)

    # Risk
    print("-> Computing the average risk for polynomials of degrees between 0 and {},".format(dmax))
    print("   using cross validation with {} folds :".format(folds))

    risks = list(best_degree(x, y, phi, dmax, folds))
    best_risk, best_d = min(risks)

    risks, degrees = zip(*risks)

    fig = pyplot.figure()
    pyplot.yscale('log')
    pyplot.plot(degrees, risks, zorder=2)
    pyplot.plot([best_d], [best_risk], 'o', zorder=1)
    pyplot.xlabel('degree')
    pyplot.ylabel('average risk')
    pyplot.show()


    print("   -> The lowest risk ({:.2f}) is obtained with degree {}.".format(best_risk, best_d))

    print("-> Computing the best function of degree {} predicting the value of y.".format(best_d))

    X = numpy.matrix([phi(d,x) for d in range(0, best_d+1)])
    theta = least_square(X, y)

    print("   -> The best function is (approximately) : {}".format(f_str(theta)))

    pyplot.plot(x, y, 'o', color=colors[1], zorder=2)
    plot.plot_function(f(theta), plot_precision, color=colors[0], zorder=1)
    pyplot.show()

def setup_parser(parser):
    parser.add_argument("-d", "--dmax", type=int, metavar="D", default=40,
                        help="maximum degree (default: 40)")
    parser.add_argument("-k", "--folds", type=int, metavar="K", default=10,
                        help="number of folds used for the cross validation (default: 10)")
    parser.add_argument("-p", "--plot-precision", type=float, metavar="P", default=0.01,
                        help="step used to plot the function (default: 0.01)")

    rootdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    parser.add_argument("datadir", type=str, nargs="?", default=os.path.join(rootdir, "data", "tp0", "1"),
                        help='directory containing the data files x.txt and y.txt (default: "data/tp0/1")')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    setup_parser(parser)

    args = parser.parse_args({})

    main(**vars(args))
