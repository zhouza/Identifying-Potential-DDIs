import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import collections
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans,DBSCAN
import hdbscan

class cluster_model:
    def __init__(self,name):
        self.name=name
    
    def reduce_pca(self,X,n_components):
        self.pca_model = PCA(n_components=n_components)
        self.pca_features = self.pca_model.fit_transform(X)
        self.pca_components = self.pca_model.components_
        
    def plot_pca_var(self,dpi=None):
        plt.figure(dpi=dpi)
        plt.plot(np.cumsum(self.pca_model.explained_variance_ratio_))
        plt.title('Principal Component Analysis')
        plt.xlabel('number of features')
        plt.ylabel('cumulative explained variance')
        plt.show();
        
    def plot_km_score(self,k_list):
        SSEs = []
        sil = []
        for k in k_list:
            km = KMeans(n_clusters=k, random_state=42, max_iter=100, n_jobs=-1)
            km.fit(self.pca_features)
            labels = km.labels_
            try:
                sil_score = silhouette_score(self.clustered_features,self.clustered_clusters)
            except:
                sil_score = 0
            SSEs.append(km.inertia_) 
            sil.append(sil_score)
        fig=plt.figure(figsize=(10,6),dpi=100)
        ax1=fig.add_subplot(2,2,1)
        ax1.plot(k_list, SSEs,)
        ax1.set_xlabel('number of clusters')
        ax1.set_ylabel('SSE')
        ax2=fig.add_subplot(2,2,2)
        ax2.plot(k_list,sil)
        ax2.set_xlabel('number of clusters')
        ax2.set_ylabel('silhouette score')
        plt.tight_layout()
        plt.show();        
    
    def get_clusters(self,cluster_model):
        self.cluster_model = cluster_model
        self.clusters = cluster_model.fit_predict(self.pca_features)
        
    def cluster_info(self):
        self.cluster_counts = collections.Counter(self.clusters)
        clustered_idx = (self.clusters!=-1)
        self.clustered_features = self.pca_features[clustered_idx,:]
        self.clustered_clusters = self.clusters[clustered_idx]
        try:
            self.sil_score = silhouette_score(self.clustered_features,self.clustered_clusters)
        except:
            self.sil_score = 'cannot compute silhouette score'
        print(self.name)
        print('unclustered count = '+str(self.cluster_counts[-1]))
        print('number of clusters = '+str(max(self.cluster_counts.keys())+1))
        print('sil score = ' +str(self.sil_score))
        print('---------------------------')
    
    def tsne_viz(self,perplexity,n_iter):
        '''run after cluster_info()
            perplexity between 5 and 50
        '''
        self.tsne_model = TSNE(n_components=2,perplexity=perplexity,n_iter=n_iter,verbose=1)
        self.tsne_embeddings = self.tsne_model.fit_transform(self.clustered_features)
        cluster_count = max(collections.Counter(self.clustered_clusters).keys())+1
        palette = np.array(sns.color_palette("hls", cluster_count))
        cluster_id = self.clustered_clusters

        f = plt.figure(figsize=(8, 8))
        ax = plt.subplot(aspect='equal')
        sc = ax.scatter(self.tsne_embeddings[:,0], self.tsne_embeddings[:,1], lw=0, s=40,c=palette[cluster_id])
        ax.axis('off')
        ax.axis('tight')
        plt.title('t-SNE clusters')
        plt.show();
    
    def to_pickle(self):
        pickle.dump(self,open('pickles/'+self.name+'.pkl','wb'))
