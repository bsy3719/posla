from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Flatten, Dense, Activation
from tensorflow.python.keras.layers.convolutional import Conv2D, MaxPooling2D
from tensorflow.python.keras.layers.core import Dropout
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.layers.normalization import BatchNormalization


import numpy as np
import glob
import sys
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

def load_data(path = './training_data/*.npz'):

    x_train = np.empty((0, 120, 320, 1))
    y_train = np.empty((0, 4))
    training_data = glob.glob(path)

    for single_npz in training_data:
        with np.load(single_npz) as data:
            x = data['train']
            y = data['train_labels']
        x = np.reshape(x, (-1, 120, 320, 1))

        x_train = np.vstack((x_train, x))
        y_train = np.vstack((y_train, y))

    # 트레이닝셋을 잘못 만들어서 잘라줘함
    y_train = y_train[:, :-1]

    # train test split, 7:3
    return train_test_split(x_train, y_train, test_size=0.3)

def show_data(x, y):

    plt_row = 5
    plt_col = 5
    plt.rcParams["figure.figsize"] = (10, 10)

    f, axarr = plt.subplots(plt_row, plt_col)

    for i in range(plt_row * plt_col):

        sub_plt = axarr[int(i / plt_row), int(i % plt_col)]
        sub_plt.axis('off')
        sub_plt.imshow(x[i].reshape(120, 320))

        label = np.argmax(y[i])

        if label == 0:
            direction = 'left'
        elif label == 1:
            direction = 'right'
        elif label == 2:
            direction = 'forward'
        elif label == 3:
            direction = 'backward'

        sub_plt_title = str(label) + " : " + direction
        sub_plt.set_title(sub_plt_title)

    plt.show()

class NeuralNetwork():

    def __init__(self):
        pass

    def load_model(self, path):
        print('load model!!')
        self.model = load_model(path)

    def predict(self, data):
        prediction = self.model.predict_classes(data)[0]
        return prediction

    def save_model(self, path):
        print('save model!!')
        self.model.save(path)

    def summary(self):
        self.model.summary()

    def train(self, x_train, y_train, epochs = 50, learning_rate = 1e-3 , batch_size = 32, split_ratio = 0.2):
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.split_ratio = split_ratio

        opt = Adam(lr = self.learning_rate, decay= self.learning_rate / self.epochs)
        self.model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

        self.hist = self.model.fit(x_train, y_train, epochs=self.epochs, batch_size=self.batch_size, validation_split=self.split_ratio, shuffle=True)


    def show_resualt(self):
        plt.subplot(1, 2, 1)
        plt.title('model loss')
        plt.plot(self.hist.history['loss'], label="loss")
        plt.plot(self.hist.history['val_loss'], label="val_loss")
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.title('model accuracy')
        plt.plot(self.hist.history['acc'], label="acc")
        plt.plot(self.hist.history['val_acc'], label="val_acc")
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend()

        plt.show();

    def evaluate(self, x_test, y_test):
        loss_and_metrics = self.model.evaluate(x_test, y_test, self.batch_size)
        print('## evaluation loss and_metrics ##')
        print(loss_and_metrics)


    def show_prediction(self, x_test, y_test):
        xhat_idx = np.random.choice(x_test.shape[0], 10)
        xhat = x_test[xhat_idx]

        yhat_classes = self.model.predict_classes(xhat)

        for i in range(10):
            print('True : ' + str(np.argmax(y_test[xhat_idx[i]])) + ', Predict : ' + str(yhat_classes[i]))



    def create_nvidia_model(self, raw = 120, column = 320, channel = 1):
        print('create nvidia model!!')

        input_shape = (raw, column, channel)

        activation = 'relu'
        keep_prob = 0.5
        keep_prob_dense = 0.5
        classes = 3

        model = Sequential()

        model.add(Conv2D(24, (5, 5), input_shape=input_shape, padding="valid", strides=(2, 2)))
        model.add(Activation(activation))
        model.add(Dropout(keep_prob))

        model.add(Conv2D(36, (5, 5), padding="valid", strides=(2, 2)))
        model.add(Activation(activation))
        model.add(Dropout(keep_prob))

        model.add(Conv2D(48, (5, 5), padding="valid", strides=(2, 2)))
        model.add(Activation(activation))
        model.add(Dropout(keep_prob))

        model.add(Conv2D(64, (3, 3)))
        model.add(Activation(activation))
        model.add(Dropout(keep_prob))

        model.add(Conv2D(64, (3, 3)))
        model.add(Activation(activation))
        model.add(Dropout(keep_prob))

        # FC
        model.add(Flatten())

        model.add(Dense(100))
        model.add(Dropout(keep_prob_dense))

        model.add(Dense(50))
        model.add(Dropout(keep_prob_dense))

        model.add(Dense(10))
        model.add(Dropout(keep_prob_dense))

        model.add(Dense(classes))
        model.add(Activation('softmax'))

        self.model = model

    def create_VGG_model(self, raw=120, column=320, channel=1):
        print('create VGG model!!')

        inputShape = (raw, column, channel)

        init = 'he_normal'
        # init = 'glorot_normal'
        activation = 'relu'
        keep_prob_conv = 0.25
        keep_prob_dense = 0.5

        chanDim = -1
        classes = 3

        model = Sequential()

        # CONV => RELU => POOL
        model.add(Conv2D(32, (3, 3), padding="same", input_shape=inputShape))
        model.add(Activation(activation))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(3, 3)))
        model.add(Dropout(keep_prob_conv))

        # (CONV => RELU) * 2 => POOL
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation(activation))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation(activation))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(keep_prob_conv))

        # (CONV => RELU) * 2 => POOL
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation(activation))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation(activation))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(keep_prob_conv))

        # (CONV => RELU) * 2 => POOL
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation(activation))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation(activation))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(keep_prob_conv))

        # first (and only) set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(1024))
        model.add(Activation(activation))
        model.add(BatchNormalization())
        model.add(Dropout(keep_prob_dense))

        # softmax classifier
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        # return the constructed network architecture
        self.model = model








