"""Worker functions for processing sound generation tasks in parallel."""

import logging

logger = logging.getLogger(__name__)


# def worker(generator: Any, sound: Any) -> None:
#     """Process a single sound generation task."""
#     try:
#         # sound.generate(generator)
#         print(sound)
#         logger.info(f"Generated sound: {sound}")
#     except Exception as e:
#         logger.error(f"Error generating {sound}: {e}")


# def process_queue(generator: Any, worklist: Sequence[Any], workers: int = 16) -> None:
#     """Process a list of sound tasks in parallel using threads."""
#     with ThreadPoolExecutor(max_workers=workers) as executor:
#         futures = [executor.submit(worker, generator, item) for item in worklist]
#         for future in as_completed(futures):
#             # Optionally handle results or exceptions here
#             try:
#                 future.result()
#             except Exception as exc:
#                 logger.error(f"Worker thread failed: {exc}")


# Example usage:
# if __name__ == "__main__":
#     generator = ...  # Your generator object
#     worklist = [...] # List of sound objects
#     process_queue(generator, worklist, workers=4)
# def worker(generator, sound):
#     try:
#         sound.generate(generator)
#     except Exception as e:
#         logger.error(e)
#         # logger.critical(f'{sound} has no ')
#         # raise Exception('ooo')


# def queue(generator, worklist: list, workers=3):
#     from concurrent.futures import ThreadPoolExecutor

#     with ThreadPoolExecutor(max_workers=workers) as executor:
#         for item in worklist:
#             executor.submit(worker, generator, item)


# from concurrent.futures import ThreadPoolExecutor

# ff = ['one', 'two', 'three', 'fish']

# with ThreadPoolExecutor(max_workers=3) as executor:
#     for i in ff:
#         executor.submit(worker, f, Sound(i))
