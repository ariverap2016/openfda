import http.server
import http.client
import json
#import socketserver
class OpenFDAClient():
    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"
    def get_event(self, url, limit):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + url +limit)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        data1 = r1.read()
        data=data1.decode("utf8")
        event=data
        return event
class OpenFDAParser():
    def get_drugs_from_events(self, events):
        drugs = []
        for event in events:
            drugs += [event['patient']['drug'][0]['medicinalproduct']]
        return drugs
    def get_search_companynumb(self, events):
        companynumb = []
        for event in events:
            companynumb += [event['companynumb']]
        return companynumb
    def get_patientsex(self, events):
        patientsex= []
        for event in events:
            patientsex += [event['patient']['patientsex']]
        return patientsex
class OpenFDAHTML():
    def get_main_page(self):
        html='''
        <html>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1>OpenFDA Client</h1>
                <form method="get" action="listDrugs">
                    Drug List:<input type="submit" value="Drug List: Send to OpenFDA">
                    Limit:<input name="number" size='2' type="text">
                </form>
                <form method="get" action="searchDrug">
                    Drug Search:<input name="drug" type="text">
                    <input type="submit" value="Drug Search: Send to OpenFDA">
                </form>
                <form method="get" action="listCompanies">
                    Companies List:<input type="submit" value="Companies List: Send to OpenFDA">
                    Limit:<input name="number" size='2' type="text">
                </form>
                <form method="get" action="searchCompany">
                    Company Search:<input name="company" type="text">
                    <input type="submit" value="Company Search: Send to OpenFDA">
                </form>
                <form method="get" action="listGender">
                    Patientsex List:<input type="submit" value="Patientsex List: Send to OpenFDA">
                    Limit:<input name="number" size='2' type="text">
                </form>
            </body>
        </html>
        '''
        return html
    def get_list_html(self, drugs):
        drugs_html="""
        <html>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <ol>
                """
        for drug in drugs:
            drugs_html += "<li>" + drug + "</li>\n"
        drugs_html += """
                </ol>
            </body>
        </html>
        """
        return drugs_html
    def get_html_not_exists_resource(self):
        html='''
        <html>
            <head>
                <title>Error OpenFDA Cool App</title>
            </head>
            <body>
                <h1>Error</h1>
                <p>Error not found </p>
            </body>
        </html>
        '''
        return html
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def get_html_answer(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
    def do_GET(self):
        client = OpenFDAClient()
        parser=OpenFDAParser()
        HTML=OpenFDAHTML()
        html=HTML.get_main_page()
        main_page = False
        listDrug = False
        searchDrug = False
        listCompanies = False
        searchCompany = False
        listGender = False
        if  self.path=='/':
            main_page=True
        elif '/listDrugs' in self.path:
            listDrug = True
        elif '/searchDrug' in self.path:
            searchDrug = True
        elif '/listCompanies' in self.path:
            listCompanies = True
        elif '/searchCompany' in self.path:
            searchCompany = True
        elif '/listGender' in self.path:
            listGender = True
        if main_page:
            self.get_html_answer()
            self.wfile.write(bytes(html, "utf8"))
        elif listDrug:
            self.get_html_answer()
            url = "?limit="
            limit = self.path.split('=')[1]
            event = client.get_event(url, limit)
            events=json.loads(event)
            events=events["results"]
            events= parser.get_drugs_from_events(events)
            html=HTML.get_list_html(events)
            self.wfile.write(bytes(html, "utf8"))
        elif searchDrug:
            self.get_html_answer()
            url = '?search=patient.drug.medicinalproduct:'+ self.path.split('=')[1]
            limit = '&limit=10'
            event = client.get_event(url, limit)
            events = json.loads(event)
            events=events["results"]
            events=parser.get_search_companynumb(events)
            html=HTML.get_list_html(events)
            self.wfile.write(bytes(html, "utf8"))
        elif listCompanies:
            self.get_html_answer()
            url = "?limit="
            limit = self.path.split('=')[1]
            event = client.get_event(url, limit)
            events = json.loads(event)
            events = events["results"]
            events = parser.get_search_companynumb(events)
            html = HTML.get_list_html(events)
            self.wfile.write(bytes(html, "utf8"))
        elif searchCompany:
            self.get_html_answer()
            url = '?search=' + self.path.split('=')[1]
            limit = '&limit=10'
            event = client.get_event(url, limit)
            events = json.loads(event)
            events = events["results"]
            events= parser.get_drugs_from_events(events)
            html = HTML.get_list_html(events)
            self.wfile.write(bytes(html, "utf8"))
        elif listGender:
            self.get_html_answer()
            url = "?limit="
            limit = self.path.split('=')[1]
            event = client.get_event(url, limit)
            events=json.loads(event)
            events=events["results"]
            events= parser.get_patientsex(events)
            html=HTML.get_list_html(events)
            self.wfile.write(bytes(html, "utf8"))
        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
            html=HTML.get_html_not_exists_resource()
            self.wfile.write(bytes(html, "utf8"))
        return
