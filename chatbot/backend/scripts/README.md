# Chroma Database Initialization Scripts

This directory contains utility scripts for managing the Chroma vector database used by the chatbot backend.

## `init_chroma_db.py`

A standalone Python script to pre-initialize the Chroma database locally with document embeddings **before containerization**. This eliminates database initialization overhead during container startup.

### Why Pre-initialize?

- **Faster container startup**: Database initialization (loading docs, generating embeddings) is time-consuming. Pre-initializing shifts this work to the build phase.
- **Consistent deployments**: The same database is used in all deployed containers, ensuring consistency.
- **Reduced resource usage**: Container startup doesn't require embedding model overhead.

### Prerequisites

Before running this script, ensure:
1. **Python environment**: Set up with project dependencies (`poetry install` or `pip install -r requirements.txt`)
2. **Ollama service**: Ollama must be running and accessible (the script uses `OllamaEmbeddings` for embeddings)
3. **Documentation files**: The `backend/docs/` directory must contain `.md` files to embed
4. **Environment variables** (if needed): Create `backend/environment/.env` with required API keys and configurations

### Usage

#### Basic usage (default paths)
```bash
# From the chatbot/scripts directory
python init_chroma_db.py
```

This will:
- Load documents from `../backend/docs/`
- Create/reset the database at `../backend/database/`
- Generate embeddings for all local documents

#### With custom paths
```bash
python init_chroma_db.py \
  --docs-path /path/to/custom/docs \
  --db-path /path/to/custom/database
```

#### Append to existing database (don't reset)
```bash
python init_chroma_db.py --no-reset
```

Note: This is useful if you want to add new documents without losing existing embeddings.

### Output

The script creates:
- `backend/database/` directory containing:
  - Chroma database files
  - Two collections: `local_documents` and `web_documents`
  - Embedding data (.parquet files, etc.)

Example successful output:
```
================================================================================
Chroma Database Pre-Initialization Script
================================================================================
Documentation path: /path/to/backend/docs
Database path: /path/to/backend/database
Reset existing database: True
================================================================================
Step 1/3: Initializing Ollama embeddings model...
✓ Ollama embeddings model initialized
Step 2/3: Loading and splitting documents...
✓ Loaded and split documents into 42 sections
Step 3/3: Creating Chroma database and embedding documents...
✓ Chroma database initialized successfully
Database location: /path/to/backend/database
Collections created: 'local_documents', 'web_documents'
================================================================================
✓ Chroma database initialization completed successfully!
================================================================================
You can now build the Docker image and COPY the database directory:
  COPY /path/to/backend/database /project/database/
================================================================================
```

### Docker Integration

After successful initialization, update your Dockerfile to include the pre-initialized database:

```dockerfile
# In the final runtime stage
COPY database/ /project/database/

# Set environment variable to skip runtime initialization
ENV SKIP_DB_INIT=true
```

The container will use the pre-initialized database and skip the expensive initialization step.

### Workflow: Pre-initialize Before Building Docker Image

1. **Prepare documents**:
   - Add or update `.md` files in `backend/docs/`
   - Ensure Ollama service is running

2. **Run pre-initialization**:
   ```bash
   cd chatbot/scripts
   python init_chroma_db.py
   ```

3. **Build Docker image** (with pre-initialized database):
   ```bash
   cd chatbot/backend
   docker build -t chatbot-backend:latest .
   ```

4. **Run container**:
   ```bash
   docker run -p 20000:20000 chatbot-backend:latest
   ```

The database will be ready immediately on startup; no initialization delay.

### Troubleshooting

#### Script fails with "Ollama connection error"
- **Solution**: Ensure Ollama service is running
  ```bash
  # Check if Ollama is running (typically on port 11434)
  curl http://localhost:11434/api/tags
  ```

#### "Documentation directory not found"
- **Solution**: Verify the path to `backend/docs/` exists and is correct
  ```bash
  ls -la ../backend/docs/
  ```

#### "No Markdown files found"
- **Solution**: Ensure `.md` files exist in the docs directory
  ```bash
  ls -la ../backend/docs/*.md
  ```

#### Script hangs during embedding generation
- **Solution**: This is normal for large document sets. The embedding process can take several minutes depending on:
  - Number of documents and sections
  - Embedding model size
  - System resources
- Use `Ctrl+C` to cancel, then investigate logs

#### Database file corruption
- **Solution**: Delete the entire database directory and re-run the script:
  ```bash
  rm -rf ../backend/database
  python init_chroma_db.py
  ```

### Environment Variables

The script respects the same environment variables as the backend:

- `PYTHONPATH`: Should be set correctly for imports (set automatically by the script)
- `OLLAMA_BASE_URL`: URL of the Ollama service (default: http://localhost:11434)
- Any variables in `backend/environment/.env` (API keys, etc.)

### Advanced: Selective Document Embedding

Currently, the script embeds all `.md` files in the `docs/` directory. To selectively embed documents:

1. Create a separate `docs/` subdirectory with only the documents you want
2. Run the script with `--docs-path` pointing to that directory

### Future Enhancements

- Support for web documents (URLs) as CLI arguments
- Incremental updates (only re-embed changed documents)
- Database versioning and metadata tracking
- Parallel document processing for faster embedding

---

**For more information**, see the main README in `backend/README.md`.
