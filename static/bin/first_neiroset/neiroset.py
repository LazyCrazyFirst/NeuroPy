import numpy as np


def start():
    slov = {}

    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    training_inputs = np.array([[0, 0, 1],
                                [1, 1, 1],
                                [1, 0, 1],
                                [0, 1, 1]])

    training_outpus = np.array([[0, 1, 1, 0]]).T

    synaptic_weights = 2 * np.random.random((3, 1)) - 1

    k = 2 * np.random.random((3, 1)) - 1
    slov['Случайные инициализирующие веса:'] = k

    # Метод обратного распространения
    for i in range(20000):
        input_layer = training_inputs
        outputs = sigmoid(np.dot(input_layer, synaptic_weights))

        err = training_outpus - outputs
        adjustments = np.dot(input_layer.T, err * (outputs) * (1 - outputs))

        synaptic_weights += adjustments

    slov['Веса после обучения:'] = synaptic_weights
    slov['Результат после обучения:'] = outputs

    return slov
