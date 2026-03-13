import matplotlib.pyplot as plt
import time
import subprocess

class MonitorTemperaturaRPI:
    def __init__(self, duracion_ventana=60, intervalo=1.0, duracion_total=300, umbral_alerta=70.0, color_normal='green', color_alerta='red'):
        self.duracion_ventana = duracion_ventana  
        self.intervalo = intervalo               
        self.duracion_total = duracion_total      
        self.umbral_alerta = umbral_alerta        
        self.color_normal = color_normal          
        self.color_alerta = color_alerta         

        self.tiempos = []
        self.temperaturas = []
        self.inicio = time.time()

        self.temp_max = -float('inf')
        self.temp_min = float('inf')

        plt.ion()
        self.fig, self.ax = plt.subplots()

    def leer_temperatura(self):
        try:
            salida = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
            temp_str = salida.strip().replace("temp=", "").replace("'C", "")
            return float(temp_str)
        except Exception as e:
            print("Error leyendo temperatura:", e)
            return None

    def actualizar_datos(self):
        ahora = time.time() - self.inicio
        temp = self.leer_temperatura()
        
        if temp is not None:
            self.tiempos.append(ahora)
            self.temperaturas.append(temp)

            if temp > self.temp_max: self.temp_max = temp
            if temp < self.temp_min: self.temp_min = temp

            while self.tiempos and self.tiempos[0] < ahora - self.duracion_ventana:
                self.tiempos.pop(0)
                self.temperaturas.pop(0)

            if temp >= self.umbral_alerta:
                print(f"¡ALERTA! Temperatura alta: {temp}°C")

        return ahora  
    def graficar(self):
        self.ax.clear()

        temp_actual = self.temperaturas[-1] if self.temperaturas else 0
        promedio = sum(self.temperaturas) / len(self.temperaturas) if self.temperaturas else 0

        color_actual = self.color_alerta if temp_actual >= self.umbral_alerta else self.color_normal

        self.ax.plot(self.tiempos, self.temperaturas, color=color_actual, linewidth=2)

        
        titulo = (f"Temperatura CPU Raspberry Pi | Actual: {temp_actual}°C\n"
                  f"Máx: {self.temp_max}°C | Mín: {self.temp_min}°C | Promedio: {promedio:.1f}°C")
        self.ax.set_title(titulo, fontsize=10)
        
        self.ax.set_xlabel(f"Tiempo transcurrido (s) - Ventana visible: {self.duracion_ventana}s")
        self.ax.set_ylabel("Temperatura (°C)")
        self.ax.grid(True)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def ejecutar(self):
        print(f"Iniciando monitoreo por {self.duracion_total} segundos...")
        print(f"Muestreo cada {self.intervalo}s. Umbral de alerta: {self.umbral_alerta}°C.")
        try:
            while plt.fignum_exists(self.fig.number):
                tiempo_actual = self.actualizar_datos()
                self.graficar()

                
                if tiempo_actual >= self.duracion_total:
                    print(f"\nTiempo máximo de {self.duracion_total}s alcanzado. Deteniendo monitoreo...")
                    break

                time.sleep(self.intervalo)

        except KeyboardInterrupt:
            print("\nMonitoreo interrumpido por el usuario.")

        finally:
            print("Monitoreo finalizado.")
            plt.ioff()
            plt.show()  


if __name__ == "__main__":

    
    monitor = MonitorTemperaturaRPI(
        duracion_ventana=30, 
        intervalo=1.0, 
        duracion_total=120, 
        umbral_alerta=60.0, 
        color_normal='green', 
        color_alerta='red'
    )
    monitor.ejecutar()