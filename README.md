## Natural Language Interface for Script or API Operations

This repository contains the source code for a project developed as part of the course **Engineering with Generative AI** at **RPTU Kaiserslautern** during the Winter Semester 2023-24. The project aims to bridge the gap between natural language inputs and API operations for managing a todo list, utilizing advanced NLP models.

## Project Overview

The project consists of a user-friendly interface and an intermediary processing layer that transforms natural language inputs into valid API calls. The system is primarily written in Python 3.10, leveraging Dash Plotly for the interface and integrating the Llama 2 70B Chat model and Lang-Chain for natural language processing.

### Key Features:
- **Natural Language Processing:** Converts user inputs into commands for a todo list.
- **User Interface:** Built with Dash Plotly for a smooth user interaction experience.
- **Intermediary Layer:** Integrates Llama 2 70B Chat model and Lang-Chain for processing inputs.

## Getting Started

### Prerequisites
Before you start, ensure you have Python 3.10 installed, and all dependencies from `requirements.txt` are installed in your Python environment.

### Installation
Clone the repository and navigate to the top-level directory:
```bash
git clone <repository-url>
cd path/to/todo-manager/directory/
```

### Running the Application

Execute the following commands to start the application:

```bash
python app.py
```
After starting the application, access it by navigating to `http://127.0.0.1:8050/` in your web browser.

## Project Structure

-   `app.py`: Main entry point for the application.
-   `logic_llm/`: Contains logic for processing and generating todo commands.
-   `custom_llm/`: Handles API calls to the Llama model.

## Design

The design focuses on efficient natural language processing, employing custom prompts and system prompts tailored for specific tasks like adding to the todo list or integrating weather data using the RAG feature.

## Implementation

The application uses Lang-Chain to structure and manage LLM calls efficiently. This modularity allows easy swapping and testing of different models or configurations.

## Reflection

This project integrates cutting-edge AI to create a robust and user-friendly interface for todo list management via natural language inputs. It demonstrates a practical application of generative AI technologies in software engineering.

## License

MIT

## Acknowledgements

- RPTU Kaiserslautern, Department of Computer Science
