import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score

class MLModel:
    def __init__(self, df: pd.DataFrame, x_cols: list[str], y_col: str, rand_state = 42):
        '''Features is a list of column names that are used for prediction (the independent variables),
        y is the name of the variable that you want to predict. (the dependent variable)
        Rand state is used for the train test split'''
        self._rand_state = rand_state

        self._data = df.copy()
        self._x_cols = x_cols
        self._y_col = y_col

        self._prep_data()
        self._trainX, self._testX, self._trainY, self._testY = self._train_test_split()
        self._model = None

        self._category_dummy_map: dict = None
        self._y_encoding_map: dict = None
        

    def _train_test_split(self):
        x = self._data[self._x_cols]
        y = self._data[self._y_col]
        return train_test_split(x, y, random_state=self._rand_state)

    def _prep_data(self):
        '''This will do things like encoding and other important modifications to the data to get them to work properly.
        After encoding the data, it has to include dummy variables (if any) as features inside of x_col and remove the old
        categorical column feature.
        But specific classes may do other data preparation like how KNN may do normalizations.'''

        # Encoding the independent variables
        category_dummy_map:dict[str, list] = dict()
        categorical_features = self._data[self._x_cols].select_dtypes('object')
        for col in categorical_features:
            category_dummy_map[col] = []
            uniques = self._data[col].unique()
            for i in range(len(uniques) - 1):
                i_val = uniques[i]
                column_name = f'is {i_val}'
                category_dummy_map[col].append(column_name)
                last_index = len(self._data.columns) - 1
                self._data.insert(last_index, column = column_name, value = self._data[col].apply(lambda val: 1 if val == i_val else 0))

                
                self._x_cols.append(column_name)
            
            self._x_cols.remove(col)
            
        self._category_dummy_map = category_dummy_map

        self._encode_y()


    def _encode_y(self):
        # Encoding the dependent variable if it is cateogorical
        original_name = self._y_col
        if self._data[original_name].dtype != 'object':
            return
    
        y_uniques = self._data[original_name].unique()
        self._y_encoding_map = dict()
        count = 0
        for val in y_uniques:
            self._y_encoding_map[val] = count
            count += 1

        encoded_series = []
        for x in self._data[original_name]:
            encoded_series.append(self._y_encoding_map[x])

        new_column_name = f'{original_name}_encoded'

        self._data.insert(
            loc = len(self._data.columns) - 1, 
            column = new_column_name,
            value = encoded_series
            )
        
        self._y_col = new_column_name


    def _train(self):
        if self._model == None:
            return
        self._model.fit(self._trainX, self._trainY)


    def _cross_validate(self, other_model=None) -> float:
        '''Cross validation with accuracy metric is used to test how good the model is.'''
        
        if other_model != None:
            return cross_val_score(other_model, self._trainX, self._trainY, cv=5).mean()

        if self._model == None:
            return
        return cross_val_score(self._model, self._trainX, self._trainY, cv=5).mean()


    def _test(self):
        if self._model == None:
            return

        return self._model.predict(self._testX)


    def optimize(self) -> None:
        '''This is specific to the ML algorithm'''
        
        pass


    def summarize(self) -> dict:
        '''This is also specific to the algorithm. 
        For example: a logistic regression can give you an odds ratio where as KNN can not'''

        pass