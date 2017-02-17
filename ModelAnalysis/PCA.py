from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def PCAReduction(X_scaled, classifiers):
    pca = PCA(n_components=2);
    pca.fit(X_scaled);
    plt.figure();
    Projection = pca.fit_transform(X_scaled)
    plt.scatter(Projection[:, 0], Projection[:, 1], s=200, c=classifiers)
    plt.xlabel('principle component 1');
    plt.ylabel('principle component 2');
    plt.title('Dimensional Reduction View of the Predictor Features')
    pca3d = PCA(n_components=3)
    pca3d.fit(X_scaled);
    Projection3D = pca3d.fit_transform(X_scaled);
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(Projection3D[:, 0], Projection3D[:, 1], Projection3D[:, 2], s=400, c=classifiers)
    plt.show()
