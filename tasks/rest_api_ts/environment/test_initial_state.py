import os
import shutil
import pytest

def test_encore_cli_available():
    assert shutil.which("encore") is not None, "encore CLI not found in PATH."

def test_git_available():
    assert shutil.which("git") is not None, "git CLI not found in PATH."

def test_node_available():
    assert shutil.which("node") is not None, "Node.js not found in PATH."

def test_curl_available():
    assert shutil.which("curl") is not None, "curl not found in PATH."
