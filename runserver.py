from app import create_app, db
from app.models import Users, SmartPixlParams, FilteredData

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users, 'FilteredData': FilteredData, 'SmartPixlParams': SmartPixlParams}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=app.config["DEBUG"], port=app.config["PORT"])
