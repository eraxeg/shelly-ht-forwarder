import configparser
import http.server
import urllib.request
import logging
import socket

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class RequestHandler(http.server.BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        self.target_address = kwargs.pop('target_address', 'odroid')
        super().__init__(*args, **kwargs)

    def do_GET(self):
        logging.info(f"Incoming GET request: {self.path}")
        # Extract query string from the request
        query_string = self.path.split('?', 1)[-1]
        qs_dict = urllib.parse.parse_qs(query_string)
        instance = qs_dict.pop('instance')[0]
        try:
            job_name = list(qs_dict.keys())[0]
            value = list(qs_dict.values())[0][0]
        except Exception as e:
            logging.error(e)

        body = f'{job_name}{{instance="{instance}"}} {value}\n'
        url_to_forward = f'http://{self.target_address}/metrics/job/{job_name}'
        logging.info(f"Posting {body} to {url_to_forward}")
        response = urllib.request.urlopen(url_to_forward, data=body.encode())
        logging.info(f"Response {response}")
        self.send_response(response.code)
        self.send_header("Content-type", response.headers.get_content_type())
        self.end_headers()
        self.wfile.write(response.read())

def check_connection(hostname):
    try:
        # Try to resolve hostname
        ip_address = socket.gethostbyname(hostname)
        return True
    except Exception as e:
        logging.error(f"Error checking connection to {hostname}: {e}")
        return False

def read_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

def run_server(host='0.0.0.0', config=None):
    port = config.getint('server', 'port', fallback=9093)
    hostname = config.get('target', 'hostname', fallback='odroid')
    target_port = config.getint('target', 'port', fallback=9092)

    if check_connection(hostname):  # Replace "odroid" with your hostname
        logging.info(f"Connection to host {hostname} is successful!")
    else:
        logging.error(f"Unable to connect to host {hostname}!")
        return

    server_address = (host, port)
    target_address = f'{hostname}:{target_port}'
    httpd = http.server.HTTPServer(server_address, lambda *args, **kwargs: RequestHandler(target_address=target_address, *args, **kwargs))
    logging.info(f"Starting server on {host}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    parsed_config = read_config('config.ini')
    run_server(config=parsed_config)

