"""This module generates a data file in the form of a JSON.

Given a list of sentences, embeddings of these sentences will be generated using the specified model.
A JSON file with both the text and embeddings are created.
"""

import json

from grag.components.embedding import Embedding
from tqdm import tqdm


def gen_embeddings(data, verbose=True):
    """Generates embeddings for a list of sentences using a specified embedding model.

    Args:
        verbose: 
        data (list): A list of strings containing sentences to generate embeddings for.

    Returns:
        list: A list of embeddings corresponding to the input sentences.

    Example:
        >>> sentences = ["This is the first sentence.", "This is the second sentence."]
        >>> embeddings = gen_embeddings(sentences)
    """
    embedding = Embedding("instructor-embedding", "hkunlp/instructor-xl")
    embedding_instruction = "Represent the sentence for retrieval"
    embedding.embedding_function.query_instruction = embedding_instruction
    embedding_func = embedding.embedding_function.embed_query

    if verbose:
        embeddings = []
        for string in tqdm(data, desc="Generating embeddings"):
            embeddings.append(embedding_func(string))
    else:
        embeddings = [embedding_func(string) for string in data]
    return embeddings


def gen_json(data, save_path, verbose=True):
    """Generates a JSON file containing text data and corresponding embeddings.

    Args:
        verbose: 
        data (list): A list of strings containing text data.
        save_path (str): The path to save the generated JSON file.

    Returns:
        None

    Example:
        >>> texts = ["This is the first text.", "This is the second text."]
        >>> gen_json(texts, 'output.json')
    """
    embeddings = gen_embeddings(data, verbose=verbose)
    dict_ = {}
    if verbose:
        pbar = tqdm(enumerate(zip(data, embeddings)), desc="Generating json")
    else:
        pbar = enumerate(zip(data, embeddings))

    for index, (text, embedding) in pbar:
        dict_[index] = {
            "text": text,
            "embedding": embedding
        }

    with open(save_path, 'w') as f:
        json.dump(dict_, f, indent=4)


if __name__ == '__main__':
    data = [
        'Paris is the capital of France.',
        # 'France is a country in Europe.', 
        'The Eiffel Tower is a wrought-iron lattice tower in Paris.',
        'The Eiffel Tower is one of the most recognisable structures in the world.',
        'The Eiffel Tower has 6 million visitors a year.',
        # 'France is a member of the European Union.',
        'Washington, D.C. is the capital of the United States of America.',
        'The Washington Monument is an obelisk in Washington, D.C.',
        'More than 800,000 people visit the Washington Monument each year.',
        ' The Washington Monument was built to commemorate George Washington.',
        'Both France and the United States of America are members of the NATO.'
    ]

    gen_json(data, save_path='Data/eg_data.json')
