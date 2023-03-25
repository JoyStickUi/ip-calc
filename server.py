from http.server import  HTTPServer, SimpleHTTPRequestHandler
import ipcalc2
from urllib.parse import unquote
import json

class my_handler(SimpleHTTPRequestHandler):    
    def do_GET(self):
        path = self.path.split('?')
        if path[0] == '/ip':
            ip = None
            netmask = None
            if len(path) == 2:
                address = path[1].split(',')
                if len(address) == 2:
                    if address[0].split('=')[0] == 'ip' and address[1].split('=')[0] == 'netmask':
                        ip = unquote(address[0].split('=')[1])
                        netmask = address[1].split('=')[1]
                elif len(address) == 1:
                    if address[0].split('=')[0] == 'ip':
                        ip = unquote(address[0].split('=')[1])
                if ip != None:
                    self.send_response(200)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    result = ipcalc2.get_matrix(ip, netmask)
                    self.wfile.write(json.dumps(result).encode())
            else:
                self.send_response(403)
                self.wfile.write('Invalid params'.encode())

if __name__ == '__main__':
    server_address = ('172.17.2.45', 80)

    httpd = HTTPServer(server_address, my_handler)

    httpd.serve_forever()
