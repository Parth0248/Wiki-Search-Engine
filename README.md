# Wiki-Search-Engine
A Search Engine for wikipedia dump

## How to run
1. Download the wikipedia dump from [here](https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2) and extract it.
2. Put it in a directory named `wiki_dump` in the root directory of the project.
3. Run `$ bash index.sh <path_to_wiki_dump> <path_to_inverted_index> invertedindex_stat.txt` to create the inverted index, secondary index and title sheet.
4. Run `$ python3 search.py <path_to_queries_file>` to search for the queries in the inverted index. The top 10 relevant documents with the search time will be stored in **queries_op.txt**.

## Functionality of the files
* **index.sh** - Calls the files to the inverted index, secondary index and title sheet.
* **indexer.py** - Creates inverted index in chunks of 10000 wiki documents and stores it in a directory named `temp`
* **merger.py** - Merges the chunks of inverted index using merge sort and stores it in a file named `temp_final.txt`
* **tfidf.py** - Calculated the idf (*inverse document frequency*) of each term in the inverted index and stores it next to each term in the inverted index. It breaks the inverted index into chunks of 10000 tokens and creates a secondary index which stores the first term and file number of the chunk.
* **tsep.py** - Creates a title sheet which stores the title of each wiki document and its corresponding document id in chunk size of 10000 titles per file.
* **search.py** - Searches for the queries in the inverted index and returns the top 10 relevant documents with the search time.
  
## Performance
* The search queries are processed in 2 seconds on an average.
* The inverted index is 1/12th of the size of the wikipedia dump.
* The indexer takes 12 mins to index 4 GB of wikipedia dump.
* The search output is 84-89% accurate.
* Supports both normal and field specific queries.

## Major implementations
* Porter Stemmer
* Word Tokenizer
* Stopword Removal
* XML parser
* TF-IDF
* Casefolding, Normalization and Token Cleaning