<div align="center">
  <h1>ORBIT</h1>
  <h2><strong>Open Retrieval-Based Inference Toolkit</strong></h2>
  
  <p>
    <a href="#sovereignty-and-data-control">Features</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#setup">Installation</a> •
    <a href="#starting-the-orbit-server">Usage</a> •
    <a href="#-license">License</a>
  </p>
</div>

## Overview

ORBIT is a modular, self-hosted toolkit that provides a unified API for open-source AI inference models. It enables you to interact AI models on your own infrastructure, maintaining complete control over your data while eliminating commercial API dependencies.

Visit the ORBIT website for more information: https://orbit.schmitech.ai/

## Sovereignty and Data Control

ORBIT is designed with digital sovereignty in mind, offering several key advantages:

1. **Complete Data Control**: All data processing happens on your infrastructure, ensuring sensitive information never leaves your environment
2. **No External Dependencies**: By eliminating reliance on commercial AI APIs, you maintain full control over your AI capabilities
3. **Compliance Ready**: Self-hosted deployment makes it easier to comply with data residency requirements and privacy regulations
4. **Transparency**: Open-source nature allows full visibility into the system's operations and data handling
5. **Customization**: Ability to modify and adapt the system to meet specific organizational or national requirements

This makes ORBIT particularly valuable for:

- Government agencies requiring sovereign AI capabilities
- Organizations with strict data privacy requirements
- Countries implementing digital sovereignty initiatives
- Enterprises needing to maintain control over their AI infrastructure

## Architecture
<div align="left">
  <img src="docs/orbit-architecture-diagram.svg" width="800" alt="ORBIT Architecture">
</div>

## Quick Start

### System Requirements

- A device (Win/Linux or Mac) with 16GB memory, GPU preferred.
- Python 3.12+
- MongoDB
- Redis (optional)
- Ollama (optional but preferred)
- Elasticsearch (optional)

### Setup

```bash
# Download and extract the latest release
curl -L https://github.com/schmitech/orbit/releases/download/v1.0.0/orbit-1.1.0.tar.gz -o orbit.tar.gz
tar -xzf orbit.tar.gz
cd orbit-1.0.0

# Activate virtual environment
source venv/bin/activate

# Add --help for comand options
./install.sh
```

#### Install Ollama:

https://ollama.com/download

```bash
# Download the models
ollama pull gemma3:1b
ollama pull nomic-embed-text
```

#### Using llama.cpp instead of Ollama
If you prefer not to use Ollama or open any additional ports, you may use the llama_cpp inference option in config.yaml.
First, install the dependencies and download the GGUF model file (by default, it downloads Gemma3:1b from Hugging Face - you can modify the download command to use your preferred model):

```bash
# Download the GGUF model file
curl -L https://huggingface.co/unsloth/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_0.gguf -o ./gguf/gemma3-1b.gguf
```

### Configuration
Edit config.yaml with default settings:
```yaml
general:
  port: 3000
  verbose: false
  https:
    enabled: false
    port: 3443
    cert_file: "./cert.pem"
    key_file: "./key.pem"
  session_id:
    header_name: "X-Session-ID"
    required: true
  inference_provider: "ollama"
  language_detection: true
  inference_only: false
  adapter: "qa-sql"
```

```bash
# Update .env with your MongoDB credentials:
INTERNAL_SERVICES_MONGODB_HOST=localhost
INTERNAL_SERVICES_MONGODB_PORT=27017
INTERNAL_SERVICES_MONGODB_USERNAME=mongo-user
INTERNAL_SERVICES_MONGODB_PASSWORD=mongo-password
```

### Starting the ORBIT server (add --help for options):
```bash
./bin/orbit.sh start
```

### ORBIT client setup:
```bash
pip install schmitech-orbit-client
orbit-chat --url http://localhost:3000
```

<div align="left">
  <img src="https://res.cloudinary.com/dk87ffid0/image/upload/v1748380714/local-chatbot-gif_rvlyzv.gif" width="70%" alt="ORBIT Chat Demo">
</div>

> **Note:** Set `inference_only: false` to enable RAG mode (run `./bin/orbit.sh restart --delete-logs` for the changes to take effect Here a sample DB you use for testing the SQL RAG Adapter:

### Simple SQL RAG Example:

```bash
./sample_db/setup-demo-db.sh sqlite

# Use the key genrerated from previous commnand
orbit-chat --url http://localhost:3000 --api-key orbit_1234567ABCDE
```

Refer to [SQL Retriever Architecture](docs/sql-retriever-architecture.md) for details on the database-agnostic SQL retriever implementation and supported database types.

## 📚 Documentation

For more detailed information, please refer to the following documentation in the `/docs` folder.

## 🤝 Contributing

Contributions are welcome! Please read our [Code of Conduct](CODE_OF_CONDUCT.md) for details the process for submitting pull requests.

## 📃 License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.