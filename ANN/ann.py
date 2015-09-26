import numpy as np
import random
import math

def _get_np_array(nr, nc, l, h):
    return np.array([np.array([random.uniform(l, h)    for c in range(nc)])    for r in range(nr)])

def _sigmoid(x):
    return 1 / (1 + math.exp(-x))

def _deriv_sigmoid(x):
    return x * (1 - x)

class ANN:
    def __init__(self, ni, nh, no, iteration=3000, lr=1.0):
        self.ni = ni #+ 1 # for bias
        self.no = no
        self.nh = nh #+ 1 # for bias
        self.lr = lr
        self.iteration = iteration

        self.wi = _get_np_array(self.nh, self.ni, -0.5, 0.5)
        self.wo = _get_np_array(self.no, self.nh, -2, 2)


    def _train(self, x):
        self.x = x
        self._out_hidden = np.array([_sigmoid(np.dot(w, np.array(x)))    for w in self.wi])
        self._output = np.array([_sigmoid(np.dot(out, self._out_hidden))    for out in self.wo])

    def _back_propagate(self, y):
        self.delta_o = np.array([_deriv_sigmoid(i)    for i in self._output]) * (np.array(y) - self._output)
        self.wo = self.wo + (self.lr * np.array([self._out_hidden * d    for d in self.delta_o]))

        self.delta_h = np.array([_deriv_sigmoid(i)    for i in self._out_hidden]) * np.dot(self.wo.transpose(), self.delta_o)
        self.wi = self.wi + (self.lr * self.delta_h.reshape(self.nh, 1) * np.array(self.x))

    def fit(self, X, Y):
        for i in range(self.iteration):
            for x, y in zip(X, Y):
                self._train(x)
                self._back_propagate(y)
            if i % 100 == 0:
                print "delta_o: ", self.delta_o
                print ""

    def predict(self, X):
        self._train(X)
        return self._output

if __name__ == "__main__":
    ann = ANN(3, 8, 1)
    data = [[0, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 1],
            [1, 1, 0],
            [1, 1, 1]]
    target = [[0], [1], [1], [1], [1], [1], [1], [1]]
    ann.fit(data, target)

    for d, t in zip(data, target):
        print d, " ==> ", t, " --> ", ann.predict(d)
