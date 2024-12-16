import os
import subprocess
import time

# Ruta absoluta de Maven
MAVEN_CMD = r"C:\Users\cuell\Downloads\apache-maven-4.0.0-beta-4-bin\apache-maven-4.0.0-beta-4\bin\mvn.cmd"

def get_project_root():
    """
    Obtiene la ruta de la carpeta donde se encuentra este script.
    """
    return os.path.dirname(os.path.abspath(__file__))


def find_jar_file(base_dir, pattern):
    """
    Busca el primer archivo JAR que coincida con el patrón especificado en el directorio base.
    """
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".jar") and pattern in file:
                return os.path.join(root, file)
    raise FileNotFoundError(f"No se encontró un archivo JAR que coincida con '{pattern}' en {base_dir}")


def wait_for_log_output(process, search_text, timeout=60):
    """
    Espera a que la salida del proceso contenga la línea 'search_text'.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        line = process.stdout.readline().decode('utf-8').strip()
        if line:
            print(line)
        if search_text in line:
            print(f"[INFO] Se detectó la línea de texto '{search_text}' en el log.")
            return True
    raise TimeoutError(f"No se detectó el texto '{search_text}' en los logs después de {timeout} segundos.")


def run_java_application(jar_path, main_class=None):
    """
    Ejecuta una aplicación Java usando 'java -jar' o 'java -cp' si se proporciona la clase principal.
    """
    if main_class:
        command = ["java", "-cp", jar_path, main_class]
    else:
        command = ["java", "-jar", jar_path]

    print(f"[INFO] Ejecutando: {' '.join(command)}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return process


def run_command(command, work_dir=None):
    """
    Ejecuta un comando en el sistema operativo y muestra su salida.
    """
    # Asegura que 'mvn' use la ruta completa
    if command[0] == "mvn":
        command[0] = MAVEN_CMD

    print(f"[INFO] Ejecutando comando: {' '.join(command)} en {work_dir if work_dir else 'directorio actual'}")
    process = subprocess.Popen(command, cwd=work_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout:
        print(line.decode('utf-8').strip())
    process.wait()
    if process.returncode != 0:
        raise Exception(f"Error ejecutando el comando: {' '.join(command)}")


def main():
    # Obtiene la ruta raíz del proyecto
    project_root = get_project_root()

    # Rutas relativas de los microservicios y del Init Manager
    init_manager_path = os.path.join(project_root, 'InitManager')
    salud_service_path = os.path.join(project_root, 'Backend_Wakanda_Salud')
    gobierno_service_path = os.path.join(project_root, 'Backend_Wakanda_Gobierno')

    # Compilar los proyectos (si es necesario) usando Maven
    print("[INFO] Compilando Init Manager")
    run_command(["mvn", "clean", "package", "-DskipTests"], work_dir=init_manager_path)

    print("[INFO] Compilando Servicio de Salud")
    run_command(["mvn", "clean", "package", "-DskipTests"], work_dir=salud_service_path)

    print("[INFO] Compilando Servicio de Gobierno")
    run_command(["mvn", "clean", "package", "-DskipTests"], work_dir=gobierno_service_path)

    # Buscar los archivos JAR resultantes de la compilación
    print("[INFO] Buscando archivos JAR...")
    init_manager_jar = find_jar_file(init_manager_path, "InitManager")
    salud_service_jar = find_jar_file(salud_service_path, "BackendWakandaSalud")
    gobierno_service_jar = find_jar_file(gobierno_service_path, "BackendWakandaGobierno")

    print(f"[INFO] Archivo JAR de Init Manager: {init_manager_jar}")
    print(f"[INFO] Archivo JAR de Servicio de Salud: {salud_service_jar}")
    print(f"[INFO] Archivo JAR de Servicio de Gobierno: {gobierno_service_jar}")

    # Ejecutar Init Manager
    print("[INFO] Iniciando Init Manager...")
    init_manager_process = run_java_application(init_manager_jar)

    # Esperar a que Init Manager esté listo
    try:
        wait_for_log_output(init_manager_process, "Todos los microservicios iniciados en orden.", timeout=300)
    except TimeoutError as e:
        print("[ERROR] No se detectó que el Init Manager estuviera listo: ", e)
        init_manager_process.terminate()
        return

    # Ejecutar el servicio de Salud
    print("[INFO] Iniciando Servicio de Salud...")
    salud_service_process = run_java_application(salud_service_jar)
    try:
        wait_for_log_output(salud_service_process, "Started BackendWakandaSaludApplication", timeout=120)
    except TimeoutError as e:
        print("[ERROR] No se detectó que el Servicio de Salud estuviera listo: ", e)
        salud_service_process.terminate()
        return

    # Ejecutar el servicio de Gobierno
    print("[INFO] Iniciando Servicio de Gobierno...")
    gobierno_service_process = run_java_application(gobierno_service_jar)
    try:
        wait_for_log_output(gobierno_service_process, "Started BackendWakandaGobiernoApplication", timeout=120)
    except TimeoutError as e:
        print("[ERROR] No se detectó que el Servicio de Gobierno estuviera listo: ", e)
        gobierno_service_process.terminate()
        return

    print("[INFO] Todos los microservicios se iniciaron correctamente.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("[ERROR] Ocurrió un error inesperado: ", e)
