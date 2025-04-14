import atomics
from multiprocessing import shared_memory
import copy

mem = shared_memory.SharedMemory(name='test', create=True, size=1024)
view = atomics.atomicview(buffer=mem.buf[0:4], atype=atomics.BYTES)

desired = b'\xFF' * 4
exp = bytearray(b'\x11' * 4)

with view as v:
    res = atomics.CmpxchgResult(success=False, expected=v.load())
    while not res:
        res = v.cmpxchg_weak(expected=exp, desired=desired)


print(res)
print(v)

mem.unlink()
