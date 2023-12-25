from files import main
import typer
import os
app=typer.Typer()

@app.command(help="This cli is used for analyzing batch of emails/email. ")
def run_file(path:str=typer.Option('', "--path", "-p", help="add the path here")):
    if path:
        print("Report\n\n\n")
        details,score=main.run_script(path)
        print(details)
        print("\n\n\n")
        if 0 <= score <= 20:
            risk_level = "High Risk - Strongly indicates phishing. Avoid interaction and report immediately."
        elif 21 <= score <= 40:
            risk_level = "Moderate Risk - Multiple worrisome signs. Validate the email's authenticity and be cautious with interactions."
        elif 41 <= score <= 70:
            risk_level = "Low Risk - Some questionable elements detected. Proceed with caution."
        elif 71 <=score <= 100:
            risk_level = "Highly Safe"
        print(f"Risk Level: {risk_level}")

if __name__ == "__main__":
    app()



