import asyncio

def start_job(coro, registry):
    task = asyncio.create_task(coro)
    registry.add(task)
    task.add_done_callback(registry.discard)
    return task
