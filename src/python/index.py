import logging

from typing import Dict, List, Optional

import elasticsearch
from elasticsearch.helpers import bulk

from query import Query
from vocabulary import Vocabulary


class Index():
    """Class for managing access Elasticsearch index.

    :param name: Index name
    :type name: str

    :param host Elasticsearch host URL
    :type host: str

    :param port Elasticsearch host port
    :type port: int
    """

    def __init__(
            self,
            name: str,
            host: str = "localhost",
            port: int = 9200,
            ):
        """Constructor method
        """
        self.name = name

        self.es = elasticsearch.Elasticsearch(
                [
                    {
                        'host': host,
                        'port': port,
                        }
                    ],
                timeout = 300
                )

        self.vocabulary = Vocabulary()

        self.ensure_index()

    def ensure_index(self) -> None:
        """Creates or recreates index.

        :raises Exception: if index creation failed
        """
        try:
            self.es.indices.delete(
                index = self.name,
                ignore_unavailable = True
                )

            self.es.indices.create(
                index = self.name,
                body = {
                    'settings' : {
                        'number_of_shards': 2,
                        'number_of_replicas': 1
                        },
                    'mappings': {
                        'properties': {
                            'full_text': {
                                'type': 'text'
                                },
                            }
                        }
                    }
                )

        except Exception as e:
            logging.ERROR(str(e))
            exit(1)

    def _bulk_data_generator(self, texts: List[str]) -> Dict:
        """Generator for document indexing actions.

        :param texts: List of documents
        :type texts: List[str]

        :return: Action
        :rtype: Dict
        """
        for text in texts:
            yield {
                    '_op_type': "index",
                    '_index': self.name,
                    '_source': {
                        'full_text': text,
                        },
                    }

    def add(self, text: str) -> Dict:
        """Adds single document to index and adds its words to vocabulary.

        :param text: Document text
        :type text: str

        :return: Elasticsearch response
        :rtype: Dict
        """
        self.vocabulary.add_words_from(text)

        return self.es.index(
                index = self.name,
                refresh = "wait_for",
                body = {
                    'full_text': text
                    },
                )

    def add_bulk(self, texts: List[str]) -> Dict:
        """Adds many documents to index and adds their words to vocabulary.

        :param text: Document text
        :type text: str

        :return: Elasticsearch response
        :rtype: Dict
        """
        for text in texts:
            self.vocabulary.add_words_from(text)

        return elasticsearch.helpers.bulk(
                client = self.es,
                actions = self._bulk_data_generator(texts),
                refresh = "wait_for",
                )

    def get(self, id: int) -> Dict:
        """Returns document from Index by ID.

        :param id: ID of document in index
        :type id: int

        :return: Elasticsearch response
        :rtype: Dict
        """
        return self.es.get(
                index = self.name,
                id = id,
                )

    def search(self, query: Query) -> Dict:
        """Returns query response from index.

        :param query: Query
        :type query: :class:`Query`

        :return: Elasticsearch response
        :rtype: Dict
        """
        return self.es.search(
                index = self.name,
                body = query.body
                )

    def random_document(self) -> Dict:
        """Returns random document from index.

        :return: Elasticsearch response
        :rtype: Dict
        """
        return self.es.search(
                index = self.name,
                body = {
                    'size': 1,
                    'query': {
                        'function_score': {
                            'query': {
                                'match_all': {}
                                },
                            'random_score': {}
                            }
                        }
                    }
                )

    def explain(self, query: Query, id: int) -> Dict:
        """Returns Elasticsearch explanation for match between query and document by ID.

        :param query: Query
        :type query: :class:`Query`

        :param id: ID of document in index
        :type id: int

        :raises Exception: if ID does not exist in index

        :return: Elasticsearch response
        :rtype: Dict
        """
        try:
            return self.es.explain(
                    index = self.name,
                    id = id,
                    body = query.body,
                    )

        except Exception as e:
            logging.ERROR(str(e))
            exit(1)

