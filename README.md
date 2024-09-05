# Apollo System

## Description

Apollo is an Architecture and oPen-source system for Orchestrating Large Language mOdels (LLMs) for autonomous decision-making.

## Dependencies

Apollo relies on the following external dependencies:

| Dependency | Version |
|------------|---------|
| Ollama | v0.3.2 |
| Flask | v3.0.3 |
| Jinja2 | v3.1.4 |
| PyPDF2 | v3.0.1 |
| PyMuPDF | v1.24.10 |
| detoxify | v0.5.2 |
| fitz | v0.0.1.dev2 |
| haystack-ai | v2.5 |
| ollama-haystack | v0.0.7 |
| redis | v5.0.8 |

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/abeljohny/apollo.git
   cd apollo
   ```

2. Set up a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Ollama separately following the instructions at [Ollama's official documentation](https://ollama.ai/download).

6. Install Redis following the instructions at [Redis's official documentation](https://redis.io/download).

## Configuration

1. Ensure Redis is running and properly configured.
2. Download the default LLMs used - [llama3.1](https://ollama.com/library/llama3.1) and [gemma2](https://ollama.com/library/gemma2) via Ollama if you wish to run Apollo out-of-the-box.

## Usage

1. Start the Redis database with 
```bash
/opt/homebrew/opt/redis/bin/redis-server /opt/homebrew/etc/redis.conf
```
2. Start the Flask server by running `app.py`.


## Development

- Agents in Apollo can be assigned custom behaviors by overriding the `ModelABC` abstract base class to specify a custom behavior for the specific model in the `models/` directory. 
The agent.py file (method `_instantiate_model`) should also be modified to add a route to this new class.
- Static files (CSS, JavaScript, etc.) are in the `static/` directory.
- HTML templates are stored in the `templates/` directory.
- Utilities used such as Redis and Haystack Retrieval Augmented Generation (RAG) subsystem can be found in the `utils/` directory.

## License

This project is licensed under the GNU General Public License v2.0 - see the LICENSE file for details.

## Acknowledgments

Apollo was designed and developed as part of my CS Masters dissertation project at the University of Nottingham.
