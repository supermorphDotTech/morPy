import threading, multiprocessing, ctypes, time
from multiprocessing import Process, Value
from multiprocessing.managers import BaseManager

# -----------------------------------------------------------------------------
# Manager Process and Thread
# -----------------------------------------------------------------------------

class MorPyDictServer:
    """
    This server holds the real dictionary and services all operations
    (get, set, delete, update, keys, items, etc.). It also holds a shared
    version counter (ctypes-backed via multiprocessing.Value). Communication
    happens via a multiprocessing.Queue (which under the hood uses pipes).
    """
    def __init__(self, ctx=None):
        # Use the provided context (spawn) or the default context.
        if ctx is None:
            ctx = multiprocessing.get_context()
        self.ctx = ctx
        self.cmd_queue = ctx.Queue()
        self.data = {}
        self.version = ctx.Value(ctypes.c_int, 0)  # shared counter for updates
        self.running = True

    def start_manager(self):
        # Run a manager thread that continuously reads commands.
        t = threading.Thread(target=self._manager_loop, daemon=True)
        t.start()

    def _manager_loop(self):
        while self.running:
            try:
                cmd = self.cmd_queue.get(timeout=0.1)
            except Exception:
                continue

            op = cmd.get('op')
            key = cmd.get('key')
            reply_conn = cmd.get('reply_conn')
            if op == 'get':
                result = self.data.get(key, None)
                reply_conn.send(result)
                reply_conn.close()
            elif op == 'set':
                value = cmd.get('value')
                # If value is a dict and not already a MorPyDict, wrap it for nesting.
                if isinstance(value, dict) and not isinstance(value, MorPyDict):
                    value = MorPyDict(value, server=self)
                self.data[key] = value
                with self.version.get_lock():
                    self.version.value += 1
                reply_conn.send(True)
                reply_conn.close()
            elif op == 'del':
                try:
                    del self.data[key]
                    with self.version.get_lock():
                        self.version.value += 1
                    reply_conn.send(True)
                except KeyError:
                    reply_conn.send(KeyError(f"Key {key} not found"))
                reply_conn.close()
            elif op == 'update':
                update_dict = cmd.get('value')
                # For every key in update, wrap dict values as needed.
                for k, v in update_dict.items():
                    if isinstance(v, dict) and not isinstance(v, MorPyDict):
                        update_dict[k] = MorPyDict(v, server=self)
                self.data.update(update_dict)
                with self.version.get_lock():
                    self.version.value += 1
                reply_conn.send(True)
                reply_conn.close()
            elif op == 'keys':
                reply_conn.send(list(self.data.keys()))
                reply_conn.close()
            elif op == 'items':
                reply_conn.send(list(self.data.items()))
                reply_conn.close()
            elif op == 'get_version':
                reply_conn.send(self.version.value)
                reply_conn.close()
            else:
                reply_conn.send(None)
                reply_conn.close()

    def stop(self):
        self.running = False

def _server_process_main(server_obj):
    """Top-level function for the global MorPyDictServer process.
    Simply keeps the process alive while the server is running."""
    while server_obj.running:
        time.sleep(0.1)

# -----------------------------------------------------------------------------
# Manager using BaseManager
# -----------------------------------------------------------------------------

class MorPyDictManager(BaseManager):
    pass

# Register the MorPyDictServer so that it can be shared.
MorPyDictManager.register('MorPyDictServer', MorPyDictServer)

_global_manager = None
_global_server = None

def get_global_server():
    """
    Returns a singleton global server.
    If not already started, it starts a new Manager process (which in turn
    creates a shared MorPyDictServer proxy).
    """
    global _global_manager, _global_server
    if _global_server is None:
        # Use a spawn context and a fixed address and authkey.
        ctx = multiprocessing.get_context('spawn')
        _global_manager = MorPyDictManager(address=('', 50000), authkey=b'mypassword')
        _global_manager.start()
        _global_server = _global_manager.MorPyDictServer(ctx=ctx)
    return _global_server

# -----------------------------------------------------------------------------
# Frontend Proxy: MorPyDict
# -----------------------------------------------------------------------------

class MorPyDict:
    """
    MorPyDict is a dictionary-like proxy that delegates all operations to a central
    manager (a MorPyDictServer). On creation (if no server is provided) it uses a global
    server (created via get_global_server()) that is accessible from any process.

    All front-end operations (get, set, delete, update, keys, items) send a command via a
    multiprocessing.Queue (which uses pipes) to the server. A shared version counter (ctypes
    based) is updated on every write.

    Nesting is supported: if a value is a dict, it is automatically wrapped as a MorPyDict.
    """
    def __init__(self, initial=None, server=None):
        # Use provided server or the global server.
        self.server = server if server is not None else get_global_server()
        # Optionally initialize with data.
        if initial:
            self.update(initial)

    def _send_command(self, cmd):
        # Use a Pipe for the reply.
        parent_conn, child_conn = self.server.ctx.Pipe(duplex=True)
        cmd['reply_conn'] = child_conn
        # Put the command onto the server’s command queue.
        self.server.cmd_queue.put(cmd)
        result = parent_conn.recv()
        parent_conn.close()
        return result

    def __getitem__(self, key):
        result = self._send_command({'op': 'get', 'key': key})
        if result is None:
            raise KeyError(key)
        return result

    def __setitem__(self, key, value):
        self._send_command({'op': 'set', 'key': key, 'value': value})

    def __delitem__(self, key):
        result = self._send_command({'op': 'del', 'key': key})
        if result is not True:
            raise KeyError(key)

    def update(self, other):
        self._send_command({'op': 'update', 'value': other})

    def keys(self):
        return self._send_command({'op': 'keys'})

    def items(self):
        return self._send_command({'op': 'items'})

    def __iter__(self):
        return iter(self.keys())

    def get_version(self):
        return self._send_command({'op': 'get_version'})

    def __contains__(self, key):
        try:
            _ = self.__getitem__(key)
            return True
        except KeyError:
            return False

    def __repr__(self):
        return repr(dict(self.items()))

    # --- Prevent pickling the server so that child processes get the global one ---
    def __getstate__(self):
        state = self.__dict__.copy()
        if 'server' in state:
            del state['server']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        from lib.shm_three import get_global_server
        self.server = get_global_server()
