# TripCostPro

<p align="center">
  <img src="./img/logo_MATTSsmall.png" alt="TripCostPro Logo" width="300px" />
</p>

A Streamlit dashboard for analyzing and predicting trip expenses, using the uv package manager.

---

## Getting Started and Deployment

Choose one of the methods below to run the application depending on your setup.

### Method 1: Local Installation

This method requires Python 3.11+ and the uv package manager installed on your machine.

1. Clone the repository and open the project directory.
2. Install the project dependencies:
   ```bash
   uv sync   
    ```
3. Run the application using the command for your operating system:

* **Windows:**
  ```powershell
  uv run streamlit run .\src\dashboarding\main.py
  ```
* **Linux / macOS:**
  ```bash
  uv run streamlit run src/dashboarding/main.py
    ```

---

### Method 2: VS Code Dev Container

Use this method to run the application within an isolated development environment using VS Code and Docker.

1. Install Docker and the Dev Containers extension in VS Code.
2. Open the project folder in VS Code.
3. Open the Command Palette (Ctrl+Shift+P on Windows/Linux or Cmd+Shift+P on Mac).
4. Select the command: `Dev Containers: Rebuild and Open in Container`.

---

### Method 3: Standalone Docker Container

Use this method to build and run the production-ready container on a local machine or a remote server.

```bash
# Build the Docker image
docker build -t tripcostpro .

# Run the container (maps the application to port 8501)
docker run -p 8501:8501 --name tcp-test tripcostpro
```
After finishing with your tests, stop and remove the container to avoid problems of reusing the container name: 
```bash
# Remove the container after stopping it
docker rm -f tcp-test
```

---

## Accessing the Application

Once the application starts using any of the methods above, open your web browser and go to:
```
http://localhost:8501
```

## Stopping the Application
Use `STRG+C` or `CMD+C` in the console or stop the container to stop the application.