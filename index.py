import hid
import evdev
import asyncio
import subprocess

# nohup python3 index.py > log.txt 2>&1 &  -> comando usado para correr el script en segundo plano

VENDOR = 0xc0f4 # vendor id del teclado (no cambia)
PRODUCT = 0x07f5 # product id del teclado (no cambia)


# Obtener el event actual del teclado
proceso = subprocess.Popen(
    ["evtest"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

index = 1
encontrado = ""

for i in range(18):
    linea = proceso.stdout.readline()
    if "Usb KeyBoard Usb KeyBoard" in linea and index <= 1:
        print(linea.strip())
        encontrado = linea.strip()
        index+=1

arreglo_encontrados = encontrado.split(":")

KEYBOARD_EVENT = arreglo_encontrados[0] # Se buscara en este archivo de eventos 


proceso.terminate()
proceso.wait()
    

leds_encendidos = False # Se inicializa como falso

def set_leds(encendido): # 
    print(f"Intentando {'encender' if encendido else 'apagar'} LEDs...")
    try:
        with hid.Device(vid=VENDOR, pid=PRODUCT) as keyboard:
            if encendido:
                keyboard.write(bytes([0x00, 0xb5, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00]))
            else:
                keyboard.write(bytes([0x00, 0xb5, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
            print("Comando enviado OK")
    except Exception as e:
        print(f"Error: {e}")

async def main():
    global leds_encendidos
    device = evdev.InputDevice(KEYBOARD_EVENT)

    print("Escuchando tecla de LEDs... (Ctrl+C para salir)")
    async for event in device.async_read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key = evdev.categorize(event)
            if key.keycode == "KEY_SCROLLLOCK" and key.keystate == 1:
                leds_encendidos = not leds_encendidos
                print(f"Estado ahora: {leds_encendidos}")
                set_leds(leds_encendidos)

asyncio.run(main())