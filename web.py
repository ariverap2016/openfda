
#<Drugs OpenFDA>
#    Copyright (C) <2017>  <Alba>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import http.server
import http.client #import http.client en python3 pero no se porq no me funciona con eso
import json
import socketserver

'''
para convertir una lista en string
a=['1','2']
'.'join(a)
y sale '1,2'
'''

# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"
    #se mete aqui para q quede como en cajas, ya q esto es especifico de la clase

    def get_event(self):
        ###
        #GET EVENT
        ###

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL) #http.client es la biblioteca y dentro hay una clase HTTPSConnection q permite establecer conexion
        #self.OPENFDA_API_URL se pone el self pq sino no lo encuentra, lo busca dentro de la def y en el ambito global, pero no dentro de la clase y fuera de la funcion
        #el self hace referencia al propio objeto
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10") #el metodo hace una peticion tipo get y lo de al lado es lo que sigue la peticion
        #invocas la funcion
        r1 = conn.getresponse() #realizar peticion y almacenar respuesta
        #recibes la respuesta
        print(r1.status, r1.reason) #si la peticion va bien el status te devuelve 200 y la reason O
        #200 OK
        data1 = r1.read()  # This will return entire content.#lo leemos como si fuera un fichero
        data=data1.decode("utf8") #los bytes los pasa a str
        #utf8=como se codifican los caracteres a codigo binario
        #event=json.loads(data)
        event=data
        return event

    def get_drug(self):

        url=self.path
        url_list=url.split('=')
        drug=url_list[1]

        #self.path.split('=')[1]

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct:' + drug + '&limit=10')
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        data1 = r1.read()
        data=data1.decode("utf8") #los bytes los pasa a str
        #utf8=como se codifican los caracteres a codigo binario
        #event=json.loads(data)
        drug=data
        return drug

    def get_companynumb(self):

        url=self.path
        url_list=url.split('=')
        companynumb=url_list[1]

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=' + companynumb + '&limit=10')
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        data1 = r1.read()
        data=data1.decode("utf8")
        companynumb=data
        return companynumb

    def get_main_page(self):
        # Send message back to client
        #message = "Hello world! " + self.path
        html='''
        <html>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1>OpenFDA Client</h1>
                <form method="get" action="receive">
                    <input type="submit" value="Drug List: Enviar a OpenFDA">
                </form>
                <form method="get" action="search">
                    <input name="drug" type="text">
                    <input type="submit" value="Drug Search LYRICA: Enviar a OenFDA">
                </form>
                <form method="get" action="receive_companynumb">
                    <input type="submit" value="Companynumb List: Enviar a OpenFDA">
                </form>
                <form method="get" action="search_companynumb">
                    <input name="companynumb" type="text">
                    <input type="submit" value="Companynumb Search: Enviar a OenFDA">
                </form>
            </body>
        </html>
        '''
        return html

    def get_drugs_from_events(self, events):
        drugs = []
        for event in events:
            drugs += [event['patient']['drug'][0]['medicinalproduct']]
        return drugs

    def get_list_html(self, drugs):
        drugs_html="""
        <html>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <ul>
                """

        for drug in drugs:
            drugs_html += "<li>" + drug + "</li>\n"

        drugs_html += """
                </ul>
            </body>
        </html>
        """

        return drugs_html

    def get_search_companynumb(self, events):
        companynumb = []
        for event in events:
            companynumb += [event['companynumb']]
        return companynumb

    # GET
    def do_GET(self):

        #Todo lo anterior alternativa para el if self.path=='/'

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        html=self.get_main_page()

        main_page = False
        is_event = False
        is_search = False
        is_companynumb = False
        is_medicinalproduct = False
        if self.path =='/':
            #self.path es la ruta de la barra
            main_page = True
        elif self.path =='/receive' or self.path=='/receive?':
            is_event = True
        elif '/search?' in self.path:
            is_search = True
        elif self.path == '/receive_companynumb':
            is_companynumb = True
        elif '/search_companynumb?' in self.path:
            is_medicinalproduct = True
        #Todo lo anterior se puede evitar con el if self.path.write(bytes(html,"utf8")) y el else


        if main_page:
            self.wfile.write(bytes(html, "utf8"))
        elif is_event:
            event = self.get_event()
            events=json.loads(event)
                #for i in event:
                #    return(event["results"][i]['patient']['drug'][0]['medicinalproduct'])
            events=events["results"]
            drugs=self.get_drugs_from_events(events)
            html=self.get_list_html(drugs)

            #events_html=[]

            #for event in events:
            #    print(event["patient"]["drug"][0]["medicinalproduct"])
            #    events_html += [event["patient"]["drug"][0]["medicinalproduct"]]
            #    events_delistaastr=",".join(events_html)

            #html_events=self.html_events()
            self.wfile.write(bytes(html, "utf8"))
        elif is_search:
            drug = self.get_drug()
            events = json.loads(drug)
            events=events["results"]
            search=self.get_search_companynumb(events)
            html=self.get_list_html(search)
            self.wfile.write(bytes(html, "utf8"))

        elif is_companynumb:
            event = self.get_event()
            events = json.loads(event)
            events = events["results"]
            companynumb = self.get_search_companynumb(events)
            html = self.get_list_html(companynumb)
            self.wfile.write(bytes(html, "utf8"))

        elif is_medicinalproduct:
            event = self.get_companynumb()
            events = json.loads(event)
            events = events["results"]
            medicinalproduct = self.get_drugs_from_events(events)
            html = self.get_list_html(medicinalproduct)
            self.wfile.write(bytes(html, "utf8"))

        return




    def html_events(self,events_html):
        html_events='''
        <html>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <ul>
                    <li>Drug10<li>
                    #li=list item
                    ...
                    </li>DRug</li>
                </ul>
                </body>
            </html>
            '''
        return html_events
        #<html> etiqueta de apertura
        #</html> etiqueta de cierre

        #<input type="text"> sirve para poner la barra de busqueda
        #html form action=tutorial
        #el metodo get hace q se te vaya pegando todo a la url
        # Write content as utf-8 data
