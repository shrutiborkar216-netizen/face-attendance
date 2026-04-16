from flask import Flask, render_template, request
import os
import time

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ HOME ROUTE (IMPORTANT)
@app.route('/')
def home():
    return render_template('register.html')


# ✅ REGISTER ROUTE
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    roll = request.form['roll']
    photo = request.files['photo']

    # Clean input
    name = name.strip().replace(" ", "")
    roll = roll.strip()

    if photo:
        # ✅ Auto filename with timestamp
        filename = f"{name}_{roll}_{int(time.time())}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        photo.save(filepath)

        return f"""
        <h2>✅ {name} Registered Successfully!</h2>
        <a href="/">Go Back</a>
        """

    return "❌ No photo uploaded"


# ✅ RUN APP
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)