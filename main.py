import threading
import logging
from info_docs.FileManager import file_manager_instance as file_manager
from Services.ServiceContainer import service_instance as service
from Controllers.BotController import BotController


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def thread_wrapper(target, name):
    try:
        logging.info(f"Starting thread {name}")
        target()
    except Exception as e:
        logging.exception(f"Thread {name} failed with error: {e}")
    finally:
        logging.info(f"Thread {name} stopped")

def main() -> None:
    setup_logging()
    bot = BotController(service, file_manager)

    threads = [
        threading.Thread(
            target=lambda: thread_wrapper(bot.polling, "polling"),
            daemon=True,
            name="PollingThread"
        ),
        threading.Thread(
            target=lambda: thread_wrapper(bot.notif_checker, "notif_checker"),
            daemon=True,
            name="NotificationThread"
        )
    ]

    for t in threads:
        t.start()

    try:
        while True:
            for t in threads:
                t.join(timeout=1.0)
    except KeyboardInterrupt:
        logging.info("Received interrupt, shutting down...")

if __name__ == '__main__':
    main()