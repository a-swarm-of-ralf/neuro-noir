from typing import Any, Callable
from asyncio import Semaphore, gather

class Runner:
    def __init__(self, dataset: list[dict[str, Any]], function: Callable[[dict[str, Any]], Any]):
        self.dataset = dataset
        self.function = function
        self.results = []

    async def _run_task(self, data: dict[str, Any], semaphore: Semaphore):
        async with semaphore:
            result = await self.function(data)
            self.results.append(result)

    async def _run_tasks(self, semaphore: Semaphore):
        tasks = []
        for data in self.dataset:
            task = self._run_task(data, semaphore)
            tasks.append(task)
        return tasks
       
    async def run(self, concurrency: int = 3) -> list[dict[str, Any]]:
        semaphore = Semaphore(concurrency)
        tasks = await self._run_tasks(semaphore)
        await gather(*tasks)
        return self.results