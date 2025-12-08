from main import create_app, db
import os

### Para activar el entorno virtual desde el CMD: .\Scripts\activate.bat

app = create_app()

app.app_context().push()  # Activa un contexto de aplicación manualmente

if __name__ == '__main__':  # Ejecuta el código dentro del bloque solo si este archivo se ejecuta directamente.
    db.create_all()

    app.run(port = os.getenv("PORT"), debug = True)  # Levantar el servidor Flask
