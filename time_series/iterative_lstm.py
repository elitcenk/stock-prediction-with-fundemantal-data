import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.callbacks import EarlyStopping
from keras.layers import Dense, LSTM
from keras.layers import Dropout
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from yahoofinancials import YahooFinancials


# Function to clean data extracts
def clean_stock_data(stock_data_list):
    new_list = []
    for rec in stock_data_list:
        if 'type' not in rec.keys():
            if rec['close'] is not None:
                new_list.append(rec)

    return new_list


def create_model(x_train, y_train):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(y_train.shape[1]))
    model.compile(loss='mean_squared_error', optimizer='adam')
    stop_here_please = EarlyStopping(patience=2, monitor='loss')
    model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2, callbacks=[stop_here_please])
    return model


def create_dataset(data_len, data):
    x_train, y_train = [], []
    for i in range(60, data_len):
        x_train.append(data[i - 60:i, :])
        y_train.append(data[i, :])
    x_train, y_train = np.array(x_train, dtype='float64'), np.array(y_train, dtype='float64')
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], x_train.shape[2]))
    return x_train, y_train


finance = YahooFinancials('KOZAL.IS')
data = clean_stock_data(finance.get_historical_price_data('2010-01-01', '2019-12-31', 'weekly')['KOZAL.IS']['prices'])
# creating dataframe
new_data = pd.DataFrame(index=range(0, len(data)), columns=['Date', 'Close', 'High', 'Low'])
for i in range(0, len(data)):
    new_data['Date'][i] = data[i]['formatted_date']
    new_data['Close'][i] = data[i]['close']
    new_data['High'][i] = data[i]['high']
    new_data['Low'][i] = data[i]['low']
# setting index
new_data.index = new_data.Date
new_data.drop('Date', axis=1, inplace=True)
# creating train and test sets
train_data_len = int(len(new_data.values) * 0.9)
test = new_data.values[train_data_len:, :]
# converting dataset into x_train and y_train
scaler = MinMaxScaler(feature_range=(0, 1))

x_train, y_train = create_dataset(train_data_len, scaler.fit_transform(new_data.values))
# create and fit the LSTM network
model = create_model(x_train, y_train)

# predicting 246 values, using past 60 from the train data
inputs = new_data[len(new_data) - len(test) - 60:].values
inputs = inputs.reshape(-1, x_train.shape[2])
inputs = scaler.transform(inputs)

X_test, Y_test = [], []
for i in range(60, inputs.shape[0]):
    X_test.append(inputs[i - 60:i, :])
    Y_test.append(inputs[i, :])
    x, y = np.array(X_test, dtype='float64'), np.array(Y_test, dtype='float64')
    x = np.reshape(x, (x.shape[0], x.shape[1], x.shape[2]))
    model.fit(x, y, epochs=1, batch_size=1, verbose=2)
    model.reset_states()

closing_price = model.predict(x)
closing_price = scaler.inverse_transform(closing_price)

rms = np.sqrt(np.mean(np.power((test - closing_price), 2)))
print('Score : ' + str(rms))

# for plotting
test = new_data[train_data_len:]
test['Predictions'] = closing_price[:, 0]
plt.plot(new_data[:train_data_len]['Close'])
plt.plot(test[['Close', 'Predictions']])
plt.show()
