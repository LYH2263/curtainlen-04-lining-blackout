import os
import tempfile

os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="curtainlen-test-")
