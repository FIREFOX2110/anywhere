from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    # Ponemos todo el diseño de la página web dentro de esta variable de Python
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Mi Página Web con Flask</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #eef2f3;
                color: #333;
                text-align: center;
                padding: 50px;
                margin: 0;
            }
            .contenedor {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                display: inline-block;
                max-width: 500px;
            }
            h1 {
                color: #2c3e50;
                margin-bottom: 20px;
            }
            p {
                font-size: 16px;
                line-height: 1.6;
                color: #555;
            }
            .boton {
                display: inline-block;
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                text-decoration: none;
                margin-top: 20px;
                font-weight: bold;
                transition: background 0.3s;
            }
            .boton:hover {
                background-color: #2980b9;
            }
        </style>
    </head>
    <body>

        <div class="contenedor">
            <h1>¡Mi aplicación web en la nube! 🚀</h1>
            <p>Esta página no es un archivo estático común; está siendo procesada y entregada dinámicamente por un servidor usando <strong>Python</strong> y el framework <strong>Flask</strong>.</p>
            <p>¡Has completado con éxito tu práctica de PaaS!</p>
            <a href="#" class="boton">¡Hacer clic aquí!</a>
        </div>

    </body>
    </html>
    """
    return html_content