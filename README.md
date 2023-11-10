# Hacker News Autocomplete System

## Overview
This project is an autocomplete system using a trie data structure, sourced from Hacker News titles. It aims to teach the intricacies of building an autocomplete system and explores advanced concepts like Retrieval-Augmented Generation (RAG) and integration with Large Language Models (LLM).

## Features
- **Autocomplete Functionality**: Utilizes a trie data structure for efficient autocomplete suggestions based on Hacker News titles.
- **RAG System**: Leverages the concept of Retrieval-Augmented Generation for enhancing information retrieval and response generation (In progress).
- **LLM Integration**: Uses a Large Language Model to analyze data, identify trends, and generate relevant questions. [Looking options for utilizing open-source LLMs with faster inference methods (tvm, llama.cpp, wasm)].

## TODO
- Extend trie that I could store titles
- Generate embeddings
- Store those embeddings ( interested in sqlite-vss, pgvector)
- Build connections between LLMs and data source