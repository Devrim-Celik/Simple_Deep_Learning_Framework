import numpy as np
import matplotlib.pyplot as plt
import pickle
from losses import LossMSE

def calculate_performance(X, Y, network, plot=False):
    """
    Given samples X and labels Y, uses the network to make a prediction
    and calculate the number of correct predictions and the MSE.

    Args:
        X (nd.array):               Samples of Form [samples x features]
        Y (nd.array):               Labels of Form [samples x 1]
        network (NeuralNetwork):    Neural Network
        plot (boolean):             Whether to Plot
    Returns:
        mse_error
        accuracy (float):           Percentage of correct Classifications
        prediction (nd.array):      Actual (rounded) Predictions
    """
    # predictions of the neural network
    prediction = network.forward(X.T)[0]

    # initializing loss function
    loss_function = LossMSE()

    # calculating loss
    mse_error = loss_function(Y, prediction)

    # rounding them to 1 or 0
    prediction[prediction>=0.5] = 1
    prediction[prediction<0.5] = 0
    prediction = prediction.astype(int)
    # calculating the accuracy
    accuracy = np.mean(prediction == Y)

    if plot:
        plot_data(X, prediction)

    return mse_error, accuracy, prediction


def plot_data(X, Y):
    colors = {}
    plt.figure("Data Plot")
    plt.scatter(X[:,0], X[:,1], color=np.array(["red" if x == 0 else "blue" for x in Y]))
    plt.show()


def plot_performance(training_mse, training_accuracies, testing_mse, testing_accuracies):
    plt.figure("MSE Summary")
    plt.plot([x[0] for x in training_mse], [x[1] for x in training_mse], label="Training MSE")
    plt.plot([x[0] for x in testing_mse], [x[1] for x in testing_mse], label="Testing MSE")
    plt.legend()


    plt.figure("Accuracy Summary")
    plt.plot([x[0] for x in training_accuracies], [x[1] for x in training_accuracies], label="Training Accuracy")
    plt.plot([x[0] for x in testing_accuracies], [x[1] for x in testing_accuracies], label="Testing Accuracy")
    plt.legend()

    plt.show()

def save_as_pickle(obj, file_path):
    with open(file_path, "wb") as pckl:
        pickle.dump(obj, pckl, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(file_path):
    with open(file_path, "rb") as pckl:
            obj =  pickle.load(pckl)
    return obj

def early_stopping(testing_mse, n = 3):
    # first extract only the mse value, getting rid of the epochs
    testing_mse = [x[1] for x in testing_mse]

    # check if the smallest mse was in the last n epochs; if yes continue
    if min(testing_mse) in testing_mse[-n:]:
        return False
    else:
        print("[!] EARLY STOPPING CRITERIA TRIGGERED")
        return True
