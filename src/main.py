from app import App
from handlers.app_events_handlers import AppEventsHandlers


if __name__ == "__main__":
    app = App()
    handlers = AppEventsHandlers(app)
    app.run()
