from invoke.tasks import task


@task
def start(ctx):
    ctx.run("python src/app.py")


@task
def test(ctx):
    ctx.run("pytest src/tests")


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest")


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")


@task()
def format(ctx):
    ctx.run("isort .")
    ctx.run("black .")


@task()
def lint(ctx):
    ctx.run("pylint src")
