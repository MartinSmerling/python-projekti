from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import smtplib
from email.message import EmailMessage
import os

PORT = 8095

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'martin.smerling@gmail.com'
SENDER_PASSWORD = 'ycjjfjltatjqqejv'  

class EmailHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            try:
                with open('index.html', 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(file.read())
            except:
                self.send_error(404, "Sivua ei löytynyt")

        elif self.path.endswith(".css"):
            try:
                filepath = self.path.strip("/")
                with open(filepath, 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/css; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(file.read())
            except:
                self.send_error(404, "Tyylitiedostoa ei löytynyt")

        elif self.path == "/second.html":
            try:
                with open("second.html", "rb") as file:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(file.read())
            except:
                self.send_error(404, "Kiitossivua ei löytynyt")
        else:
            self.send_error(404, "Sivua ei löytynyt")

    def do_POST(self):
        if self.path == "/send":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            # Haetaan lomakedata
            sender_email = parsed_data.get('email', [''])[0]
            message_body = parsed_data.get('message', [''])[0]

            # Muodostetaan sähköposti
            msg = EmailMessage()
            msg['Subject'] = 'Martinin uusi yhteydenotto lomakkeelta'
            msg['From'] = SENDER_EMAIL
            msg['To'] = sender_email
            msg['Cc'] = SENDER_EMAIL
            msg.set_content(f"Sähköposti: {sender_email}\n\nViesti:\n{message_body}")


            try:
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
                    smtp.starttls()
                    smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
                    smtp.send_message(msg)
                self.send_response(200)
                self.end_headers()
            except Exception as e:
                print("Virhe sähköpostin lähetyksessä:", e)
                self.send_error(500, "Viestin lähetys epäonnistui.")
        else:
            self.send_error(404, "Reittiä ei löydy.")


def run(server_class=HTTPServer, handler_class=EmailHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Palvelin käynnissä osoitteessa http://localhost:{PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
