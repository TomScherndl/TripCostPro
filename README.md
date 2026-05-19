To start the app directly:
In Windows:
``uv run streamlit run .\src\dashboarding\main.py``

Bash in Linux: 
``uv run streamlit run src/dashboarding/main.py`` 

Alternative 1: use Devcontainer
In VSC use `DevContainers: Rebuild and Open in Container`

Alternative 2: Use Docker
```
# build docker image 
docker build -t tripcostpro .

# run docker container
docker run -p 8501:8501 --name tcp-test tripcostpro

# remove docker container after finishing
docker rm -f tcp-test
```