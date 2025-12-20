You reached the start of the range
Dec 19, 2025, 7:32 PM
Starting Container
[2025-12-20 03:38:44 +0000] [2] [INFO] Booting worker with pid: 2
[2025-12-20 03:38:44 +0000] [2] [ERROR] Exception in worker process
Traceback (most recent call last):
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/arbiter.py", line 608, in spawn_worker
    worker.init_process()
    ~~~~~~~~~~~~~~~~~~~^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/workers/base.py", line 135, in init_process
    self.load_wsgi()
    ~~~~~~~~~~~~~~^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/workers/base.py", line 147, in load_wsgi
    self.wsgi = self.app.wsgi()
                ~~~~~~~~~~~~~^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/app/base.py", line 66, in wsgi
    self.callable = self.load()
                    ~~~~~~~~~^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/app/wsgiapp.py", line 57, in load
    return self.load_wsgiapp()
           ~~~~~~~~~~~~~~~~~^^
[2025-12-20 03:38:44 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2025-12-20 03:38:44 +0000] [1] [INFO] Listening at: http://0.0.0.0:8080 (1)
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/app/wsgiapp.py", line 47, in load_wsgiapp
    return util.import_app(self.app_uri)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/util.py", line 370, in import_app
    mod = importlib.import_module(module)
  File "/mise/installs/python/3.14.2/lib/python3.14/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1398, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 755, in exec_module
  File "<frozen importlib._bootstrap_external>", line 893, in get_code
  File "<frozen importlib._bootstrap_external>", line 823, in source_to_code
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "/app/app.py", line 9
    @app.route("/
               ^
SyntaxError: unterminated string literal (detected at line 9)
[2025-12-20 03:38:44 +0000] [2] [INFO] Worker exiting (pid: 2)
[2025-12-20 03:38:44 +0000] [1] [ERROR] Worker (pid:2) exited with code 3
[2025-12-20 03:38:44 +0000] [1] [ERROR] Shutting down: Master
[2025-12-20 03:38:44 +0000] [1] [ERROR] Reason: Worker failed to boot.
[2025-12-20 03:38:45 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2025-12-20 03:38:45 +0000] [1] [INFO] Listening at: http://0.0.0.0:8080 (1)
[2025-12-20 03:38:45 +0000] [1] [INFO] Using worker: sync
[2025-12-20 03:38:45 +0000] [2] [INFO] Booting worker with pid: 2
           ~~~~~~~~~~~~~~~~~^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/app/wsgiapp.py", line 47, in load_wsgiapp
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/app/base.py", line 66, in wsgi
    return util.import_app(self.app_uri)
[2025-12-20 03:38:45 +0000] [2] [ERROR] Exception in worker process
    self.callable = self.load()
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
Traceback (most recent call last):
                    ~~~~~~~~~^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/util.py", line 370, in import_app
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/arbiter.py", line 608, in spawn_worker
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/app/wsgiapp.py", line 57, in load
    worker.init_process()
    return self.load_wsgiapp()
    ~~~~~~~~~~~~~~~~~~~^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/workers/base.py", line 135, in init_process
    self.load_wsgi()
    ~~~~~~~~~~~~~~^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/workers/base.py", line 147, in load_wsgi
    self.wsgi = self.app.wsgi()
                ~~~~~~~~~~~~~^^
    @app.route("/
               ^
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
SyntaxError: unterminated string literal (detected at line 9)
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
    mod = importlib.import_module(module)
[2025-12-20 03:38:45 +0000] [2] [INFO] Worker exiting (pid: 2)
  File "<frozen importlib._bootstrap_external>", line 755, in exec_module
  File "/mise/installs/python/3.14.2/lib/python3.14/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap_external>", line 893, in get_code
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap_external>", line 823, in source_to_code
  File "<frozen importlib._bootstrap>", line 1398, in _gcd_import
  File "<frozen importlib._bootstrap>", line 491, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "/app/app.py", line 9
[2025-12-20 03:38:45 +0000] [1] [ERROR] Worker (pid:2) exited with code 3
[2025-12-20 03:38:45 +0000] [1] [ERROR] Shutting down: Master
[2025-12-20 03:38:45 +0000] [1] [ERROR] Reason: Worker failed to boot.
Stopping Container
[2025-12-20 03:38:47 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2025-12-20 03:38:47 +0000] [1] [INFO] Listening at: http://0.0.0.0:8080 (1)
[2025-12-20 03:38:47 +0000] [1] [INFO] Using worker: sync
[2025-12-20 03:38:47 +0000] [2] [INFO] Booting worker with pid: 2
[2025-12-20 03:38:47 +0000] [2] [ERROR] Exception in worker process
Traceback (most recent call last):
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/arbiter.py", line 608, in spawn_worker
    worker.init_process()
    ~~~~~~~~~~~~~~~~~~~^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/workers/base.py", line 135, in init_process
    self.load_wsgi()
    ~~~~~~~~~~~~~~^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/workers/base.py", line 147, in load_wsgi
    self.wsgi = self.app.wsgi()
                ~~~~~~~~~~~~~^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/app/base.py", line 66, in wsgi
    self.callable = self.load()
                    ~~~~~~~~~^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/app/wsgiapp.py", line 57, in load
    return self.load_wsgiapp()
           ~~~~~~~~~~~~~~~~~^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/app/wsgiapp.py", line 47, in load_wsgiapp
    return util.import_app(self.app_uri)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  File "/app/.venv/lib/python3.14/site-packages/gunicorn/util.py", line 370, in import_app
    mod = importlib.import_module(module)
  File "/mise/installs/python/3.14.2/lib/python3.14/importlib/__init__.py", line 88, in import_module
