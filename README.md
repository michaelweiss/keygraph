# keygraph

The goal of this project is to implement the KeyGraph algorithm for chance discovery (Ohsawa et al., 1998; Ohsawa, 2006). It builds on this project: https://github.com/ShinsakuSegawa/keygraph.

## Installation

Clone the repository, then run `setup.py` to install the required NLTK resources:

```bash
python3 setup.py
```

To run the scripts you need to have Python installed.

## Usage

Suppose the document you want to analyze is in the file `d1.txt` in the `txt_files` folder. To create a keygraph from the text in this document, run:

```bash
python3 keygraph.py d1
```

This creates the file `d1.html` in the `graphs` folder. Open this file to view the keygraph.

When generating a keygraph, stopwords in the `noise\stopwords.txt` file are used to remove noise words. To add more stopwords, add one stopword per line.

There are two hyper-parameters:

- $M$ is the number of high frequency words
- $K$ is the number of keys (chances)

Both are used to eliminate words and connections from the keygraph. $M$ is used during the selection of black nodes and the creation of clusters of black nodes (which represent established concepts). $K$ is the number of red nodes which connect or bridge clusters and represent chances (which represent new concepts). Note that both are upper limits: nodes will only be shown if they are connected to other nodes after the two selection steps (high frequency words and chances).

## Web-based version

A web-based version to access the tool is under development.

## References

Ohsawa, Y., Benson, N. E., & Yachida, M. (1998). KeyGraph: Automatic indexing by co-occurrence graph based on building construction metaphor. International Forum on Research and Technology Advances in Digital Libraries (ADL), 12-18). IEEE.

Ohsawa, Y. (2006). Chance discovery: The current states of art. In: Ohsawa, Y., & Tsumoko, E. (eds.), Chance Discoveries in Real World Decision Making, 3-20. Springer.
