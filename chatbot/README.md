# LaredocMind

## Overview

LaredocMind is an intelligent chatbot platform that enables users to interact with their own documents and data through a modern web interface and a powerful backend. The project is split into two main parts:
- **Frontend:** A React + Tailwind CSS web widget, distributed as an npm package.
- **Backend:** A Python REST API for conversational logic, document processing, and AI model integration.

---

## Quick Setup

### Prerequisites
- **Python 3.11** (required for backend, must be available as `py -3.11`)
- **Node.js** (LTS recommended, required for frontend and npm scripts)
- **winget** (for automatic dependency installation on Windows)

### 1. Clone the repository
```sh
cd LaredocMind
```

### 2. Configure environment variables
- Copy `.env.example` to `.env` in the `backend` directory and fill in the required values.

### 3. Automatic installation (recommended)
Run the following script from the project root to install all dependencies and set up both environments:
```sh
setup_app.bat
```
- The script will check for Python 3.11 and Node.js, installing them if needed.
- If Python or Node.js is installed during this process, you will be asked to close and re-run the script.

### 4. Running the application
To start both backend and frontend in development mode:
```sh
run-app.bat
```
- This will launch both servers in the same terminal session.

---

## Project Structure
```
LaredocMind/
├── backend/         # Python backend (API, business logic, data processing)
├── frontend/        # React frontend (chat widget, npm package)
├── run-app.bat      # Script to run both backend and frontend
├── setup_app.bat    # Script to install all dependencies and set up environments
└── LICENSE
```

- See the `README.md` files in `backend/` and `frontend/` for technical details, development, and publishing instructions.

---

## Usage

1. Open your browser at [http://localhost:21000](http://localhost:21000) (default frontend port).
2. Interact with the chatbot using your own documents.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
