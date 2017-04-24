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
import http.client
import json
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
                <style>
                form {text-align: center; }
                </style>
            </head>
            <body>
                <h1 align='center'>OpenFDA Client</h1>
                <form method="get" action="listDrugs">
                    Drug List <BR> <input type="submit" value="Drug List: Send to OpenFDA">
                    <BR> Limit:<input name="number" size='2' type="text">
                </form>
                <form method="get" action="searchDrug">
                    <BR> Drug Search <BR> <input name="drug" type="text">
                    <BR> <input type="submit" value="Drug Search: Send to OpenFDA">
                </form>
                <form method="get" action="listCompanies">
                    <BR> Companies List <BR> <input type="submit" value="Companies List: Send to OpenFDA">
                    <BR> Limit:<input name="number" size='2' type="text">
                </form>
                <form method="get" action="searchCompany">
                    <BR> Company Search <BR> <input name="company" type="text">
                    <BR> <input type="submit" value="Company Search: Send to OpenFDA">
                </form>
                <form method="get" action="listGender">
                    <BR> Patientsex List <BR> <input type="submit" value="Patientsex List: Send to OpenFDA">
                    <BR> Limit:<input name="number" size='2' type="text">
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
    def get_html_secret(self):
        html='''
        <html>
            <head>
                <title>Unauthorized</title>
            </head>
            <body>
                <h1>Error</h1>
                <p> WWW-Authenticate de basic Realm </p>
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
        secret = False
        redirect = False
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
        elif '/secret' in self.path:
            secret = True
        elif '/redirect' in self.path:
            redirect = True
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
        elif secret:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
            self.end_headers()
        elif redirect:
            self.send_response(302)
            self.send_header('Location', 'http://localhost:8000/')
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
            html=HTML.get_html_not_exists_resource()
            self.wfile.write(bytes(html, "utf8"))
        return
