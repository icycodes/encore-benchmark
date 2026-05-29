import os
import shutil

def test_encore_binary_available():
    assert shutil.which("encore") is not None, "encore binary not found in PATH."

def test_project_directory_exists():
    project_dir = "/home/user/myproject"
    assert os.path.isdir(project_dir), f"Project directory {project_dir} does not exist."