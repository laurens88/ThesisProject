from sklearn.model_selection import train_test_split


def train_test_validate_split(data_x, data_y):
    train_ratio = 0.70
    validation_ratio = 0.15
    test_ratio = 0.15

    # train is now 70% of the entire data set
    # the _junk suffix means that we drop that variable completely
    x_train, x_test, y_train, y_test = train_test_split(data_x, data_y,
                                                        test_size=int((len(data_x)) * test_ratio * 2), stratify=data_y)

    # test is now 15% of the initial data set
    # validation is now 15% of the initial data set
    x_val, x_test, y_val, y_test = train_test_split(x_test, y_test,
                                                    test_size=int((len(data_x)) * test_ratio), stratify=y_test)

    return x_train, x_test, x_val, y_train, y_test, y_val
