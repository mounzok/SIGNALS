from flask import Flask, redirect, request, render_template_string
import os

app = Flask(__name__)

CLIENT_ID = os.getenv("DERIV_CLIENT_ID", "votre_client_id_ici")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://ton-app.onrender.com/oauth-callback")

template_page = """
<!DOCTYPE html>
<html>
<head><title>Connexion Deriv</title></head>
<body>
  {% if token %}
    <h2>Token OAuth2 récupéré :</h2>
    <p><code>{{ token }}</code></p>
    <p>Copiez ce token pour l'utiliser dans votre app Streamlit.</p>
  {% else %}
    <h2>Erreur : Aucun token trouvé</h2>
  {% endif %}
</body>
</html>
"""

@app.route("/")
def home():
    auth_url = f"https://oauth.deriv.com/oauth2/authorize?app_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return redirect(auth_url)

@app.route("/oauth-callback")
def oauth_callback():
    token = request.args.get("token")
    return render_template_string(template_page, token=token)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
