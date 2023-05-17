import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle

num_input = 28 
timesteps = 28
n_classes = 10 
learning_rate = 0.001
epochs = 10 
batch_size = 100  
num_hidden_units = 128 

def load_data(mode='train'):
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    
    return x_train, y_train, x_test, y_test
    
def randomize(x, y):
    permutation = np.random.permutation(y.shape[0])
    shuffled_x = x[permutation, :]
    shuffled_y = y[permutation]
    return shuffled_x, shuffled_y

def get_next_batch(x, y, start, end):
    x_batch = x[start:end]
    y_batch = y[start:end]
    return x_batch, y_batch

x_train, y_train, x_valid, y_valid = load_data(mode='train')
print("Size of:")
print("- Training-set:\t\t{}".format(len(y_train)))
print("- Validation-set:\t{}".format(len(y_valid)))

def weight_variable(shape):
    initializer = tf.initializers.TruncatedNormal(stddev=0.01)
    return tf.Variable(initializer(shape), dtype=tf.float32)

def bias_variable(shape):
    return tf.Variable(tf.zeros(shape, dtype=tf.float32))

X = tf.keras.Input(shape=(num_input, timesteps), dtype=tf.float32)
Y = tf.keras.Input(shape=(10,), dtype=tf.float32)


W = weight_variable(shape=[num_hidden_units, n_classes])
b = bias_variable(shape=[n_classes])

def RNN(x, weights, biases, timesteps, num_hidden):
    x = tf.unstack(x, timesteps, axis=1)
    rnn_cell = tf.keras.layers.SimpleRNNCell(num_hidden)
    rnn_layer = tf.keras.layers.RNN(rnn_cell)
    outputs = rnn_layer(tf.stack(x))

    return tf.matmul(outputs[:], weights) + biases

output_logits = RNN(X, W, b, timesteps, num_hidden_units)
y_pred = tf.nn.softmax(output_logits)

cls_prediction = tf.argmax(output_logits, axis=1, name='predictions')

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=output_logits), name='loss')

optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate, name='Adam-op')

correct_prediction = tf.equal(tf.argmax(output_logits, 1), tf.argmax(Y, 1), name='correct_pred')
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='accuracy')

init = tf.compat.v1.global_variables_initializer()
sess = tf.compat.v1.InteractiveSession()
sess.run(init)

global_step = 0
num_tr_iter = int(len(y_train) / batch_size)

for epoch in range(epochs):
    print('Training epoch: {}'.format(epoch + 1))
    x_train, y_train = shuffle(x_train, y_train)
    for iteration in range(num_tr_iter):
        global_step += 1
        start = iteration * batch_size
        end = (iteration + 1) * batch_size
        x_batch, y_batch = get_next_batch(x_train, y_train, start, end)
        x_batch = x_batch.reshape((batch_size, timesteps, num_input))
        
        # Run optimization op (backprop)
        feed_dict_batch = {X: x_batch, Y: y_batch}
        optimizer.minimize(loss, var_list=W + b)
        
        if iteration % 100 == 0:
            # Calculate and display the batch loss and accuracy
            loss_batch, acc_batch = sess.run([loss, accuracy], feed_dict=feed_dict_batch)
            
            print("iter {0:3d}:\t Loss={1:.2f},\tTraining Accuracy={2:.01%}".format(iteration, loss_batch, acc_batch))

    # Run validation after every epoch
    x_valid_shuffle, y_valid_shuffle = shuffle(x_valid, y_valid)
    x_valid_batch = x_valid_shuffle[:1000].reshape((-1, timesteps, num_input))
    y_valid_batch = y_valid_shuffle[:1000]
    feed_dict_valid = {X: x_valid_batch, Y: y_valid_batch}
    
    loss_valid, acc_valid = sess.run([loss, accuracy], feed_dict=feed_dict_valid)
    print('---------------------------------------------------------')
    print("Epoch: {0}, Loss: {1:.2f}, Training accuracy: {2:.01%}".format(epoch + 1, loss_valid, acc_valid))
    print('---------------------------------------------------------')

    def plot_images(images, cls_true, cls_pred=None, title=None):
    fig, axes = plt.subplots(3, 3, figsize=(9, 9))
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    for i, ax in enumerate(axes.flat):
        # Plot image.
        ax.imshow(np.squeeze(images[i]).reshape(28, 28), cmap='binary')

        # Show true and predicted classes.
        if cls_pred is None:
            ax_title = "True: {0}".format(cls_true[i])
        else:
            ax_title = "True: {0}, Pred: {1}".format(cls_true[i], cls_pred[i])

        ax.set_title(ax_title)

        # Remove ticks from the plot.
        ax.set_xticks([])
        ax.set_yticks([])

    if title:
        plt.suptitle(title, size=20)
    plt.show(block=False)

def plot_example_errors(images, cls_true, cls_pred, title=None):
    incorrect = np.logical_not(np.equal(cls_pred, cls_true))

    incorrect_images = images[incorrect]

    cls_pred = cls_pred[incorrect]
    cls_true = cls_true[incorrect]

    plot_images(images=incorrect_images[0:9],
                cls_true=cls_true[0:9],
                cls_pred=cls_pred[0:9],
                title=title)
    
x_test, y_test = load_data(mode='test')
feed_dict_test = {x: x_test[:1000].reshape((-1, timesteps, num_input)), y: y_test[:1000]}
loss_test, acc_test = sess.run([loss, accuracy], feed_dict=feed_dict_test)
print('---------------------------------------------------------')
print("Test loss: {0:.2f}, test accuracy: {1:.01%}".format(loss_test, acc_test))
print('---------------------------------------------------------')

cls_pred = sess.run(cls_prediction, feed_dict=feed_dict_test)
cls_true = np.argmax(y_test, axis=1)
plot_images(x_test, cls_true, cls_pred, title='Correct Examples')
plot_example_errors(x_test[:1000], cls_true[:1000], cls_pred, title='Misclassified Examples')
plt.show()