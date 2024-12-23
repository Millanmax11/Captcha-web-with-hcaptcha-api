from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# Replace this with your hCaptcha secret key
SECRET_KEY = "ES_2f5eea82e1c54d999778434e64ea2c0a"

# hCaptcha verification endpoint
VERIFY_URL = "https://api.hcaptcha.com/siteverify"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Retrieve form data
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        token = request.form.get("h-captcha-response")
        
        # Check for missing captcha token
        if not token:
            return jsonify({"error": "Captcha token missing"}), 400

        # Prepare payload for hCaptcha verification
        data = {
            "secret": SECRET_KEY,
            "response": token
        }

        # Make POST request to hCaptcha
        response = requests.post(VERIFY_URL, data=data)
        response_json = response.json()

        # Check if captcha verification succeeded
        if response_json.get("success"):
            # Display the user's details and success message
            success_message = f"Hello {first_name} {last_name}, captcha verification succeeded!"
            return render_template_string('''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Captcha Success</title>
                    <style>
                        body {
                            background-color: white;
                            font-family: Arial, sans-serif;
                            text-align: center;
                            margin-top: 50px;
                        }
                        h1 {
                            color: green;
                        }
                        a {
                            text-decoration: none;
                            color: blue;
                        }
                    </style>
                </head>
                <body>
                    <h1>{{ message }}</h1>
                    <a href="/">Go Back</a>
                </body>
                </html>
            ''', message=success_message)
        else:
            # Captcha verification failed
            return jsonify({"error": "Captcha verification failed", "details": response_json}), 400

    # Render the form
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>hCaptcha Demo</title>
            <script src="https://js.hcaptcha.com/1/api.js" async defer></script>
            <style>
                body {
                    background-color: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    font-family: Arial, sans-serif;
                }
                .form-container {
                    background-color: white;
                    border: 2px solid blue;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                input {
                    display: block;
                    width: 100%;
                    margin-bottom: 10px;
                    padding: 8px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                input[type="submit"] {
                    background-color: blue;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: darkblue;
                }
            </style>
        </head>
        <body>
            <div class="form-container">
                <form action="/" method="POST">
                    <input type="text" name="first_name" placeholder="First Name" required />
                    <input type="text" name="last_name" placeholder="Last Name" required />
                    <input type="text" name="email" placeholder="Email" required />
                    <input type="password" name="password" placeholder="Password" required />
                    <div class="h-captcha" data-sitekey="bee67218-8dac-41d2-9aaa-dd1a30d46ea4"></div>
                    <br />
                    <input type="submit" value="Submit" />
                </form>
            </div>
        </body>
        </html>
    '''

if __name__ == "__main__":
    app.run(debug=True)
