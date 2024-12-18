import subprocess
import os

def ejecutar_microservicio(nombre, ruta_clases, main_class):
    """
    Ejecuta un microservicio Java usando 'java -cp' con la ruta de las clases y la clase principal.
    """
    comando = f"java -cp \"{ruta_clases}\" {main_class}"
    print(f"[INFO] Iniciando {nombre} con comando: {comando}")
    try:
        proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[INFO] Microservicio '{nombre}' iniciado correctamente.")
        return proceso
    except Exception as e:
        print(f"[ERROR] No se pudo iniciar el microservicio '{nombre}': {e}")
        return None

def detener_microservicio(proceso, nombre):
    """
    Detiene un microservicio en ejecución.
    """
    if proceso:
        proceso.terminate()
        proceso.wait()
        print(f"[INFO] Microservicio '{nombre}' detenido correctamente.")

def main():
    """
    Punto de entrada principal: inicia y gestiona los microservicios.
    """
    # Configuración de rutas y clases principales
    base_dir = os.path.abspath("C:/Users/cuell/OneDrive/Documentos/GitHub/Python-Script-Launcher/Main")
    microservicios = [
        {"nombre": "Backend_Wakanda_Salud", "ruta_clases": os.path.join(base_dir, "Backend_Wakanda_Salud/target/classes"),
         "main_class": "org.example.backend_wakanda_salud.BackendWakandaSaludApplication"},
        {"nombre": "Backend-Wakanda-Agua", "ruta_clases": os.path.join(base_dir, "Backend-Wakanda-Agua/target/classes"),
         "main_class": "org.example.backendwakandaagua.BackendWakandaAguaApplication"},
        {"nombre": "Backend-Wakanda-Trafico", "ruta_clases": os.path.join(base_dir, "Backend-Wakanda-Trafico/target/classes"),
         "main_class": "org.example.backendwakandatrafico.BackendWakandaTraficoApplication"},
        {"nombre": "Backend-Wakanda-Seguridad", "ruta_clases": os.path.join(base_dir, "Backend-Wakanda-Seguridad/target/classes"),
         "main_class": "org.example.backendwakandaseguridad.BackendWakandaSeguridadApplication"},
        {"nombre": "Backend-Wakanda-Residuos", "ruta_clases": os.path.join(base_dir, "Backend-Wakanda-Residuos/target/classes"),
         "main_class": "org.example.backendwakandaresiduos.BackendWakandaResiduosApplication"},
        {"nombre": "Backend-Wakanda-Servicios-Emergencia", "ruta_clases": os.path.join(base_dir, "Backend-Wakanda-Servicios-Emergencia/target/classes"),
         "main_class": "org.example.backendwakandaserviciosemergencia.BackendWakandaServiciosEmergenciaApplication"},
        {"nombre": "Backend-Wakanda-Educacion", "ruta_clases": os.path.join(base_dir, "Backend-Wakanda-Educacion/target/classes"),
         "main_class": "org.example.backendwakandaeducacion.BackendWakandaEducacionApplication"},
        {"nombre": "Backend-Wakanda-Cultura-Ocio-Turismo", "ruta_clases": os.path.join(base_dir, "Backend-Wakanda-Cultura-Ocio-Turismo/target/classes"),
         "main_class": "org.example.backendwakandaculturaocio.BackendWakandaCulturaOcioTurismoApplication"},
        {"nombre": "Backend-Wakanda-Transporte-Movilidad", "ruta_clases": os.path.join(base_dir, "Backend-Wakanda-Transporte-Movilidad/target/classes"),
         "main_class": "org.example.backendwakandamovilidad.BackendWakandaTransporteMovilidadApplication"},
        {"nombre": "Backend-Wakanda-Conectividad-Redes", "ruta_clases": os.path.join(base_dir, "Backend-Wakanda-Conectividad-Redes/target/classes"),
         "main_class": "org.example.backendwakandaredes.BackendWakandaConectividadRedesApplication"},
        {"nombre": "Backend-Wakanda-Energia-Sostenible-Eficiente", "ruta_clases": os.path.join(base_dir, "Backend-Wakanda-Energia-Sostenible-Eficiente/target/classes"),
         "main_class": "org.example.backendwakandaenergia.BackendWakandaEnergiaSostenibleApplication"},
        {"nombre": "Backend-Wakanda-Gobierno", "ruta_clases": os.path.join(base_dir, "Backend-Wakanda-Gobierno/target/classes"),
         "main_class": "org.example.backendwakandagobierno.BackendWakandaGobiernoApplication"},
        {"nombre": "Backend-Wakanda-API-Central", "ruta_clases": os.path.join(base_dir, "Backend-Wakanda-API-Central/target/classes"),
         "main_class": "org.example.backendwakandaapicentral.BackendWakandaApiCentralApplication"}
    ]

    procesos = []

    try:
        print("=== Iniciando microservicios ===")
        for ms in microservicios:
            proceso = ejecutar_microservicio(ms["nombre"], ms["ruta_clases"], ms["main_class"])
            if proceso:
                procesos.append((proceso, ms["nombre"]))

        print("\n=== Todos los microservicios están en ejecución ===")
        print("Presiona Ctrl + C para detener los microservicios.")

        while True:
            pass

    except KeyboardInterrupt:
        print("\n=== Deteniendo microservicios ===")
        for proceso, nombre in procesos:
            detener_microservicio(proceso, nombre)

    finally:
        print("\n=== Ejecución finalizada ===")

if __name__ == "__main__":
    main()
