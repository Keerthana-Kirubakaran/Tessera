import numpy as np
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt

def visualize_pca(mosaic, title="TESSERA PCA Visualization"):
    """
    Visualize TESSERA embeddings using PCA (bands → RGB)
    mosaic shape: (bands, height, width)
    """
    bands, h, w = mosaic.shape

    X = mosaic.reshape(bands, -1).T
    mask = ~np.any(np.isnan(X), axis=1)

    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X[mask])

    X_pca = (X_pca - X_pca.min()) / (X_pca.max() - X_pca.min())

    rgb = np.zeros((h * w, 3))
    rgb[mask] = X_pca
    rgb = rgb.reshape(h, w, 3)

    plt.figure(figsize=(10, 10))
    plt.imshow(rgb)
    plt.title(title)
    plt.axis("off")
    plt.show()