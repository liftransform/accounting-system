import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, confusion_matrix, silhouette_score, f1_score

from ml_model import MLModel



def custom_confusion_matrix(true_values, predicted_values, model: MLModel):
    df:pd.DataFrame = pd.DataFrame(
        {
            'True': true_values,
            'Predicted': predicted_values
        }
    )

    encoding_map = {}
    try:
        y_col = model._y_col[: model._y_col.index('_encoded')]
    except:
        y_col = model._y_col

    for i, row in model._data[[y_col, model._y_col]].iterrows():
        encoding_map[row[model._y_col]] = row[y_col]

    print(encoding_map)
    matrix = []
    uniques = list(set(true_values))
    column_names = [y_col] + [encoding_map[i] for i in uniques] + ['precision']

    for index, i in enumerate(uniques):
        temp = []
        
        for j in uniques:
            temp.append(df[(df['True'] == i) & (df['Predicted'] == j)].count()[0])

        temp.append(temp[index] / sum(temp))
        temp = [encoding_map[i]] + temp
        matrix.append(temp)

    return pd.DataFrame(matrix, columns=column_names)


class LogisticML(MLModel):
    def __init__(self, df: pd.DataFrame, x_cols: list[str], y_col: str, rand_state=42):
        super().__init__(df, x_cols, y_col, rand_state)
        self._model = LogisticRegression()
        self._train()
    
    
    def optimize(self) -> None:
        super().optimize()

    def summarize(self) -> dict:
        '''Returns the coefficients, the odds ratio, the confusion matrix, the accuracy.'''
        super().summarize()
        coefficients = self._model.coef_
        odds = np.exp(coefficients)
        predictions = self._model.predict(self._testX)
        matrix = confusion_matrix(self._testY, predictions)
        acc = accuracy_score(self._testY, predictions)
        return {
            'coefficients': coefficients,
            'odds': odds,
            'confusion_matrix': matrix,
            'accuracy': acc
        }



class KNN(MLModel):
    def __init__(self, df: pd.DataFrame, x_cols: list[str], y_col: str, rand_state=42):
        super().__init__(df, x_cols, y_col, rand_state)
        self._model = KNeighborsClassifier()
        self._train()
    
    def _prep_data(self):
        super()._prep_data()

    def optimize(self) -> None:
        '''This will normalize the data'''
        super().optimize()
        for col_name in self._data[self._x_cols]:
            minimum = self._data[col_name].min()
            maximum = self._data[col_name].max()
            self._data[col_name] = self._data[col_name].apply(lambda x: (x - minimum)/ (maximum - minimum))
        self._trainX, self._testX, self._trainY, self._testY = self._train_test_split()
        self._train()
    
    def summarize(self) -> dict:
        '''Returns the confusion matrix, the accuracy of the model'''
        super().summarize()
        predictions = self._model.predict(self._testX)
        matrix = confusion_matrix(self._testY, predictions)
        acc = accuracy_score(self._testY, predictions)
        return {
            'confusion_matrix': matrix,
            'accuracy': acc
        }


class SVMML(MLModel):
    def __init__(self, df: pd.DataFrame, x_cols: list[str], y_col: str, rand_state=42):
        super().__init__(df, x_cols, y_col, rand_state)
        self._model = SVC()
        self._train()

    def optimize(self) -> None:
        '''For now this is just about trying different kernels and 
        picking the one that give the best results (accuracy)'''
        super().optimize()
        kernels = ['linear', 'poly', 'rbf', 'sigmoid']
        kernel_model_map = {
            kernel: SVC(kernel=kernel)
            for kernel in kernels
        }
        kernel_score_map = dict()
        for kernel in kernels:
            model = kernel_model_map[kernel]
            model.fit(self._trainX, self._trainY)
            accuracy = self._cross_validate(model)
            kernel_score_map[kernel] = accuracy
        
        df = pd.DataFrame({
            'kernel': kernels, 
            'score': [kernel_score_map[k] for k in kernels]})
        
        sorted_table = df.sort_values(by=['score'], ascending=False).reset_index().drop(columns='index', axis=1)
        best = sorted_table.loc[0, 'kernel']
        
        print(sorted_table)
        print('Best is', best)
        self._model = kernel_model_map[best]
        self._train()
        

        
    def summarize(self) -> dict:
        predictions = self._model.predict(self._testX)
        matrix = confusion_matrix(self._testY, predictions)
        acc = accuracy_score(self._testY, predictions)
        return {
            'confusion_matrix': matrix,
            'accuracy': acc
        }


class Baysian(MLModel):
    def __init__(self, df: pd.DataFrame, x_cols: list[str], y_col: str, rand_state=42):
        super().__init__(df, x_cols, y_col, rand_state)
        self._model = GaussianNB()
        self._train()
    
    def optimize(self) -> None:
        super().optimize()
    

    def summarize(self) -> dict:
        '''Returns the confusion matrix, the accuracy of the model'''
        super().summarize()
        predictions = self._model.predict(self._testX)
        matrix = confusion_matrix(self._testY, predictions)
        acc = accuracy_score(self._testY, predictions)
        return {
            'confusion_matrix': matrix,
            'accuracy': acc
        }

    
class RandForest(MLModel):
    def __init__(self, df: pd.DataFrame, x_cols: list[str], y_col: str, rand_state=42):
        super().__init__(df, x_cols, y_col, rand_state)
        self._model = RandomForestClassifier()
        self._train()
    
    def _prep_data(self):
        super()._prep_data()

    def summarize(self) -> dict:
        predictions = self._model.predict(self._testX)
        matrix = custom_confusion_matrix(self._testY, predictions, self)
        acc = accuracy_score(self._testY, predictions)
        # print(predictions, self._y_encoding_map)
        return {
            'confusion_matrix': matrix,
            'accuracy': acc,

        }


def pick_classification_model(data: pd.DataFrame, features: list[str], y:str, rand_state = 42, optimized = False) -> MLModel:
    '''Picks a model that gives the best cross validation score.'''
    
    name_model_map: dict[str, MLModel] = dict()
    results: dict[str, int] = dict()
    for ml_class in [LogisticML, KNN, Baysian, SVMML, RandForest]:

        print(f'Training {ml_class.__name__} model with the data...')
        model: MLModel =  ml_class(data, features, y, rand_state)
        if optimized:
            print('=> Optimizing it...')
            model.optimize()

        name_model_map[ml_class.__name__] = model
        
        print('=> Calculating cross validation score...')
        results[ml_class.__name__] = model._cross_validate(None)
    
    # picking the best one----
    score_table= pd.DataFrame({
        'model': list(results.keys()),
        'score': [results[m] for m in results]
    })

    sorted_table = score_table.sort_values(by=['score'], ascending=False).reset_index().drop(axis=1, columns='index')
    best = sorted_table.loc[0, 'model']
    #-----------------
    
    print(sorted_table)
    print(f'------Best is {best}-------')
    return name_model_map[best]
