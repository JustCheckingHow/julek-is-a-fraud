from data_source import DataSource
import numpy as np
import json

PCA_LOC = 'modules/TFIDF/pca_vecs.npy'
INDEX_LOC = "modules/TFIDF/pca_index.json"
X_PCA = np.load(PCA_LOC)
index_set = json.load(open(INDEX_LOC, 'r'))
index_set = {int(k): v for k, v in index_set.items()}
inverse_indx = {v: k for k, v in index_set.items()}


class TFNeighbour(DataSource):
    def __init__(self, company_name):
        super().__init__(company_name)
        self.company_name = company_name

    def __dot_product(self, x1, x2):
        norm_x1 = np.linalg.norm(x1)
        norm_x2 = np.linalg.norm(x2)
        if norm_x2 == 0 or norm_x1 == 0:
            return 0.0
        return np.sum(x1 * x2) / (norm_x1 * norm_x2)

    def __get_n_max(self, sim_mat, N=5):
        indx = sim_mat.argsort()[-(N + 1):][::-1]
        to_ret = sim_mat[indx]
        if to_ret[0] == 1.0:
            indx = indx[1:]
            to_ret = to_ret[1:]
        else:
            indx = indx[:-1]
            to_ret = to_ret[:-1]

        # retrieve_companies
        companies = []
        to_ret_final = []
        print(indx)
        for idx, score in zip(indx, to_ret):
            try:
                companies.append(index_set[idx])
                to_ret_final.append(score)
            except:
                pass
        return {"nearest_neighbours": companies, "scores": to_ret_final}

    def __compute_sim_matrix(self, vector, matrix):
        prods = []
        for vec in matrix:
            prods.append(self.__dot_product(vec, vector))

        prods = np.asarray(prods)
        return prods

    def __calculate_dot_product(self):
        try:
            company_index = int(inverse_indx[self.company_name])
        except KeyError:
            return {"nearest_neighbours": [], "scores": []}
        vector = X_PCA[company_index]
        mat = self.__compute_sim_matrix(vector, X_PCA)

        return self.__get_n_max(mat, N=40)

    def return_data(self, **kwargs) -> dict:
        return self.__calculate_dot_product()
