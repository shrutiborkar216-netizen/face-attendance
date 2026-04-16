import csv

@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.form.get('name')
        roll = request.form.get('roll')
        photo = request.files.get('photo')

        if not name or not roll or not photo:
            return "❌ Please fill all fields and upload photo"

        name = name.strip().replace(" ", "")
        roll = roll.strip()

        filename = f"{name}_{roll}_{int(time.time())}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        photo.save(filepath)

        # ✅ SAVE DATA TO students.csv
        file_exists = os.path.isfile('students.csv')

        with open('students.csv', 'a', newline='') as file:
            writer = csv.writer(file)

            # Write header if file not exists
            if not file_exists:
                writer.writerow(["Name", "Roll", "Image"])

            writer.writerow([name, roll, filepath])

        return f"✅ {name} Registered Successfully!"

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ✅ RUN APP (DEPLOYMENT READY)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
