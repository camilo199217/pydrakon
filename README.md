# SecureAuthAPI

SecureAuthAPI es una API de autenticación segura desarrollada con FastAPI como parte de un portafolio profesional.

## Características principales
- Registro y login de usuarios usando JWT
- Contraseñas encriptadas con bcrypt
- Validación de datos con Pydantic
- Protección contra inyección SQL con SQLModel
- Arquitectura limpia y modular
- Sistema básico de roles y permisos (extensible)
- Logging básico de eventos
- Listo para Docker

## Cómo usar

### Ejecutar localmente
```bash
git clone https://github.com/tuusuario/SecureAuthAPI.git
cd SecureAuthAPI
docker-compose up --build
```

### Endpoints disponibles
- POST `/auth/register` — Registro
- POST `/auth/login` — Login

### Ejemplo curl
```bash
curl -X POST "http://localhost:8000/auth/register" -d "username=testuser&password=testpass"
curl -X POST "http://localhost:8000/auth/login" -d "username=testuser&password=testpass"
```

### Acceso Swagger
Visita: `http://localhost:8000/docs`

## Pruebas
```bash
pytest app/tests/test_auth.py
```

---

Incluye tus comentarios y contribuciones en GitHub. ¡Este proyecto demuestra buenas prácticas de desarrollo seguro!
# secure-auth-api
