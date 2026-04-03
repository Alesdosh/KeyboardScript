import hid
import time

# Codigo usado para encontrar la instruccion que enciende el led del teclado

VENDOR = 0xc0f4
PRODUCT = 0x07f5

with hid.Device(vid=VENDOR, pid=PRODUCT) as keyboard: # Se obtiene el teclado en base a su vid y pid
    # Probar report IDs distintos (0x00 es el default, pero puede haber otros)
    for report_id in [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]:
        for cmd in [0x10, 0x11, 0x12, 0x20, 0x21, 0x30, 0x41, 0x51, 0xb0, 0xb5]:
            payload = [report_id, cmd, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00]
            try:
                keyboard.write(bytes(payload))
                time.sleep(0.8)
                respuesta = input(f"report=0x{report_id:02x} cmd=0x{cmd:02x} ¿LED iluminación? (Enter=nada): ")
                if respuesta:
                    print(f">>> ENCONTRADO: {payload} -> {respuesta}")
            except Exception as e:
                pass  # ignorar errores silenciosamente