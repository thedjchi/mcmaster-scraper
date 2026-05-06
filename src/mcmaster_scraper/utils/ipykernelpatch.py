import ipykernel
import os

def patch_ipykernel():
    lib_path = ipykernel.__file__
    if lib_path is None:
        return
    lib_dir = os.path.dirname(lib_path)
    file = os.path.join(lib_dir, "kernelapp.py")

    with open(file, "r") as f:
        content = f.read()

    patched = content.replace(
        "asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())",
        "pass"
    )

    with open(file, "w") as f:
        f.write(patched)