#! /usr/bin/python
# coding: utf-8

from mechanize import Browser
from BeautifulSoup import BeautifulSoup

from data import AIRPORTS_LIST

    
class Airport(object):

    def __init__(self, code):
        if str(code) not in AIRPORTS_LIST:
            raise Exception("Invalid Airport Code")
        self.code = code
        self.br = Browser()
        self.br.set_handle_robots(False)

    def _get_flights_data(self):
        self.br.open("http://www.infraero.gov.br/voos/index.aspx")
        self.br.select_form(name="form1")
        self.br["aero_companias_aeroportos"] = [self.code,]
        response = self.br.submit()
        return response.read()

    def _parse_flights_data(self, data):
        soup = BeautifulSoup(data)
        table = soup.find("table", { "id" : "grd_voos" })
        flights_list = []
        for row in table.findChildren('tr')[1:]:
            col = row.findChildren('td')
            get_span = lambda col,i: col[i].findChildren('span')[0].string
            try:
                flight_info = {
                'airline': get_span(col,2),
                'flight': get_span(col,3),
                'origin': get_span(col,4),
                'date': get_span(col,5),
                'scheduled': get_span(col,6),
                'confirmed': get_span(col,7),
                'scales': get_span(col,8),
                'status': get_span(col,9),
                }
                flights_list.append(flight_info)
            except: pass
        return flights_list

    def get_info(self):
        pass

    def get_flights(self, airline=""):
        raw_flights_data = self._get_flights_data()
        return self._parse_flights_data(raw_flights_data)

    def get_flight(self):
        pass

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        sys.exit('Usage: %s airport 4 digit code' % sys.argv[0])
    print Airport(sys.argv[1]).get_flights()