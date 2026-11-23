"""
TCP-сервер IPv6 для передачі даних у мережі 6LoWPAN.
"""

import socket
import time

HOST = ""
PORT = 2016


def build_payload() -> bytes:
    """Формує повідомлення з даними студента та посиланням."""
    message = (
        "Student: Маковій Володимир | Група: ЕЛ-24-1 | "
        "Link: http://6lowpan.local/EL-24-1/Makovii_Volodymyr\n"
    )
    return message.encode("utf-8")


def start_server() -> None:
    """Ініціалізує IPv6-сокет та обробляє запити клієнта."""
    s6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
    s6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Перевірка інтерфейсу 6LoWPAN (як на RPi); на ПК переходимо на loopback ::1
    try:
        scope_id = socket.if_nametoindex("lowpan0")
        s6.bind((HOST, PORT, 0, scope_id))
        mode = "6LoWPAN (інтерфейс lowpan0)"
    except (OSError, AttributeError):
        s6.bind(("::1", PORT, 0, 0))
        mode = "локальна емуляція IPv6 (::1)"

    s6.listen(1)

    print("=" * 65)
    print(f"Сервер запущено | Режим: {mode} | Порт: {PORT}")
    print("=" * 65)

    try:
        while True:
            conn, addr = s6.accept()
            timestamp = time.strftime("%H:%M:%S")
            payload = build_payload()
            conn.send(payload)
            print(f"[{timestamp}] Підключення від {addr[0]} -> дані надіслано")
            conn.close()
    except KeyboardInterrupt:
        print("\nРоботу сервера зупинено користувачем.")
    finally:
        s6.close()


if __name__ == "__main__":
    start_server()