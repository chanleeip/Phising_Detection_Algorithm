from files import main
import typer
import os
app=typer.Typer()

@app.command(help="This cli is used for analyzing batch of emails/email. ")
def run_file(path:str=typer.Option('', "--path", "-p", help="add the path here")):
    if path:
        print(main.run_script(path))

if __name__ == "__main__":
    app()



