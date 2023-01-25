from importlib import import_module
from rekuest.structures.default import get_default_structure_registry
from rekuest.definition.registry import get_default_definition_registry
import inspect
import asyncio
from typing import Type
from arkitekt import Arkitekt
import click





module_path = f"hu"

z = locals()
y = locals()


def import_builder(module_path, function_name) -> Type[Arkitekt]:
    module = import_module(module_path)
    function = getattr(module, function_name)
    return function


async def run_module(identifier, version, entrypoint,  builder: str = "arkitekt.builders.easy"):

    module_path, function_name = builder.rsplit(".", 1)
    builder = import_builder(module_path, function_name)



    app = builder(identifier, version)

    import_module(entrypoint)

    async with app:
        await app.rekuest.run()




   

    
    







