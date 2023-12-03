# Funny RAG

## Overview
This project is only for educational purpose, it aims to teach myself about the fundemental workflow of RAG (Retrieval-Augmented Generation). The app is powered by FastAPI with Jinja2 template engine. Besides that, for autocomplete system, the trie data structured is also utilized (using submodule named `trie`).

## Features
- **Autocomplete Functionality**: Utilizes a trie data structure for efficient autocomplete suggestions based on LLM generated questions.
- **RAG System**: Leverages the concept of Retrieval-Augmented Generation for enhancing information retrieval and response generation (In progress).
- **LLM Integration**: Uses a Large Language Model to analyze data, identify trends, and generate relevant questions. [Looking options for utilizing open-source LLMs with faster inference methods (tvm, llama.cpp, wasm)].
- **LLM Used**: 
-- Mistral-7B API provided by [together.ai](https://www.together.ai/)
-- GPT-3.5 powered by [OpenAI](https://openai.com/)

## TODO
- Crawl the corresponding post linked urls to: 
-- To generate comprehensive questions for clustered posts.
-- To generate insightful answer.
- Build connections between LLMs and data source
- Deploy to AWS, only using free-tier service.