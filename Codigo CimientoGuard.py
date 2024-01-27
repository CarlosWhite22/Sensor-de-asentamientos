import machine
import network
import utime
import urequests

# Configuración de pines
pin_buzzer = machine.Pin(25, machine.Pin.OUT)
pin_led1 = machine.Pin(32, machine.Pin.OUT)
pin_led2 = machine.Pin(33, machine.Pin.OUT)
pin_led3 = machine.Pin(14, machine.Pin.OUT)
pin_led4 = machine.Pin(27, machine.Pin.OUT)
pin_sensor_inclinacion1 = machine.Pin(35, machine.Pin.IN)
pin_sensor_inclinacion2 = machine.Pin(34, machine.Pin.IN)
pin_sensor_inclinacion3 = machine.Pin(26, machine.Pin.IN)
pin_sensor_inclinacion4 = machine.Pin(13, machine.Pin.IN)

# Configuración inicial
pin_buzzer.value(0)
pin_led1.value(0)
pin_led2.value(0)
pin_led3.value(0)
pin_led4.value(0)

# Configuración WiFi
SSID = "Natalia"
PASSWORD = "Hola123**"

def conectar_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Conectando a WiFi...")
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            utime.sleep(1)
        print("Conexión exitosa")
    else:
        print("Ya conectado a WiFi")

def alerta(sensores_activados):
    # Apagar todos los LEDs
    pin_led1.value(0)
    pin_led2.value(0)
    pin_led3.value(0)
    pin_led4.value(0)

    if sensores_activados:
        # Encender los LEDs correspondientes a los sensores activados
        for sensor in sensores_activados:
            if sensor == 1:
                pin_led1.value(1)
            elif sensor == 2:
                pin_led2.value(1)
            elif sensor == 3:
                pin_led3.value(1)
            elif sensor == 4:
                pin_led4.value(1)

        # Sonido de alerta principal
        for _ in range(3):
            generar_tono(2000, 300)  # Frecuencia: 2000 Hz, Duración: 0.3 segundos
            utime.sleep(0.1)         # Esperar 0.1 segundos entre los pitidos

        # Apagar todos los LEDs después de la alerta
        pin_led1.value(0)
        pin_led2.value(0)
        pin_led3.value(0)
        pin_led4.value(0)

        # Enviar mensaje a Telegram
        enviar_mensaje_telegram("Se detecta asentamientos en las zapatas: {}".format(sensores_activados))
    else:
        print("Zapatas sin ningún asentamiento")

def generar_tono(frecuencia, duracion):
    pwm = machine.PWM(pin_buzzer)
    pwm.freq(frecuencia)
    pwm.duty(10)
    utime.sleep_ms(duracion)
    pwm.deinit()

def enviar_mensaje_telegram(mensaje):
    # Token del bot de Telegram
    token_telegram = "6775712426:AAFLFUe0ynhZe0vtWyr3E8XV-syxlGIqmqU"
    # ID de chat al que enviar el mensaje (puede ser tu propio ID de chat o el ID de un grupo)
    chat_id = "241806545"

    # URL de la API de Telegram para enviar mensajes
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(token_telegram, chat_id, mensaje)

    # Enviar la solicitud HTTP
    response = urequests.get(url)
    # Imprimir la respuesta del servidor (puedes comentar esta línea si no quieres ver la respuesta)
    print("Respuesta del servidor Telegram:", response.text)

def main():
    conectar_wifi()

    tiempo_entre_mensajes = 10  # Cambia este valor a la frecuencia deseada en segundos
    tiempo_ultimo_mensaje = utime.ticks_ms()

    while True:
        # Leer el valor de los sensores de inclinación
        inclinacion1_detectada = pin_sensor_inclinacion1.value()
        inclinacion2_detectada = pin_sensor_inclinacion2.value()
        inclinacion3_detectada = pin_sensor_inclinacion3.value()
        inclinacion4_detectada = pin_sensor_inclinacion4.value()

        sensores_activados = [i for i, val in enumerate([inclinacion1_detectada, inclinacion2_detectada, inclinacion3_detectada, inclinacion4_detectada], start=1) if val == 1]

        if sensores_activados:
            print("Se detecta asentamientos en las zapatas:", sensores_activados)
            alerta(sensores_activados)
            tiempo_ultimo_mensaje = utime.ticks_ms()  # Reinicia el temporizador
        elif utime.ticks_diff(utime.ticks_ms(), tiempo_ultimo_mensaje) >= tiempo_entre_mensajes * 500:
            print("Zapatas sin ningún asentamiento")
            tiempo_ultimo_mensaje = utime.ticks_ms()  # Reinicia el temporizador

if __name__ == "__main__":
    main()

