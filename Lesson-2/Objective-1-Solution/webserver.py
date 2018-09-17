#!/usr/bin/env python3
# different imports
from http.server import HTTPServer, BaseHTTPRequestHandler
# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):
    form_html = \
        '''
        <form method='POST' enctype='multipart/form-data' action='/hello'>
        <h2>What would you like me to say?</h2>
        <input name="message" type="text"><input type="submit" value="Submit" >
        </form>
         '''

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output.encode())
                return

        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))
def main():
    try:
        server = HTTPServer(('', 8080), webServerHandler)
        print 'Web server running...open localhost:8080/restaurants in your browser'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
