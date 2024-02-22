import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly

class CustomPCA():
    def __init__(self,df:pd.DataFrame, features:list[str], n_components:int, y:str = None, scale: bool = False) -> None:
        self.df = df
        self.feature_names = features
        self.y = y
        self.n_components = n_components
        self.pca = PCA(n_components=n_components)
        
        self.features = df[self.feature_names]

        self._optimal_PCA_df = None

        f = self.features
        if scale == True:
            f = StandardScaler().fit_transform(f)
            self.features = pd.DataFrame(f, columns=self.feature_names)

        self.pca.fit(f)

    def visualize(self, dimensions:int = 2, scale = False, pca_names: list = None) -> plotly.graph_objs.Figure:
        if not (dimensions in [2,3]):
            raise ValueError('dimensions given was different from 2 and 3. Please give a value that is either 2 or 3.')
        pca = PCA(n_components=dimensions)

        X = None
        if scale:
            X = StandardScaler().fit_transform(self.df[self.feature_names])
        else:
            X = self.df[self.feature_names]
            
        components = pca.fit_transform(X)
        col_names = []
        if pca_names == None:
            col_names = [f'PCA{i}' for i in range(1, dimensions + 1)]
        else:
            col_names = pca_names
        
        pca_df = pd.DataFrame(components, columns=col_names)
        
        if self.y != None:
            pca_df[self.y] = self.df[self.y]    

        if dimensions == 2:
            return px.scatter(pca_df, x = col_names[0], y = col_names[1], color=self.y)

        return px.scatter_3d(pca_df, x=col_names[0], y=col_names[1], z=col_names[2], color=self.y)

    def get_loading_matrix(self) -> pd.DataFrame:
        loading_mat = self.pca.components_
        data = {'variables': self.feature_names}
        for i in range(1, self.n_components+1):
            data[f'PCA{i}'] = loading_mat[i-1]
            data[f'PCA{i}_abs'] = [abs(x) for x in loading_mat[i-1]]

        loading_df = pd.DataFrame(data)

        return loading_df

    def total_explained_ratio(self) -> float:
        return self.pca.explained_variance_ratio_.sum()
    
    def explained_ratio_graph(self) -> plotly.graph_objs.Figure:
        ratio = [x*100 for x in self.pca.explained_variance_ratio_]
        pca_names = [f'PCA{i}' for i in range(1, self.n_components+1)]
        explained_df = pd.DataFrame({'PCA': pca_names, 'Explained Variance %': ratio})
        return px.bar(explained_df, x='PCA', y='Explained Variance %')

    def get_optimal_pca_no_components(self, trials=10, threshold=0.9) -> int:
        no_of_components = []
        explained_ratio_list = []
        for i in range(1, int(min([trials, len(self.feature_names)]))):
            pca_temp = PCA(n_components=i)
            pca_temp.fit(self.features)
            no_of_components.append(i)
            explained_ratio_list.append(pca_temp.explained_variance_ratio_.sum())

        pca_optimal_df = pd.DataFrame({'Components': no_of_components, 'Explained ratio':explained_ratio_list})
        
        self._optimal_PCA_df = pca_optimal_df
        for _, row in pca_optimal_df.iterrows():
            if row[1] >= threshold:
                return int(row[0])
        
        return -1

    def optimize(self, threshold=0.9) -> None:
        #TODO: implement different SVD solvers and pick the best one
        optimal_no = self.get_optimal_pca_no_components(threshold=threshold)
        
        if optimal_no == -1:
            raise Exception(f'Can not be optimized at the threshold level {threshold}. Try reducing it')
        
        self.n_components = optimal_no
        self.pca = PCA(n_components=optimal_no)
        self.pca.fit(self.features)

    def get_projections(self) -> None:
        return self.pca.transform(self.features)

    def get_reduced_dataframe(self) -> pd.DataFrame:
        projections = self.get_projections()
        col_names = []
        col_names = [f'PCA{i}' for i in range(1, self.n_components + 1)]
        df = pd.DataFrame(projections, columns=col_names)
        if self.y != None:
            df[self.y] = self.df[self.y]
        return df