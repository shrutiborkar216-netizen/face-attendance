from flask import Flask, render_template, request
import os
import time
import csv

app = Flask(__name__)

# ✅ Upload folder
UPLOAD_FOLDER = os.path.join('static', 'images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# ✅ HOME ROUTE
@app.route('/')
def home():
    return render_template('register.html')


# ✅ REGISTER ROUTE (NOW SAVES DATA)
@app.route('/register', methods=['POST'])
def register():
    try:
        # Get data safely
        name = request.form.get('name')
        roll = request.form.get('roll')
        photo = request.files.get('photo')

        # Validation
        if not name or not roll or not photo:
            return "❌ Please fill all fields and upload photo"

        # Clean input
        name = name.strip().replace(" ", "")
        roll = roll.strip()

        # Save image
        filename = f"{name}_{roll}_{int(time.time())}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(filepath)

        # ✅ SAVE TO students.csv
        file_exists = os.path.isfile('students.csv')

        with open('students.csv', 'a', newline='') as file:
            writer = csv.writer(file)

            # Write header only once
            if not file_exists:
                writer.writerow(["Name", "Roll", "Image"])

            writer.writerow([name, roll, filepath])

        return f"""
        <h2>✅ {name} Registered Successfully!</h2>
        <a href="/">Go Back</a>
        """

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ✅ RUN APP
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# ✅ RUN APP (DEPLOYMENT READY)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
