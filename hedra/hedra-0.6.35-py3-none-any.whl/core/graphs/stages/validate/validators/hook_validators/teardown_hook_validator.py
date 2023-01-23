from hedra.core.graphs.hooks.hook_types.hook_type import HookType
from hedra.core.graphs.events.event import Event
from hedra.core.graphs.hooks.registry.registry_types import TeardownHook
from hedra.core.graphs.stages.validate.exceptions import HookValidationError
from .base_hook_validator import BaseHookVaidator


class TeardownHookValidator(BaseHookVaidator):

    def __init__(self, metadata_string: str) -> None:
        super(
            TeardownHookValidator,
            self
        ).__init__(metadata_string)

    async def validate(self, hook: TeardownHook):

        try:

            call = hook._call
            if isinstance(hook, Event):
                call = hook.target._call

            await self.logger.filesystem.aio['hedra.core'].debug(f'{self.metadata_string} - Validating {hook.hook_type.name.capitalize()} Hook - {hook.name}:{hook.hook_id}:{hook.hook_id}')

            assert hook.hook_type is HookType.TEARDOWN, f"Hook type mismatch - hook {hook.name}:{hook.hook_id} is a {hook.hook_type.name} hook, but Hedra expected a {HookType.TEARDOWN.name} hook."
            assert hook.shortname in hook.name, f"Shortname {hook.shortname} must be contained in full Hook name {hook.name}:{hook.hook_id} for @teardown hook {hook.name}:{hook.hook_id}."
            assert hook.shortname in hook.name, "Shortname must be contained in full Hook name."
            assert call is not None, f"Method is not not found on stage or was not supplied to @teardown hook - {hook.name}:{hook.hook_id}"
            assert call.__code__.co_argcount == 1, f"Too many args. - @teardown hook {hook.name}:{hook.hook_id} requires no additional args."
            assert 'self' in call.__code__.co_varnames


            await self.logger.filesystem.aio['hedra.core'].debug(f'{self.metadata_string} - Validated {hook.hook_type.name.capitalize()} Hook - {hook.name}:{hook.hook_id}:{hook.hook_id}')


        except AssertionError as hook_validation_error:
                raise HookValidationError(hook.stage_instance, str(hook_validation_error))