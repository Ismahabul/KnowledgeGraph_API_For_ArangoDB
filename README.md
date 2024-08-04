# Knowledge Graph API

This repository contains a FastAPI application for creating and querying knowledge graphs using ArangoDB. The application consists of two main functionalities:
1. Uploading a PDF or text file to create a graph in ArangoDB.
2. Querying the graph to get responses based on the uploaded data.

## Table of Contents

- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Important Notes](#important-notes)
- [License](#license)

## Installation

To install the necessary dependencies, run the following command:

```sh
pip install fastapi uvicorn python-arango langchain langchain_community
```
Running the Application
To run the application locally, use the following command:
```sh
uvicorn app.main:app --reload
```

#### To run the application using Docker:

1.Build the Docker image:

```sh
docker build -t my_fastapi_app .
```
2/Run the Docker container:

```sh
docker run -p 8000:8000 my_fastapi_app
```

## API Endpoints
### Upload Endpoint
#### URL: /upload/

#### Method: POST

Description: Uploads a PDF or text file and creates a graph in ArangoDB.


Response:

```json
{
    "message": "Graph 'file_name_without_extension' created successfully."
}
```
### Query Endpoint
#### URL: /query/

#### Method: POST

Description: Queries the specific graph in ArangoDB.

Request:

```json
{
    "source": "graph_name",
    "query": "Your query here"
}
```
Response:

```json
{
    "answer": "Response from the graph"
}
```
## Environment Variables
```
OPENAI_API_KEY: Your OpenAI API key.
```
Make sure to set this environment variable before running the application.

### Important Notes
#### Dataset Usage: 
We use only one dataset for one chatbot because it is not possible to track the specific collection for each chatbot. From the client's perspective, they want to use the whole database for data security purposes.
#### Graph Management: 
In the ArangoDB graph database, we have many collections. However, we select specific collections to build a graph. This means we build specific graphs from specific collections. When invoking a query, it responds from the specific graph that we have assigned.
#### Graph Naming: 
When you upload a PDF or text file, it generates collections and creates a graph where the graph name will be the name of the PDF or text file. When invoking a query, it works on the graph, not the collections.
