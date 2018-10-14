from model import load_data, show_data, NeuralNetwork

x_train, x_test, y_train, y_test = load_data()

#show_data(x_train, y_train)

model = NeuralNetwork()
model.create_VGG_model()
model.train(x_train= x_train, y_train = y_train, epochs= 10)

#model.show_prediction(x_test, y_test)

model.evaluate(x_test, y_test)

model.show_resualt()

#model.save_model(path = './model_data/VGG_model.h5')

#test_model = model.load_model(path = './model_data/VGG_model.h5')



