from info_docs.FileManager import file_manager_instance as file_manager
from Services.ServiceContainer import service_instance as service
from Controllers.BotController import BotController
import threading


def main() -> None:
    bot = BotController(service, file_manager)
    threading.Thread(target=bot.polling).start()
    threading.Thread(target=bot.notif_checker).start()
    
if __name__ == '__main__':
    main()
    