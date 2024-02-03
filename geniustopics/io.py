import os
import logging
import tempfile
import pandas as pd

temp_dir = tempfile.TemporaryDirectory()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def n_chunk_loader(dataset_path, n, chunk_size, batch_size):
    logger.info("Loading dataset...")

    # Initialize dataframe
    df = pd.DataFrame()

    # Initialize counters
    n_chunk = 0
    n_rap = 0
    n_rb = 0
    n_pop = 0
    n_rock = 0

    batch_records_n = 0
    batch_num = 0
    for chunk in pd.read_csv(dataset_path, chunksize=chunk_size):
        n_chunk += 1
        logger.debug("Number of Rap lyrics: %s, Number of R&B lyrics: %s, Number of Pop lyrics: %s, Number of Rock lyrics: %s",
                     n_rap, n_rb, n_pop, n_rock)

        # filter out rap, r&b, pop, rock
        chunk = chunk[chunk['language'] == 'en']
        chunk = chunk[chunk['tag'] != 'misc']
        rap_chunks = chunk[chunk['tag'] == 'rap']
        rb_chunks = chunk[chunk['tag'] == 'rb']
        pop_chunks = chunk[chunk['tag'] == 'pop']
        rock_chunks = chunk[chunk['tag'] == 'rock']

        batch_records_n += sum([len(rap_chunks), len(rb_chunks),
                               len(pop_chunks), len(rock_chunks)])

        # if rap, r&b, pop, rock < n, append
        if n_rap < n:
            n_rap += len(rap_chunks)
            df = pd.concat([df, rap_chunks])
        if n_rb < n:
            n_rb += len(rb_chunks)
            df = pd.concat([df, rb_chunks])
        if n_pop < n:
            n_pop += len(pop_chunks)
            df = pd.concat([df, pop_chunks])
        if n_rock < n:
            n_rock += len(rock_chunks)
            df = pd.concat([df, rock_chunks])

        if batch_records_n >= batch_size:
            print(df.value_counts("tag"))
            yield df
            df = pd.DataFrame()

        # if rap, r&b, pop, rock >= n, break
        if all([n_rap >= n, n_rb >= n, n_pop >= n, n_rock >= n]):
            break


def batch_files(dataset_path, batch_size):
    logger.info("Batching files...")

    # Read dataset
    df = pd.read_csv(dataset_path)

    # Filter dataset
    df = df[df['language'] == 'en']
    df = df[df['tag'] != 'misc']

    # Calculate total number of batches
    total_batches = len(df) // batch_size + 1
    logger.info("Total number of batches: %s", total_batches)

    # Batch dataset and save
    for batch_num in range(total_batches):
        starting_i = batch_num * batch_size
        ending_i = min((batch_num + 1) * batch_size, len(df))
        batch_df: pd.DataFrame = df[starting_i:ending_i]
        batch_df.to_csv(f'{temp_dir.name}\\batch_{batch_num}.csv', index=False)

    logger.info("Finished batching files...")
    return total_batches


def split_by_genre(df: pd.DataFrame):
    logger.info("Splitting dataset by genre...")
    rap_lyrics = df[df['tag'] == 'rap']['lyrics'].tolist()
    rb_lyrics = df[df['tag'] == 'rb']['lyrics'].tolist()
    pop_lyrics = df[df['tag'] == 'pop']['lyrics'].tolist()
    rock_lyrics = df[df['tag'] == 'rock']['lyrics'].tolist()
    return rap_lyrics, rb_lyrics, pop_lyrics, rock_lyrics


def batch_generator(total_batches):
    try:
        logger.info('Batching files...')
        for batch_num in range(total_batches):
            yield pd.read_csv(f'{temp_dir.name}\\batch_{batch_num}.csv')
    except Exception as e:
        logger.error('BATCH GENERATOR Error: ' + str(e))


def append_to_tempfile(lyrics, genre):
    logger.info("Appending lyrics to temporary file...")
    logger.debug("lyrics: %s, genre: %s", lyrics, genre)
    lyrics = pd.DataFrame([{'lyrics': doc} for doc in lyrics])
    path = f"{temp_dir.name}\\{genre}.csv"
    lyrics.to_csv(path, header=False, index=False, mode='a')
    logger.info("Finished appending lyrics to temporary file to: %s", path)


def tempfile_n_chunk_generator(genre, chunk_size):
    path = f"{temp_dir.name}\\{genre}.csv"
    if os.path.exists(path):
        for doc in pd.read_csv(path, chunksize=chunk_size):
            yield doc
