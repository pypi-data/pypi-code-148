from fastapi import FastAPI

from script_master_ui.routers import notebook, variable, task
from script_master_ui.settings import Settings

app = FastAPI(debug=Settings().debug)

app.include_router(notebook.router)
app.include_router(variable.router)
app.include_router(task.router)
