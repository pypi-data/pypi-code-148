from typing import Callable

import click

from projectkit.model.settings import ProjectKitSettings


def cli_project_kit_click_group(project_kit_setting: ProjectKitSettings, cli_group_name: str = "settings") -> Callable:
    @click.group(name=cli_group_name, pass_context=True)
    def project_kit_click_group(ctx):
        ctx.obj = project_kit_setting

    @project_kit_click_group.command(pass_obj=True)
    def init(_project_kit_setting: ProjectKitSettings) -> None:
        _project_kit_setting.dump_new()

    @project_kit_click_group.command(pass_obj=True)
    def update(_project_kit_setting: ProjectKitSettings) -> None:
        _project_kit_setting.update()

    return project_kit_click_group
