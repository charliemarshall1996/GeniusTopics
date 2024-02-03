
import concurrent.futures
import cudf as pd
<<<<<<< Updated upstream
=======
import nvtext
>>>>>>> Stashed changes
import regex
from spellchecker import SpellChecker
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize.treebank import TreebankWordTokenizer
import nltk
# Import WordNetLemmatizer
from nltk.stem import WordNetLemmatizer

# Instantiate WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
tokenizer = TreebankWordTokenizer()
nltk.download("punkt")

# Retrieve english stopwords
stop_words = stopwords.words("english")
    
# Define function to filter words based on pos
def pos_filter(doc):
    # Define excluded pos
    excluded_pos = {'UH', 'RP', 'SYM', 'TO'}
    
    # Tag the PoS
    # tagged_doc = pos_tag(doc)
    
    # Filter words based on pos
    return [(word, tag) for word, tag in pos_tag(doc) if tag not in excluded_pos]

def replace_white_space(doc:str):
    doc = doc.replace('\n',' ').replace('\r', ' ')

    pattern = regex.compile(r"\s{2,}")
    return regex.sub(pattern, " ", doc).strip()

def strip_stop_words(doc:list):
    return [word for word in doc if word not in stop_words]

# Define function to filter words based on pos
def pos_filter(doc):
    # Define excluded pos
    excluded_pos = {'UH', 'RP', 'SYM', 'TO'}
    
    # Tag the PoS
    # tagged_doc = pos_tag(doc)
    
    # Filter words based on pos
    return [(word, tag) for word, tag in pos_tag(doc) if tag not in excluded_pos]

def remove_misspelled(doc):
    checker = SpellChecker()
    correct_words = []
    dont_check_tags = {'NNP', 'NNPS', 'MD', 'FW'}
    misspelled = checker.unknown([word for word, _ in doc])
    for i, (word, tag) in enumerate(doc):
        if tag in dont_check_tags:
            correct_words.append((word, tag))
        else:
            if len(word) > 5:
                checker.distance = 1
            else:
                checker.distance = 2
            if word in misspelled:
                word = checker.correction(word)
            correct_words.append((word, tag))
    return correct_words

VERBS = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
NOUNS = {'NN', 'NNP', 'NNPS', 'NNS'}
ADV = {'RB', 'RBR', 'RBS'}
ADJ = {'JJ', 'JJR', 'JJS'}

lemm_pos = {'n', 'v', 'a', 'r', 's'}
def lemmatize_docs(doc):
    
    doc_words = []
    for word, tag in doc:
        if tag in VERBS:
            tag = 'v'
        if tag in NOUNS:
            tag = 'n'
        if tag in ADV:
            tag = 'r'
        if tag in ADJ:
            tag = 'a'
    for word, tag in doc:             
        if tag in lemm_pos and word:
            doc_words.append(lemmatizer.lemmatize(word, tag))
        elif word:
            doc_words.append(word)
        else:
            continue
            
    return doc_words

def process_document(i, chunk:str):
    print(f'doc {i}')
    sq_brackets_pattern = regex.compile(r"\[([^[\]]*+(?:(?R)[^[\]]*+)*)\]")
    punc_pattern = regex.compile(r"[^\w\s]")

    lyrics = chunk['lyrics'][i]
    lyrics = lyrics.casefold()
    print(f'doc {i} casefolded')
    lyrics = regex.sub(sq_brackets_pattern, "", lyrics)
    print(f'doc {i} sq brackets removed')
    lyrics = replace_white_space(lyrics)
    print(f'doc {i} no white space')
    lyrics = regex.sub(punc_pattern, "", lyrics)
    print(f'doc {i} no punc')
    lyrics = tokenizer.tokenize(lyrics)
    print(f'doc {i} tokenized')
    lyrics = strip_stop_words(lyrics)
    print(f'doc {i} no stop words')
    lyrics = pos_filter(lyrics)
    print(f'doc {i} pos filtered')
    lyrics = remove_misspelled(lyrics)
    print(f'doc {i} remove misspelled')
    lyrics = lemmatize_docs(lyrics)
    print(f'doc {i} lemmatized')
    chunk['clean_lyrics'] = {'clean_lyrics': lyrics}
    print(f"DOC {i} PROCESSED!")
    return chunk

def row_generator(df):
    for i in range(0, len(df)):
        yield i, df[i:i+1]

def preprocess(df: pd.DataFrame, chunk_size=1):
    
    # Remove row with missing title value
    df.dropna(subset=["title"], inplace=True)
    print("dropped na")
    clean_df = pd.DataFrame()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        print("running threads")
        futures = [executor.submit(process_document, i, chunk) for i, chunk in row_generator(df)]
        clean_df = pd.concat([pd.concat([chunk.result()], axis=1) for chunk in concurrent.futures.as_completed(futures)])

    return clean_df
            
    
        
            
if __name__ == "__main__":
<<<<<<< Updated upstream
    df = pd.read_csv('song_lyrics_subset_100.csv')
=======
    df = pd.read_csv('song_lyrics_subset_10000.csv')
>>>>>>> Stashed changes
    preprocessed_df = preprocess(df)
    preprocessed_df.to_csv('Preprocessed_data.csv')
    
