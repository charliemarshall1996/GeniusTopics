# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The versioning suffix is 'i'num, where 'i' signifies iteration and num is the iteration number. The purpose is to denote changes made after iterative findings.

## [Unreleased]

## [0.0.0-i1-dev2] - 2024-01-31

### Added

- Spellchecking of words, to remove incorrect words from analysis.
- cuDF to speed up df operations via GPU.
- Save df after preprocessing.
- PoS tagging, using NLTK.
- PoS Filtering, to filter out undesired PoS.

### Changed

- Split genres after preprocessing.
- Use PoS param in lemmatizer for more accurate transformation.

## [0.0.0-i1-dev1] - 2024-01-26

### Added

- Descriptive text about choice of analysis.
- Descriptive text about choice of preprocessing.
- Descriptive text about choice of model.
- Preprocessing steps.
- genius_topics.ipynb
- Loading the Dataset section to notebook, to show how the dataset is imported.
- Analysis markdown in notebook.
- Subset of lyrics in .csv for analysis.

### Changed

- README.md
