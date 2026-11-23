"""
TCP-клієнт IPv6 для опитування віддаленого вузла 6LoWPAN.
"""

import socket
import time

# На реальній Raspberry Pi вказується IPv6-адреса іншої плати (напр. fd28:e5e1:86:0:e40c:932d:df85:4be9)
SERVER_ADDR = "::1"
PORT = 2016
POLL_INTERVAL = 10  # інтервал запиту в секундах (за методичкою)


def start_client() -> None:
    """Періодично підключається до сервера та зчитує дані."""
    print("=" * 65)
    print(f"Клієнт запущено | Ціль: [{SERVER_ADDR}]:{PORT}")
    print("=" * 65)

    try:
        while True:
            s6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
            timestamp = time.strftime("%H:%M:%S")
            try:
                s6.connect((SERVER_ADDR, PORT, 0, 0))
                data = s6.recv(1024).decode("utf-8").strip()
                print(f"[{timestamp}] Отримано: {data}")
            except (ConnectionRefusedError, ConnectionResetError):
                print(f"[{timestamp}] Помилка: сервер недоступний")
            finally:
                s6.close()

            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\nРоботу клієнта зупинено користувачем.")


if __name__ == "__main__":
    start_client()