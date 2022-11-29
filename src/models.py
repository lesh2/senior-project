import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

#this code is from stack overflow https://stackoverflow.com/questions/55725139/fit-sigmoid-function-s-shape-curve-to-data-using-python
def sigmoid(x, x0, k):
    y = 1/(1 + np.exp(-k * (x-x0)))
    return (y)

def cos_curve(x, x0, k, a, b):
    y = a * (np.cos((k * x) + x0)) + b
    return (y)

def best_fit(x, y, function):
    x = np.array(x)
    y = np.array(y)
    if function == sigmoid:
        p0 = [np.median(x),1]
    else:
        p0 = [0,.5, 1, .5]
    popt, pcov = curve_fit(function, x, y, p0, method = 'dogbox')
    print(popt)
    plt.scatter(x, y, color='purple')
    line = np.linspace(min(x), max(x), 1000)
   
    plt.plot(line, function(line, *popt), color='steelblue', linestyle='--', linewidth=2)
    plt.ylim(0,1)
    plt.title('Defense Regression')
    plt.xlabel('Defense Plus Minus')
    plt.ylabel('Win Percentage')
    return popt

def test_model(values, wins, popt, function):
    x = np.array(values)
    predict = function(x, *popt)
    guesses = []
    num_correct = 0
    for p in predict:
        if p >= .5:
            guesses.append(1)
        else:
            guesses.append(0)
    for i in range(len(guesses)):
        if guesses[i] == wins[i]:
            num_correct += 1
    return num_correct/len(wins)


def display_confusion(x, y, model):
    cm = confusion_matrix(y, model.predict(x))

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(cm)
    ax.grid(False)
    ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
    ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))
    ax.set_ylim(1.5, -0.5)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha='center', va='center', color='red')
    plt.show()

# this code is from https://realpython.com/logistic-regression-python/#:~:text=The%20logistic%20regression%20function%20%F0%9D%91%9D(%F0%9D%90%B1)%20is%20the%20sigmoid%20function,that%20the%20output%20is%200.
def regress_this(values, won):
    x = np.array(values).reshape(-1,1)
    y = np.array(won)
    model = LogisticRegression(solver = 'liblinear', random_state =0).fit(x,y)
    display_confusion(x, y, model)
    print(model.score(x,y))

def dual_prediction(values1, values2, won):
    combined = np.array(values1).reshape(-1,1)
    combined = np.append(combined, np.array(values2).reshape(-1,1), axis = 1)
    won = np.array(won)
    model = LogisticRegression(solver = 'liblinear', random_state =0, multi_class = 'ovr').fit(combined,won)
    print(model.score(combined, won))

def combine_models(popt1, popt2, values1, values2, wins):
    x1 = np.array(values1)
    x2 = np.array(values2)
    prediction1 = sigmoid(x1, *popt1)
    prediction2 = sigmoid(x2, *popt2)
    p_wins = []
    correct = 0
    for i in range(len(prediction1)):
        if (prediction1[i] * prediction2[i]) >= .5:
            p_wins.append(1)
        else:
            p_wins.append(0)
    for i in range(len(p_wins)):
        if p_wins[i] == wins[i]:
            correct += 1
    return (correct/len(wins))
