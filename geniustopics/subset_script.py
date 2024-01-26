from geniustopics.io import n_chunk_loader
import pandas as pd


def main(path, n_per_genre, chunk_size, batch_size):
    df = pd.DataFrame()
    for batch in n_chunk_loader(path, n_per_genre, chunk_size, batch_size):
        df = pd.concat([df, batch])
    df.to_csv(f"song_lyrics_subset_{n_per_genre}.csv", index=False)


if __name__ == "__main__":
    path = "full_song_lyrics.csv"
    n_per_genre = 10000
    chunk_size = 10000
    batch_size = 10000
    main(path, n_per_genre, chunk_size, batch_size)
