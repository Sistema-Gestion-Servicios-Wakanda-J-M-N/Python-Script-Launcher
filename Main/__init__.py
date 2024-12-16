import os
import subprocess
import time


def get_project_root():
    """Obtiene la ruta de la carpeta donde se encuentra este script."""
    return os.path.dirname(os.path.abspath(__file__))


def run_command(command, work_dir=None):
    """Ejecuta un comando en el sistema operativo."""
    print(f"[INFO] Ejecutando comando: {' '.join(command)} en {work_dir if work_dir else 'directorio actual'}")
    process = subprocess.Popen(command, cwd=work_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout:
        print(line.decode('utf-8').strip())
    process.wait()
    if process.returncode != 0:
        raise Exception(f"Error ejecutando el comando: {' '.join(command)}")


def clone_repo_if_not_exists(repo_url, target_dir):
    """Clona un repositorio Git si no existe localmente."""
    if not os.path.exists(target_dir):
        print(f"[INFO] Clonando repositorio {repo_url} en {target_dir}")
        run_command(["git", "clone", repo_url, target_dir])
    else:
        print(f"[INFO] El directorio {target_dir} ya existe, omitiendo clonación.")


def find_jar_file(base_dir, pattern):
    """Busca el primer archivo JAR que coincida con el patrón especificado."""
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".jar") and pattern in file:
                return os.path.join(root, file)
    raise FileNotFoundError(f"No se encontró un archivo JAR que coincida con '{pattern}' en {base_dir}")


def run_java_application(jar_path):
    """Ejecuta una aplicación Java usando 'java -jar'."""
    command = ["java", "-jar", jar_path]
    print(f"[INFO] Ejecutando: {' '.join(command)}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process


def wait_for_log_output(process, search_text, timeout=60):
    """Espera a que la salida del proceso contenga la línea 'search_text'."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        line = process.stdout.readline().decode('utf-8').strip()
        if line:
            print(line)
        if search_text in line:
            print(f"[INFO] Se detectó la línea de texto '{search_text}' en el log.")
            return True
    raise TimeoutError(f"No se detectó el texto '{search_text}' en los logs después de {timeout} segundos.")


def main():
    # Repositorios a clonar
    repos = {
        "InitManager": "https://github.com/Sistema-Gestion-Servicios-Wakanda-J-M-N/InitManager.git",
        "Backend_Wakanda_Salud": "https://github.com/Sistema-Gestion-Servicios-Wakanda-J-M-N/Backend_Wakanda_Salud.git",
        "Backend_Wakanda_Gobierno": "https://github.com/Sistema-Gestion-Servicios-Wakanda-J-M-N/Backend-Wakanda-Gobierno.git",
    }

    # Directorios base
    project_root = get_project_root()
    services_paths = {name: os.path.join(project_root, name) for name in repos.keys()}

    # Clonar repositorios si no existen
    for service, repo_url in repos.items():
        clone_repo_if_not_exists(repo_url, services_paths[service])

    # Compilar proyectos con Maven
    for service, path in services_paths.items():
        print(f"[INFO] Compilando {service}...")
        run_command(["mvn", "clean", "package", "-DskipTests"], work_dir=path)

    # Buscar archivos JAR
    jars = {
        "InitManager": find_jar_file(services_paths["InitManager"], "InitManager"),
        "BackendWakandaSalud": find_jar_file(services_paths["Backend_Wakanda_Salud"], "BackendWakandaSalud"),
        "BackendWakandaGobierno": find_jar_file(services_paths["Backend_Wakanda_Gobierno"], "BackendWakandaGobierno"),
    }

    # Ejecutar aplicaciones
    print("[INFO] Iniciando Init Manager...")
    init_manager_process = run_java_application(jars["InitManager"])
    try:
        wait_for_log_output(init_manager_process, "Todos los microservicios iniciados en orden.", timeout=300)
    except TimeoutError as e:
        print(f"[ERROR] Init Manager no se inició correctamente: {e}")
        init_manager_process.terminate()
        return

    print("[INFO] Iniciando Servicio de Salud...")
    salud_process = run_java_application(jars["BackendWakandaSalud"])
    wait_for_log_output(salud_process, "Started BackendWakandaSaludApplication", timeout=120)

    print("[INFO] Iniciando Servicio de Gobierno...")
    gobierno_process = run_java_application(jars["BackendWakandaGobierno"])
    wait_for_log_output(gobierno_process, "Started BackendWakandaGobiernoApplication", timeout=120)

    print("[INFO] Todos los microservicios se iniciaron correctamente.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] Ocurrió un error inesperado: {e}")
