
"""Django's command-line utility for administrative tasks."""

import os
import sys
from multiprocessing import Process
from tutoacademy_chatApp_ms.queue.consumer import connect_consume
from django.core.management import execute_from_command_line

def run_consumer():
    connect_consume()

def main():
    """Ejecuta tareas administrativas."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        # Starts the consumer process
        consumer_process = Process(target=run_consumer)
        consumer_process.start()

        # Starts the Django server
        execute_from_command_line(sys.argv)

    except KeyboardInterrupt:
        #Finishes the consume process when the program gets interrupted
        consumer_process.terminate()
        print("Programa interrumpido")

if __name__ == '__main__':
    main()



