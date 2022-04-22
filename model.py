from sklearn.model_selection import train_test_split


def train_test_validate_split(dataX, dataY):
    train_ratio = 0.70
    validation_ratio = 0.15
    test_ratio = 0.15

    # train is now 70% of the entire data set
    # the _junk suffix means that we drop that variable completely
    x_train, x_test, y_train, y_test = train_test_split(dataX, dataY, test_size=int((len(dataX)) * test_ratio * 2), stratify=dataY)

    # test is now 15% of the initial data set
    # validation is now 15% of the initial data set
    x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=int((len(dataX)) * test_ratio), stratify=y_test)

    print(len(x_train), len(x_val), len(x_test))

    print(len(y_train), len(y_val), len(y_test))

    print(x_train[0], y_train[0])

    return x_train, x_test, x_val, y_train, y_test, y_val


