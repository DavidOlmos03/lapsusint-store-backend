# LapsusINt Store Backend

## Tecnologías utilizadas
- **Python 3.10+**
- **FastAPI** (framework backend)
- **Uvicorn** (servidor ASGI)
- **AWS DynamoDB** (base de datos NoSQL, local y cloud)
- **Boto3** (cliente AWS para Python)
- **Pydantic** (validación de datos y modelos)
- **Passlib [bcrypt]** (hash de contraseñas)
- **python-jose [cryptography]** (JWT y autenticación)
- **Docker & Docker Compose** (contenedorización y orquestación)

## Requisitos
- Docker y Docker Compose instalados
- (Solo producción AWS) AWS CLI configurado
- En Windows: [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo

## Instrucciones para clonar y ejecutar el proyecto

### 1. Clonar el repositorio
```bash
git clone https://github.com/DavidOlmos03/lapsusint-store-backend.git
cd LapsusINt-Store-Backend
```

### 2. Ejecutar con Docker Compose

#### En Linux
```bash
docker compose -f docker-compose.tests.yml up --build
```
Esto levantará la API en http://localhost:8000/docs y DynamoDB local.

#### En Windows
1. Instala y ejecuta **Docker Desktop**.
2. Abre una terminal (PowerShell o CMD) y navega a la carpeta del proyecto.
3. Ejecuta:
```bash
docker compose -f docker-compose.tests.yml up --build
```
La API estará disponible en http://localhost:8000/docs y DynamoDB local.

---

