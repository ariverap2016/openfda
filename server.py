import web
import socketserver #servidor enchufe
# ping para comprobar la identidad, de da la direccion IP de lo q quieras buscar

###
#WEB server
#

PORT=8018

#Handler = http.server.SimpleHTTPRequestHandler #es directamente una referencia a la clase
Handler = web.testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
# httpd es un objeto q se ejecuta para siempre
print("serving at port", PORT)
httpd.serve_forever()
