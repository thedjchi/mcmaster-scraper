import asyncio
import threading
from asyncio import AbstractEventLoop, wrap_future, CancelledError
from concurrent.futures import Future
from typing import Coroutine, Any, TypeVar

T = TypeVar("T")

_loop: AbstractEventLoop | None = None
_started = threading.Event()
_lock = threading.Lock()


async def run_in_loop_async(func: Coroutine[Any, Any, T]) -> T:
    c_future = _run_in_loop(func)
    a_future = wrap_future(c_future)
    try:
        return await a_future
    except CancelledError:
        c_future.cancel()
        raise


def run_in_loop_sync(func: Coroutine[Any, Any, T]) -> T:
    return _run_in_loop(func).result()


def _run_in_loop(func: Coroutine[Any, Any, T]) -> Future[T]:
    loop = _ensure_loop()
    return asyncio.run_coroutine_threadsafe(func, loop)


def _ensure_loop() -> AbstractEventLoop:
    global _loop
    with _lock:
        if _loop is None:
            t = threading.Thread(target=_run_loop, daemon=True)
            t.start()
            _started.wait()

    assert _loop is not None
    return _loop


def _run_loop():
    global _loop
    loop = asyncio.EventLoop()
    asyncio.set_event_loop(loop)
    _loop = loop
    _started.set()
    loop.run_forever()
