from typer import Typer

app = Typer()

@app.command('createuser')
def create_user():
    pass

@app.command('createsuperuser')
def create_superuser():
    pass

@app.command('makemigrations')
def make_migrations():
    pass

@app.command('migrate')
def migrate():
    pass

if __name__ == '__main__':
    app()