from model import load_data,NeuralNetwork

x_train, x_test, y_train, y_test = load_data(random_state = 41)

#show_data(x_train, y_train)

model = NeuralNetwork()
model.create_posla_net()

model.train(x_train= x_train, y_train = y_train, epochs= 50, learning_rate=1e-4, batch_size= 256)

# model.evaluate(x_test, y_test)
# model.show_resualt()
# #model.save_model(path = './model_data/VGG_model_e50_lr4_bs256.h5')
#model.load_model(path = './model_data/VGG_model.h5')
model.show_prediction(x_test, y_test)
model.evaluate(x_test, y_test)









