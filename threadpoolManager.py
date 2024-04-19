from concurrent.futures import ThreadPoolExecutor, as_completed

# This is the threadpool [MANAGER class]
class ThreadPoolManager:
    def __init__(self, app, max_workers=10):
        self.app = app
        self.max_workers = max_workers

    # The result is not interesting cuase it is performed every 45 seconds
    # And saved in the history. It will be extremely hard to understand 
    # the logs of this func
    def execute_tasks(self, task_func, items):
        def task_wrapper(item_id):
            with self.app.app_context():
                return task_func(item_id)

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for item in items:
                if item and item.id:
                    executor.submit(task_wrapper, item.id)

