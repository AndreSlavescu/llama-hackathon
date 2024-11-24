# llama-hackathon

## BACKEND

create a `.env` file with the contents of [`.env.example`](.env.example)

then run:

```
source .env
```

```
pip install -r requirements.txt
fastapi dev main.py
```

### Build llm_generation dependencies

Init the submodule
```
git submodule update --init --recursive
```

Make the build script executable
```
chmod +x llm_generation/build.sh
```

Build the dependencies
```
./llm_generation/build.sh
```
