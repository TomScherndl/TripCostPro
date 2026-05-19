FROM python:3.12-slim

WORKDIR .

# 1. Install uv directly via pip to avoid external image registry conflicts
RUN pip install --no-cache-dir uv

# 2. Copy dependency files
COPY pyproject.toml uv.lock* ./

# 3. Synchronize dependencies using system Python context
# --system tells uv to skip creating a secondary virtualenv inside the container
RUN uv pip install --system -r pyproject.toml

# 4. Copy the rest of your code
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/dashboarding/main.py", "--server.port=8501", "--server.address=0.0.0.0"]