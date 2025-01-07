from multiprocessing import Process
from UltraDict import UltraDict

def child_task():
    # Because `child_task` is now top-level, Python can pickle it
    d2 = UltraDict(name="test_dict", create=False, shared_lock=True)
    d3 = UltraDict(name="other_dict", create=False, shared_lock=True)

    d3["nested"] = {}

    with d2.lock:
        d2["count"] += 1
    with d3.lock:
        d3["count"] += 13
        d3["nested"].update({"testkey": d3["count"]})

def main():
    d = UltraDict(name="test_dict", create=True, shared_lock=True, recurse=False)
    d3 = UltraDict(name="other_dict", create=True, shared_lock=True, recurse=False)
    d["count"] = 0
    d3["count"] = 0

    ref_dict = {"d" : d, "d3" : d3}

    processes = []
    for i in range(50):
        p = Process(target=child_task)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print(f'{ref_dict["d"]["count"]}')
    print(f'{ref_dict["d3"]["count"]}')
    print(f'{ref_dict["d3"]["nested"]}')

if __name__ == "__main__":
    main()
