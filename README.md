# Synchronized Video Stream

Simple Flask application that lets multiple users watch the same video in sync.

## Setup

Install dependencies (preferably in a virtualenv):

```bash
pip install -r requirements.txt
```

Run the server:

```bash
python app.py
```

Open `http://localhost:5000` in several browser tabs to test synchronization.

## Deploy on Render

Para desplegar la aplicación en [Render](https://render.com), crea un nuevo
**Web Service** y utiliza los siguientes comandos:

- **Build Command**
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**
  ```bash
  python app.py
  ```

Render instalará las dependencias desde `requirements.txt` y ejecutará el
servidor con el comando indicado.
