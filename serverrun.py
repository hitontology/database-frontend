from os import getenv
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from app import app

application = DispatcherMiddleware(
    app, {"/database-frontend": app}
)

#if __name__ == "__main__":
if __name__ != "asdfasdf__main__":
    run_simple(
        "0.0.0.0",
        int(getenv("HITO_DATABASE_FRONTEND_PORT", "5000")),
        application,
        use_debugger=False,
        threaded=True,
    )

