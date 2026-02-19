from setuptools import setup

setup(
    name="mcp-link-library",
    version="3.3.0",
    py_modules=["mcp", "verify"],
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    entry_points={
        "console_scripts": [
            "mcp=mcp:main",
            "mcp-lib-verify=verify:verify_library",
        ],
    },
)
