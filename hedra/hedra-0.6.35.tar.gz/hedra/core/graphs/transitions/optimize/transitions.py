import asyncio
from sys import path
import traceback
import uuid
from hedra.core.graphs.stages.base.stage import Stage
from hedra.core.graphs.stages.types.stage_states import StageStates
from hedra.core.graphs.stages.types.stage_types import StageTypes
from hedra.core.graphs.transitions.exceptions import (
    StageExecutionError,
    StageTimeoutError
)
from hedra.logging import HedraLogger


async def optimize_transition(current_stage: Stage, next_stage: Stage):

    logger = HedraLogger()
    logger.initialize()

    await logger.spinner.system.debug(f'{current_stage.metadata_string} - Executing transition from {current_stage.name} to {next_stage.name}')
    await logger.filesystem.aio['hedra.core'].debug(f'{current_stage.metadata_string} - Executing transition from {current_stage.name} to {next_stage.name}')

    execute_stages = current_stage.context.stages.get(StageTypes.EXECUTE).items()
    optimize_stages = current_stage.context.stages.get(StageTypes.OPTIMIZE).items()
    paths = current_stage.context.paths.get(current_stage.name)

    visited = current_stage.context.visited

    execute_stages = {
        stage_name: stage for stage_name, stage in execute_stages if stage_name in paths and stage_name not in visited
    }

    optimize_stages_in_path = {}
    for stage_name, stage in optimize_stages:
        if stage_name in paths and stage_name != current_stage.name and stage_name not in visited:
            optimize_stages_in_path[stage_name] = stage.context.paths.get(stage_name)

    optimization_candidates = {}

    valid_states = [
        StageStates.INITIALIZED,
        StageStates.SETUP,
    ]

    for stage_name, stage in execute_stages.items():
        if stage_name in paths and stage.state in valid_states:

            if len(optimize_stages_in_path) > 0:
                for path in optimize_stages_in_path.values():
                    if stage_name not in path:
                        stage.state = StageStates.OPTIMIZING
                        optimization_candidates[stage_name] = stage

            else:
                stage.state = StageStates.OPTIMIZING
                optimization_candidates[stage_name] = stage

    next_stage.context = current_stage.context

    if len(optimization_candidates) > 0:
   
        current_stage.generation_optimization_candidates = len(optimization_candidates)

        if current_stage.timeout:
            optimization_results = await asyncio.wait_for(current_stage.run(optimization_candidates), timeout=current_stage.timeout)

        else:
            optimization_results = await current_stage.run(optimization_candidates)

        next_stage.context.optimized_params = optimization_results

        for optimization_candidate in optimization_candidates.values():
            optimization_candidate.state = StageStates.OPTIMIZED

    next_stage.state = StageStates.OPTIMIZED

    await logger.spinner.system.debug(f'{current_stage.metadata_string} - Completed transition from {current_stage.name} to {next_stage.name}')
    await logger.filesystem.aio['hedra.core'].debug(f'{current_stage.metadata_string} - Completed transition from {current_stage.name} to {next_stage.name}')



async def optimize_to_execute_transition(current_stage: Stage, next_stage: Stage):

    try:

        await optimize_transition(current_stage, next_stage)
            
    except asyncio.TimeoutError:
        return StageTimeoutError(current_stage), StageTypes.ERROR
    
    except Exception as stage_execution_error:
        return StageExecutionError(current_stage, next_stage, str(stage_execution_error)), StageTypes.ERROR

    
    current_stage = None

    return None, StageTypes.EXECUTE


async def optimize_to_checkpoint_transition(current_stage: Stage, next_stage: Stage):

    try:

        next_stage.previous_stage = current_stage.name

        await optimize_transition(current_stage, next_stage)

        next_stage.data = next_stage.context.optimized_params
            
    except asyncio.TimeoutError:
        return StageTimeoutError(current_stage), StageTypes.ERROR
    
    except Exception as stage_execution_error:
        return StageExecutionError(current_stage, next_stage, str(stage_execution_error)), StageTypes.ERROR

    current_stage = None

    return None, StageTypes.CHECKPOINT


async def optimize_to_wait_transition(current_stage: Stage, next_stage: Stage):

    try:

        next_stage.previous_stage = current_stage.name
        
        await optimize_transition(current_stage, next_stage)

        next_stage.data = next_stage.context.optimized_params
            
    except asyncio.TimeoutError:
        return StageTimeoutError(current_stage), StageTypes.ERROR
    
    except Exception as stage_execution_error:
        return StageExecutionError(current_stage, next_stage, str(stage_execution_error)), StageTypes.ERROR

    current_stage = None

    return None, StageTypes.WAIT
