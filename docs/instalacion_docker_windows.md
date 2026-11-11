# Instalar Docker en Windows y levantar el entorno

Docker Desktop en Windows corre sobre **WSL 2** (un Linux liviano integrado en Windows). En la máquina
donde armamos el repo, WSL no estaba instalado y la virtualización figuraba deshabilitada, así que
estos son los pasos completos.

## 1. Virtualización

Abrir el Administrador de tareas → Rendimiento → CPU y mirar **Virtualización**.

- Si dice **Habilitado**, pasar al paso 2.
- Si dice **Deshabilitado**, habilitarla en la BIOS/UEFI: reiniciar y entrar al setup (suele ser F2,
  F10, F12 o Supr). Buscar *Intel Virtualization Technology (VT-x)* o *SVM Mode* (en AMD) y activarla.

## 2. WSL 2

En PowerShell **como administrador**:

```powershell
wsl --install
```

Reiniciar cuando lo pida. Para verificar: `wsl --status`.

## 3. Docker Desktop

1. Descargar e instalar [Docker Desktop](https://www.docker.com/products/docker-desktop/) y dejar
   marcada la opción **Use WSL 2**. También se puede instalar desde una terminal:

   ```powershell
   winget install --id Docker.DockerDesktop -e
   ```

   Windows pide permiso de administrador: hay que aceptar el aviso **antes de 2 minutos**, porque si
   no, el instalador se cancela (en `%LOCALAPPDATA%\Docker\install-log.txt` aparece "El usuario ha
   cancelado la operación"). Después de instalarlo hay que **reiniciar** o cerrar sesión.
2. Abrir Docker Desktop y esperar a que diga *Engine running*.
3. Verificar en una terminal nueva:

```bash
docker --version
docker run hello-world
```

**Recursos:** el entorno completo usa unos 4 a 6 GB de RAM (Airflow pide al menos 4 GB). Se ajusta en
Docker Desktop → Settings → Resources.

## 4. Levantar el entorno del TP

Desde la raíz del repo:

```bash
docker compose --profile all up -d
```

La primera vez construye las imágenes, así que tarda varios minutos. Para ver el estado:

```bash
docker ps
```

Cuando todos los servicios estén `healthy`:

| Servicio | URL | Usuario / clave |
|---|---|---|
| Airflow | http://localhost:8080 | airflow / airflow |
| MLflow | http://localhost:5001 | — |
| MinIO (consola) | http://localhost:9001 | minio / minio123 |
| API | http://localhost:8800/docs | — |

Para levantar solo MLflow, MinIO y PostgreSQL (por ejemplo, para el notebook del experimento):

```bash
docker compose --profile mlflow up -d
```

## Apagar y limpiar

```bash
docker compose --profile all down         # apaga; los datos quedan en los volúmenes
docker compose down --rmi all --volumes   # borra imágenes y datos
```

## Problemas comunes

- **`port is already allocated`:** otro programa usa ese puerto. Se puede cambiar en `.env`, por ejemplo
  `AIRFLOW_PORT=8081`.
- **Los DAGs no aparecen en Airflow:** el *dag-processor* tarda unos 30 segundos. Si hay un error de
  import, se muestra arriba en la UI. También se pueden revisar los logs con
  `docker compose logs airflow-dag-processor`.
- **Cambié `dockerfiles/airflow/requirements.txt`:** hay que reconstruir con
  `docker compose --profile all up -d --build`.
