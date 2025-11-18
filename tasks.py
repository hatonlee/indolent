from invoke import task

@task
def start(ctx):
    ctx.run("python src/app.py", pty=False)

@task
def test(ctx):
    ctx.run("pytest src/tests", pty=False)

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest", pty=False)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=False)

