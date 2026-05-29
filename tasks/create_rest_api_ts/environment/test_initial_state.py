import os
import shutil

def test_encore_binary_available():
    assert shutil.which("encore") is not None, "encore binary not found in PATH."

def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."

def test_git_available():
    assert shutil.which("git") is not None, "git binary not found in PATH."

def test_project_dir_does_not_exist():
    project_dir = "/home/user/helloworld"
    assert not os.path.exists(project_dir), f"Project directory {project_dir} should not exist before the task begins."
