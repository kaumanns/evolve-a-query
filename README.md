# evolve-a-query

A command-line game about evolution and information retrieval.

---

In this game, you play a god who controls he environment of a strange world where the only species is **boolean queries**.

Their **evolutionary fitness** depends on their match with a specific random sentence from a corpus of unique sentences (the "language" of this world).

The goal is to **evolve a population of boolean queries** that matches this sentence well before the rounds are over.

You do not know the sentence and you cannot manipulate the queries directly.

You only know the vocabulary of this language, and your only tools are environmental factors of which you can chose one per round.

If your population of queries dies out, you lose.

## Installation

Install Python dependencies:

```
make setup
```

Install [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html).

Then enable and start Elasticsearch server as a service:

```
$ sudo systemctl enable elasticsearch.service
$ sudo systemctl start elasticsearch.service
```

Without any custom configuration, this initializes an index server on `localhost:9200` by default.
This game assumes the default configuration by default.

Check all options:

```
./evolve-a-query.py -h
```

If you have `swi-prolog` installed, you can rebuild the language file via:

```
make language.txt
```

## Getting started

Run:

```
./evolve-a-query.py language.txt
```

... to run the game on the provided language file.
It contains variations of [Noam Chomsky's famous nonsensical sentence](https://en.wikipedia.org/wiki/Colorless_green_ideas_sleep_furiously) "*colorless green ideas sleep furiously*", generated by a PROLOG Definite Clause Grammar.
All sentences in this file follow the same syntactic structure and make more or less sense, literally.

You can also use your own language file. Just remember: one sentence per line.

*Elasticsearch* is used as the indexing engine.
It also computes the score, or *fitness*, of each query against the secret target sentence.

## Game rules

This is what a query looks like:

```
[+ideas +furiously -colorful -wake]
```

**"+"-prefix** indicates a positive term.
It **must** be in the target sentence for the query to match.

**"-"-prefix** indicates a negative term.
It **must not** be in the target sentence for the query to match.

In each round, you can inspect

- the vocabulary,
- the current population of queries,
- their scores against the secret target sentence
- the average score across the population.

The goal is to maximize the average population score.

Each round allows you to select one of the following evolutionary actions on the population:

---

***Love Is In The Air***

... but for now just clone each individual.

***The Weak Shall Perish***

Remove least fit individuals from population.

***Deus Ex Machina***

Remove random individuals from population.

***Gamma Party***

Apply random mutations throughout population.

***This Town Is Too Small For The Both Of Us***

Remove duplicate genotypes.

---

Then the selected action is applied to the population and new queries and scores are computed.

The game ends after the specified number of rounds, of when your population dies out because your selective pressure was a tad to harsh.

## Testing

Run unit tests with `pytest` via:

```
make test
```

## TODO

### Gameplay

- Save highscores in SQLite database.
- Extend evolutionary actions.
- Parameterize evolutionary actions.
- Implement sexual reproduction of queries (for action "Love Is In The Air").
- Implement more complex search than via boolean queries. Requires more sophisticated evolutionary actions.

### Unit tests

- Extend unit tests.
- Untangle existing unit tests: one test per call.
- Replace repeat pattern for testing random operations with mockups.

### Misc

- Add pydoc documentation to methods.

## Development notes

Update Python requirements:

```
pipreqs .
```

Use virtual environment:

```
python3 -m venv evolve-a-query
source evolve-a-query/bin/activate
```
