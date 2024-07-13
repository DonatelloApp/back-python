# Etapa 1: Construcción de la aplicación
FROM python:3.9-slim AS builder
WORKDIR /app

# Copia y establece las dependencias del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 2: Configuración de la aplicación
FROM builder AS setup
WORKDIR /app
COPY . .

# Etapa 3: Servidor de producción
FROM python:3.9-slim AS production
WORKDIR /app

# Copia los archivos del build anterior
COPY --from=setup /app /app

# Configura variables de entorno
# ENV DJANGO_SETTINGS_MODULE=nombre_de_tu_app.settings.prod

# Configura la ejecución de la aplicación
CMD ["python", "manage.py", "runserver"]
