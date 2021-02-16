# keygraph

The goal of this project is to implement the KeyGraph algorithm for chance discovery (Ohsawa et al., 1998; Ohsawa, 2006). It builds on the github/ShinsakuSegawa/keygraph project.

## Installation

Clone the repository, then run `setup.py` to install the required NLTK resources.

To render a KeyGraph, you also need to install a copy of  `Graphviz` (http://www.graphviz.org).

## Usage

Suppose the document you want to analyze is in the file `d1.txt` in the `txt_files` folder. To create a KeyGraph from the text, run:

```bash
python3 key.py d1
```

This creates input for `Graphviz` in the `dot` folder. To render the KeyGraph, run:

```bash
dot -Tpdf dot/d1.dot -o graphs/d1.pdf
```

In generating the KeyGraph, stopwords in the `noise\stopwords.txt` file are used to remove noise words.

## References

Ohsawa, Y., Benson, N. E., & Yachida, M. (1998). KeyGraph: Automatic indexing by co-occurrence graph based on building construction metaphor. International Forum on Research and Technology Advances in Digital Librarie (ADL), 12-18). IEEE.

Ohsawa, Y. (2006). Chance discovery: The current states of art. In: Ohsawa, Y., & Tsumoko, E. (eds.), Chance Discoveries in Real World Decision Making, 3-20. Springer.