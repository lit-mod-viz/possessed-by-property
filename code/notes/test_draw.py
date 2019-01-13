import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier as MLP
from draw_neural_net import draw_neural_net

#--------[1] Input data
dataset = np.mat('-1 -1 -1; -1 1 1; 1 -1 1; 1 1 -1')
X_train = dataset
y_train = np.mat('0; 1; 1; 0')
#-----2-2-1
my_hidden_layer_sizes= (2,)
#------2-2-8-1
#my_hidden_layer_sizes= (2, 8,)
#------2-16-16-1
#my_hidden_layer_sizes= (16, 16,)

XOR_MLP = MLP(
    activation='tanh',
    alpha=0.,
    batch_size='auto',
    beta_1=0.9,
    beta_2=0.999,
    early_stopping=False,
    epsilon=1e-08,
    hidden_layer_sizes= my_hidden_layer_sizes,
    learning_rate='constant',
    learning_rate_init = 0.1,
    max_iter=5000,
    momentum=0.5,
    nesterovs_momentum=True,
    power_t=0.5,
    random_state=0,
    shuffle=True,
    solver='sgd',
    tol=0.0001,
    validation_fraction=0.1,
    verbose=False,
    warm_start=False)

XOR_MLP.fit(X_train,y_train)

fig = plt.figure(figsize=(12, 12))
ax = fig.gca()
ax.axis('off')

layer_sizes = [2] + list(my_hidden_layer_sizes) + [1]
draw_neural_net(ax, .1, .9, .1, .9, layer_sizes, XOR_MLP.coefs_, XOR_MLP.intercepts_, XOR_MLP.n_iter_, XOR_MLP.loss_)
fig.savefig('nn_digaram.png')