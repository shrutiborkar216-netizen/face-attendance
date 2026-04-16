from flask import Flask, render_template, request
import os
import time

app = Flask(__name__)

# ✅ Upload folder (correct for web)
UPLOAD_FOLDER = os.path.join('static', 'images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# ✅ HOME ROUTE
@app.route('/')
def home():
    return render_template('register.html')


# ✅ REGISTER ROUTE (MOBILE SAFE)
@app.route('/register', methods=['POST'])
def register():
    try:
        # ✅ Safe data fetching
        name = request.form.get('name')
        roll = request.form.get('roll')
        photo = request.files.get('photo')

        # ✅ Validation (important for mobile)
        if not name or not roll or not photo:
            return "❌ Please fill all fields and upload photo"

        # Clean input
        name = name.strip().replace(" ", "")
        roll = roll.strip()

        # Create filename
        filename = f"{name}_{roll}_{int(time.time())}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save image
        photo.save(filepath)

        return f"""
        <h2>✅ {name} Registered Successfully!</h2>
        <a href="/">Go Back</a>
        """

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ✅ RUN APP (DEPLOYMENT READY)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)