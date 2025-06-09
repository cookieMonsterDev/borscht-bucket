# Borscht Bucket

This project is a FastAPI-based Media Serve for uploading and serving media files — videos, photos, and documents. That was created for fun))

- [Features](#-features)
- [Local setup](#-local-setup)
- [Deployment with docker](#-deployment-with-docker)
- [Contributing to a project](#-contributing-to-a-project)

## 📖 Features

- **File Uploads:** Upload media files using a simple POST endpoint.
- **Photo & Document Retrieval:** Retrieve photos and documents by slug.
- **Video Streaming:** Supports HTTP Range requests to stream video content efficiently.


## 🚀 Local setup

1. Clone the repository:

```bash
https://github.com/cookieMonsterDev/borscht-bucket.git
cd borscht-bucket
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python3.12 -m venv env
source .env/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt ; pre-commit install --hook-type commit-msg
```

4. Configure your `.env` file with required settings such as `ALLOW_ORIGINS`, `HOST_PATH`, `DIRECTORY_PATH`, `CHUNK_SIZE` e.g:

```env
ORIGINS= '*'
HOST_PATH = 'http://localhost:8000'
DIRECTORY_PATH = '/mnt/e/test'
CHUNK_SIZE = 4096
```

5. Start app in the dev mode:

```bash
fastapi dev ./app/main.py
```

## 💾 Deployment with docker

To build and run the app using Docker:

1. Make sure you have Docker installed.

2. Create a `.env` file in the project root with your configuration variables (see above).

3. If your application needs access to a directory on the host (e.g., /files), ensure that it exists and has appropriate permissions:

```bash 
sudo mkdir -p /files
sudo chown $USER:$USER /files
```

4. Ensure your docker-compose.yml includes a volume mapping like:

``` 
volumes:
  - /files:/files
``` 

5. Build and start the container:

```bash 
docker compose up -d
```

6. The app will be accessible at: http://localhost:8001/docs


## 📝 Contributing to a project

We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) standard to keep our commit history clear and consistent. Each commit message should start with a type that indicates the nature of the change, optionally followed by a scope and a brief description.

Commits examples:

```bash
git commit -m "feat(upload): add support for chunked video uploads"
git commit -m "fix(video): handle multiple range headers correctly"
git commit -m "docs: update README with usage instructions"
```
