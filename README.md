# Synchronized Video Stream

Simple Flask application that lets multiple users watch the same video in sync.
The interface is styled with [Tailwind CSS](https://tailwindcss.com) to provide
a clean dark theme.

## Setup

Install dependencies (preferably in a virtualenv):

```bash
pip install -r requirements.txt
```

Run the server with a WSGI server:

```bash
gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:5000 app:app
```

This project uses `eventlet` for asynchronous support. To avoid initialization
errors, `eventlet.monkey_patch()` is invoked at the top of `app.py` before any
other imports.

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
  gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:$PORT app:app
  ```

Render instalará las dependencias desde `requirements.txt` y ejecutará el
servidor con el comando indicado.
