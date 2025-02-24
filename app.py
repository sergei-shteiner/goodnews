from flask import Flask, render_template_string
from news import generate_news

app = Flask(__name__)

# Minimalistisches HTML-Template
TEMPLATE = """
<!DOCTYPE html>
<html lang=\"de\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Nachrichtengenerator</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background-color: #f9f9f9; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0;
        }
        .container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            width: 60%;
        }
        h1 { 
            font-size: 1.5rem; 
            color: #333; 
        }
        p { 
            font-size: 1.2rem; 
            color: #555; 
            text-align: left;
            white-space: pre-wrap;
        }
        button {
            margin-top: 1rem;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            border: none;
            border-radius: 5px;
            background-color: #007BFF;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class=\"container\">
        <h1>Gute Nachricht!</h1>
        <p>{{ news }}</p>
        <form method=\"get\">
            <button type=\"submit\">Neue Nachricht generieren</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # Generiert eine neue Nachricht
    news_text = generate_news()
    return render_template_string(TEMPLATE, news=news_text)

if __name__ == '__main__':
    # Startet den Flask-Server
    app.run(host='0.0.0.0', port=80)
