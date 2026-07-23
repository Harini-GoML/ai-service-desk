# AI Service Desk

## Overview

AI Service Desk is a FastAPI-based RESTful application designed to manage IT support tickets efficiently. It provides CRUD operations for ticket management and integrates with AWS Bedrock to generate AI-powered summaries and suggested responses for support tickets.

## Features

- Create support tickets
- Retrieve tickets individually or as a list
- Update ticket information
- Delete tickets
- Filter tickets by priority and status
- AI-powered ticket summarization using AWS Bedrock
- Input validation and error handling
- Integration testing with a dedicated test database

## Technologies Used

- FastAPI
- Python
- PostgreSQL
- SQLAlchemy
- AsyncPG
- Pydantic
- AWS Bedrock
- Boto3
- Pytest
- HTTPX

## AI Integration

The application integrates with AWS Bedrock to summarize support tickets and generate professional response suggestions. Prompt templates are used to maintain consistency and version control for AI interactions.

## Testing

The project includes integration tests covering:

- Ticket Creation
- Ticket Retrieval
- Ticket Update
- Ticket Deletion
- Request Validation
- Error Scenarios

A separate PostgreSQL test database is used to ensure that testing does not affect production data.
