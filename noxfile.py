import nox

@nox.session(python=False)
def requirements(session):
    session.run("pip", "install", "-r", "requirements.txt")

@nox.session(python=False)
def formatting(session):
    session.run("pip", "install", "-r", "dev-requirements.txt")
    session.run("python3", "-m", "black", "verox")
    session.run("python3", "-m", "isort", "verox")
    session.run("python3", "-m", "codespell_lib", "verox", "-w")