import nox

SCRIPT_PATHS = [
    "verox",
    "examples"
]

@nox.session(python=False)
def requirements(session):
    session.run("pip", "install", "-Ur", "requirements.txt")
    session.run("pip", "install", "-Ur", "dev-requirements.txt")

@nox.session(python=False)
def formatting(session):
    session.run("python3", "-m", "black", *SCRIPT_PATHS)
    session.run("python3", "-m", "isort", *SCRIPT_PATHS)
    session.run("python3", "-m", "codespell_lib", "verox", "-w")