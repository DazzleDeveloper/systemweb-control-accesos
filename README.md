# 🧠 SystemWeb – Control de Accesos con Reconocimiento Facial y Análisis Emocional

Sistema web inteligente de autenticación de usuarios mediante visión por computadora, reconocimiento facial y registro de eventos en base de datos. Diseñado para permitir el acceso seguro, registrar emociones predominantes y visualizar trazabilidad desde un dashboard administrativo.

---

## 🚀 Características principales

- 📸 Registro facial de usuarios (mín. 4 imágenes)
- 🔐 Autenticación en tiempo real con codificación facial
- 😃 Detección de emociones (DeepFace o FER)
- 🗂 Registro de logs de acceso: IP, emoción, estado
- 📊 Dashboard administrativo con estadísticas

---

## 🛠 Tecnologías utilizadas

| Categoría       | Herramientas / Librerías                      |
|-----------------|-----------------------------------------------|
| Backend         | Python 3.11, Flask                            |
| Visión          | OpenCV, face_recognition, dlib, DeepFace     |
| Base de datos   | MySQL 8 (Docker o Workbench)                 |
| Frontend        | HTML5, Bootstrap, JavaScript                 |
| Visualización   | Matplotlib, Chart.js, Pandas (próximamente)  |

---

## 💻 Instalación local

### 1. Clonar repositorio

```bash
git clone https://github.com/DazzleDeveloper/systemweb-control-accesos.git
cd systemweb-control-accesos
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
# Activar entorno:
# En Windows
.venv\Scripts\activate
# En Linux/macOS
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🗄 Configuración de la base de datos MySQL

### 🔹 Opción A: Usando Docker (recomendado)

El archivo `docker-compose.yml` ya incluye lo necesario:

```yaml
services:
  mysql:
    image: mysql:8.0
    container_name: systemweb_mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: db_systemweb
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    command: --default-authentication-plugin=mysql_native_password

volumes:
  mysql_data:
```

#### Iniciar contenedor:

```bash
docker-compose up -d
```

Esto creará automáticamente:
- Base de datos: `db_systemweb`
- Usuario: `root`
- Contraseña: `root123`

---

### 🔹 Opción B: Usando MySQL Workbench o phpMyAdmin

#### 1. Crea la base de datos manualmente

```sql
CREATE DATABASE IF NOT EXISTS db_systemweb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE db_systemweb;
```

#### 2. Crea las tablas necesarias

```sql
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    cargo VARCHAR(100),
    email VARCHAR(100),
    ruta_foto VARCHAR(200),
    vector_rostro LONGBLOB,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logs_login (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    ip VARCHAR(50),
    estado ENUM('reconocido', 'fallido'),
    emocion ENUM('feliz','triste','neutral','enojado','sorprendido','asustado','disgustado'),
    dispositivo VARCHAR(100),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
```

---

### 🔐 Parámetros de conexión usados en `db.py`

```python
host="127.0.0.1"
user="root"
password="root123"
database="db_systemweb"
port=3306
```

Asegúrate de que coincidan con tu configuración real.

---

## ▶️ Ejecutar la aplicación

```bash
python run.py
```

- Visita `http://127.0.0.1:5000/registro` para registrar usuarios.
- Visita `http://127.0.0.1:5000/login` para autenticación facial.

---

## 📁 Estructura del proyecto

```
SystemWeb/
│
├── app/
│   ├── routes/          # Rutas Flask (registro, login)
│   ├── static/          # Imágenes capturadas
│   ├── templates/       # HTMLs
│   └── __init__.py      # Configuración app Flask
│
├── database/
│   ├── db.py            # Conexión MySQL
│
├── docker-compose.yml   # Contenedor MySQL
├── requirements.txt
├── run.py               # Punto de inicio Flask
└── README.md
```

---

## ✍️ Autor

**DazzleDeveloper**  
GitHub: [@DazzleDeveloper](https://github.com/DazzleDeveloper)  
Proyecto académico - 2025
