import json
import tensorflow as tf
from collections import Counter
from keras.models import Model
from keras.layers import Embedding, Input, Reshape
from keras.layers.merging import Dot
from sklearn.linear_model import LinearRegression
import numpy as np
import random
from sklearn import svm
from numba import jit,cuda


with open('data/wp_movies_10k.ndjson') as fin:
    movies = [json.loads(l) for l in fin]

link_counts = Counter()
for movie in movies:
    link_counts.update(movie[2])
print(link_counts.most_common(10))

top_links = [link for link,c in link_counts.items() if c>=3]
link_to_idx = {link:idx for idx,link in enumerate(top_links)}
movie_to_idx = {movie[0]:idx for idx,movie in enumerate(movies)}
pairs = []
for movie in movies:
    pairs.extend((link_to_idx[link],movie_to_idx[movie[0]]) for link in movie[2] if link in link_to_idx)
pairs_set = set(pairs)
print(len(pairs), len(top_links), len(movie_to_idx))

def movie_embedding_model(embedding_size = 50):
    link = Input(name='link',shape=(1,))
    movie = Input(name='movie',shape=(1,))
    link_embedding = Embedding(name='link_embedding',
                               input_dim=len(top_links),
                               output_dim=embedding_size)(link)
    movie_embedding = Embedding(name='movie_embedding',
                               input_dim=len(movie_to_idx),
                               output_dim=embedding_size)(movie)
    dot = Dot(name='dot_product', normalize=True,axes=2)([link_embedding,movie_embedding])
    merged = Reshape((1,))(dot)
    model = Model(inputs=[link,movie],outputs=[merged])
    model.compile(optimizer='adam',loss='mse')
    return model

model = movie_embedding_model()
model.summary()

random.seed(5)
@jit(target_backend='cuda', forceobj=True)
def batchfier(pairs,positive_samples=50,negative_ratio=10):
    batch_size = positive_samples*(1+negative_ratio)
    batch = np.zeros((batch_size,3))
    while True:
        for idx,(link_id,movie_id) in enumerate(random.sample(pairs,positive_samples)):
            batch[idx,:] = (link_id,movie_id,1)
        idx = positive_samples
        while idx<batch_size:
            movie_id = random.randrange(len(movie_to_idx))
            link_id = random.randrange(len(top_links))
            if not (link_id,movie_id) in pairs_set:
                batch[idx,:] = (link_id,movie_id,-1)
                idx += 1
        np.random.shuffle(batch)
        yield {'link':batch[:,0],'movie':batch[:,1]},batch[:,2]

print(next(batchfier(pairs,positive_samples=3,negative_ratio=2)))

positive_samples_per_batch = 512

@jit(target_backend='cuda', forceobj=True)
def start_play():
    model.fit(
        batchfier(pairs,positive_samples=positive_samples_per_batch,negative_ratio=10),
        epochs=15,
        steps_per_epoch=len(pairs),
        verbose=2
    )

start_play()
