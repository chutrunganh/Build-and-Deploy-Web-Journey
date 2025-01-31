from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port='5000') # Run the app in debug mode (every time you change the file, the server will restart)

