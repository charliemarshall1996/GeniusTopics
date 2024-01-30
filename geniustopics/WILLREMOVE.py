import concurrent.futures
from geniustopics.preprocessing import preprocess
from geniustopics.io import batch_files, batch_generator, split_by_genre, n_chunk_loader, append_to_tempfile, tempfile_n_chunk_generator
from gensim.models import TfidfModel, LdaModel
from gensim.corpora.dictionary import Dictionary
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from spellchecker import SpellChecker
from typing import Any
import time
import logging
import threading
from queue import Queue
from typing import List
import regex

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from geniustopics.data.vocab.vocab import get_vocab_lemmas, get_vocab_stop_words

lemmatizer = WordNetLemmatizer()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def remove_new_line(input_string: str):
    """
    Remove new line and carriage return characters from the
    input string.

    Args:
    - `input_string` (`str`): The input string from which new
    line and carriage return 
        characters need to be removed.

    Returns:
    - `str`: The input string with new line and carriage return
    characters removed.
    """
    # logger.info("Removing new line and carriage return characters...")
    logger.debug("Input string: %s", input_string)
    if not isinstance(input_string, str):
        # logger.info("Input string is not a string, returning empty string...")
        return ""
    return input_string.replace("\n", "").replace("\r", "")


def strip_sq_brackets(input_string: str):
    """
    Strip text within square brackets from the input string.

    Args:
    - `input_string` (`str`): The input string from which to
    remove text within square brackets.

    Returns:
    - `str`: The input string with text within square brackets
    removed.
    """
    # logger.info("Stripping square brackets...")
    logger.debug("Input string: %s", input_string)
    pattern = regex.compile(r'\[([^[\]]*+(?:(?R)[^[\]]*+)*)\]')
    if not isinstance(input_string, str):
        # logger.info("Input string is not a string, returning empty string...")
        return ""
    return regex.sub(pattern, '', input_string)


def strip_punctuation(input_string: str):
    """
    Strip punctuation from the input string and return the modified string.

    Args:
    - `input_string` (`str`): The input string from which
    punctuation will be stripped.

    Returns:
    - `str`: The modified string with punctuation stripped.
    """
    # logger.info("Stripping punctuation...")
    logger.debug("Input string: %s", input_string)
    pattern = regex.compile(r"[^\w\s]")
    if not isinstance(input_string, str):
        # logger.info("Input string is not a string, returning empty string...")
        return ""
    # logger.info("Stripping punctuation...")
    return regex.sub(pattern, '', input_string)


def strip_white_space(input_string: str):
    # logger.info("Stripping white space...")
    logger.debug("Input string: %s", input_string)
    pattern = regex.compile(r"\s{2,}")
    if not isinstance(input_string, str):
        # logger.info("Input string is not a string, returning empty string...")
        return ""
    # logger.info("Stripping white space...")
    return regex.sub(pattern, ' ', input_string).strip()


def normalize_case(input_string: str):
    # logger.info("Normalizing case...")
    logger.debug("Input string: %s", input_string)
    if not isinstance(input_string, str):
        # logger.info("Input string is not a string, returning empty string...")
        return ""
    # logger.info("Normalizing case...")
    return input_string.casefold()


def strip_stop_words(input_string: str):
    # logger.info("Stripping stop words...")
    logger.debug("Input string: %s", input_string)
    # Get stop words
    vocab_stop_words = get_vocab_stop_words()
    stop_words = stopwords.words('english')

    # Split the input string into a list of words
    # logger.info("Splitting input string into a list of words...")
    input_list = input_string.split(" ")
    logger.debug("Input list: %s", input_list)
    logger.debug("Input list type: %s", type(input_list))

    # Remove stop words from the list of words
    # logger.info("Removing stop words from the list of words...")
    stop_words_stripped_list = [
        word for word in input_list if word not in stop_words]
    stop_words_stripped_list = [
        word for word in stop_words_stripped_list if word not in vocab_stop_words]

    # Join the list of words back into a string
    # logger.info("Joining the list of words back into a string...")
    return_string = " ".join(stop_words_stripped_list)
    # logger.info("Returning string: %s", return_string)
    return return_string


def lemmatize(input_string: str):
    # logger.info("Lemmatizing...")
    logger.debug("Input string: %s", input_string)
    if not isinstance(input_string, str):
        # logger.info("Input string is not a string, returning empty string...")
        return ""
    # logger.info("Lemmatizing...")
    return lemmatizer.lemmatize(input_string)


def preprocess(list_of_docs, genre):
    logger.debug("LYRICS BEFORE: %s", len(list_of_docs))
    # logger.info("Preprocessing lyrics...")

    # logger.info("Normalizing case...")
    case_normalized_list = [normalize_case(
        doc) for doc in list_of_docs]

    # logger.info("Removing square brackets...")
    sq_bracket_stripped_list = [strip_sq_brackets(
        doc) for doc in case_normalized_list]

    # logger.info("Removing punctuation...")
    punc_stripped_list = [strip_punctuation(
        doc) for doc in sq_bracket_stripped_list]

    # logger.info("Removing white space...")
    white_space_stripped_list = [strip_white_space(
        doc) for doc in punc_stripped_list]

    # logger.info("Removing stop words...")
    stop_words_stripped_list = [strip_stop_words(
        doc) for doc in white_space_stripped_list]

    # logger.info("Lemmatizing...")
    lemmatized_list = [lemmatize(doc)
                       for doc in stop_words_stripped_list if doc]

    # logger.info("Word tokenizing...")
    tokenized_list = [word_tokenize(doc)
                      for doc in lemmatized_list if doc]

    # logger.info("Preprocessing complete.")
    logger.debug("LYRICS AFTER: %s", len(tokenized_list))
    return tokenized_list, genre


lyrics_lock = threading.Lock()

genre_dicts = {
    'rap': Dictionary(),
    'rb': Dictionary(),
    'pop': Dictionary(),
    'rock': Dictionary()
}
misspelled = set()
spell_checked = set()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


def check_english(check_english_q):
    logger.info("Checking Spelling...")
    lyrics = check_english_q.get()
    try:
        for doc in lyrics:
            misspelled_in_doc = set(SpellChecker().unknown(doc))
            for word in misspelled_in_doc:
                misspelled.add(word)
        logger.info("Spelling checked!")
    except:
        pass


def extract_dtm(dct: Dictionary, genre, temp_chunk_size):
    logger.info("Building corpus...")
    corpus = [dct.doc2bow(doc, allow_update=True)
              for doc in tempfile_n_chunk_generator(genre, temp_chunk_size)]

    logger.info("Building tfidf model...")
    model = TfidfModel(corpus)
    logger.info("Building Document-Term Matrix...")
    dtm = model.__getitem__(corpus)

    logger.info("returning dtm...")
    return dtm


def make_word_cloud(dct: dict, genre, colormap):
    logger.info("Making word cloud for genre: %s", genre)

    logger.debug("Retrieving word probabilities for genre: %s", genre)
    word_probs = {}
    for topic, prob in dct.items():
        if topic in word_probs:
            logger.info("Adding prob to topic: %s for genre: %s", topic, genre)
            logger.debug("Topic: %s, Prob: %s", topic, prob)
            word_probs[topic] += prob
        else:
            logger.info(
                "Adding topic to word_probs: %s for genre: %s", topic, genre)
            word_probs[topic] = prob

    logger.info("Making word cloud...")
    wordcloud = WordCloud(background_color="white", max_words=100,
                          width=800, height=400, colormap=colormap).generate_from_frequencies(word_probs)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Genre: {genre} Top Words")
    plt.savefig(f"{genre}_top_words.png")
    plt.show()


def pipeline(docs, genre, *args):
    logger.info("Running pipeline...")
    logger.debug("docs: %s, genre: %s", len(docs), genre)
    vocab: Dictionary = args[0]
    prepped = preprocess(docs, genre)
    if not vocab:
        vocab = Dictionary(prepped)
    else:
        vocab.add_documents(prepped)


def main(dataset_path, n_per_genre, chunk_size, batch_size, temp_chunk_size):
    logger.info("Starting...")
    rap_lda = None
    rb_lda = None
    pop_lda = None
    rock_lda = None
    rap_dict = None
    rb_dict = None
    pop_dict = None
    rock_dict = None

    bows = {
        'rap': Dictionary(),
        'rb': Dictionary(),
        'pop': Dictionary(),
        'rock': Dictionary()
    }

    # load dataset
    logger.info("Loading dataset...")
    total_batches = n_chunk_loader(
        dataset_path, n_per_genre, chunk_size, batch_size)

    logger.info("Preprocessing dataset...")

    batch_num = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_to_batch = [executor.submit(split_by_genre, batch) for batch in n_chunk_loader(
            dataset_path, n_per_genre, chunk_size, batch_size)]
        for batch_future in concurrent.futures.as_completed(future_to_batch):
            logger.info("Processing Batch: %s/%s",
                        batch_num, total_batches)
            rap, rb, pop, rock = batch_future.result()
            batch_num += 1
            future_to_prep = [executor.submit(preprocess, docs, genre) for docs, genre in [
                (rap, "rap"), (rb, "rb"), (pop, "pop"), (rock, "rock")]]
            prepped_futures = concurrent.futures.wait(future_to_prep)

        for prepped_future in prepped_futures.done:
            prepped, genre = prepped_future.result()
            print("Adding docs to dictionary for genre: %s", genre)
            bows[genre].add_documents(prepped)

            append_to_tempfile(prepped, genre)

    # extract
    if bows['rap']:
        rap_dtm = extract_dtm(bows['rap'], "rap", temp_chunk_size)
    if bows['rb']:
        rb_dtm = extract_dtm(bows['rb'], "rb", temp_chunk_size)
    if bows['pop']:
        pop_dtm = extract_dtm(bows['pop'], "pop", temp_chunk_size)
    if bows['rock']:
        rock_dtm = extract_dtm(bows['rock'], "rock", temp_chunk_size)
    # train
    print("Making LDA models...")
    if bows['rap'] and rap_dtm:
        print("Making rap LDA...")
        rap_lda = LdaModel(rap_dtm, id2word=bows['rap'], num_topics=1)
    if bows['rb'] and rb_dtm:
        rb_lda = LdaModel(rb_dtm, id2word=bows['rb'], num_topics=1)
    if bows['pop'] and pop_dtm:
        pop_lda = LdaModel(pop_dtm, id2word=bows['pop'], num_topics=1)
    if bows['rock'] and rock_dtm:
        rock_lda = LdaModel(rock_dtm, id2word=bows['rock'], num_topics=1)

    # Retrieve topics
    print("Retrieving topics...")
    if rap_lda:
        rap_dict = dict(rap_lda.show_topics(
            num_topics=1, num_words=100, formatted=False)[0][1])
    if rb_lda:
        rb_dict = dict(rb_lda.show_topics(
            num_topics=1, num_words=100, formatted=False)[0][1])
    if pop_lda:
        pop_dict = dict(pop_lda.show_topics(
            num_topics=1, num_words=100, formatted=False)[0][1])
    if rock_lda:
        rock_dict = dict(rock_lda.show_topics(
            num_topics=1, num_words=100, formatted=False)[0][1])

    # make word cloud
    print("Making word clouds...")
    if rap_dict:
        make_word_cloud(rap_dict, 'rap', 'spring', )
    if rb_dict:
        make_word_cloud(rb_dict, 'rb', 'summer', )
    if pop_dict:
        make_word_cloud(pop_dict, 'pop', 'autumn', )
    if rock_dict:
        make_word_cloud(rock_dict, 'rock', 'winter', )
    with open("incorrect_spellings.txt", 'w', errors="ignore") as file:
        for word in misspelled:
            print("writing: " + word)
            file.write(word + '\n')


if __name__ == "__main__":
    dataset_path = "full_song_lyrics.csv"
    n_per_genre = 5
    chunk_size = 1
    batch_size = 1
    temp_chunk_size = 1
    main(dataset_path, n_per_genre, chunk_size, batch_size, temp_chunk_size)
