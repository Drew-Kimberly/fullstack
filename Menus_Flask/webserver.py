__author__ = 'Drew'
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi #Common Gateway Interface
import bleach
import urllib2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('postgresql:///menus')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200) #200 status code indicates successful GET request
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += "<form method='POST' enctype = 'multipart/form-data' action = '/" \
                      "hello'><h2>What would you like me to say?</h2><input name='message'" \
                      "type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161;Hola <a href = '/hello'>Back to Hello</a>"
                output += "<form method='POST' enctype = 'multipart/form-data' action = '/" \
                      "hello'><h2>What would you like me to say?</h2><input name='message'" \
                      "type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                session = DBSession()
                restaurants = session.query(Restaurant).order_by(Restaurant.name.asc()).all()
                session.close()

                output = ""
                output += "<html><body>"
                output += "<div class='newRestaurant' style='padding-bottom:20px;'>"
                output += "<a href='/restaurants/new'>Make a New Restaurant Here</a>"
                output += "</div>"
                for restaurant in restaurants:
                    output += "<div class='restaurant' style='padding-bottom:30px;'>"
                    output += "<span><strong>" + bleach.clean(restaurant.name) + "</strong></span>"
                    output += "<br />"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "<br />"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "</div>"
                output += "</body></html>"

                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/new'>" \
                        "<h2>Make a New Restaurant</h2><input name='restaurant'" \
                        "type='text'><input type='submit' value='Create'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith("/edit"):
                #Parse URL path to get restaurant ID
                restaurant_id = int(self.path.split("/")[2])

                #Get Restaurant name from db
                session = DBSession()
                restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                session.close()

                if restaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h1>%s</h1>" % bleach.clean(restaurant.name)
                    output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/edit'>" \
                            "<input name='newRestaurantName' type='text'><input type='submit' value='Rename'></form>" \
                              % str(restaurant_id)
                    output += "</body></html>"

                    self.wfile.write(output)
                    return
                else:
                    print("Could not not retrieve restaurant from the DB in GET method.")

            if self.path.endswith("/delete"):
                #Parse URL path to get restaurant ID
                restaurant_id = int(self.path.split("/")[2])

                #Get Restaurant object from db with given id
                session = DBSession()
                restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                session.close()

                if restaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?</h1>" % bleach.clean(restaurant.name)
                    output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" \
                            "<input type='submit' value='Delete'></form>" \
                              % str(restaurant_id)
                    output += "</body></html>"

                    self.wfile.write(output)
                    return
                else:
                    print("Could not not retrieve restaurant from the DB in GET method.")

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    content = fields.get('restaurant')
                    restaurant = content[0]

                session = DBSession()
                try:
                    session.add(Restaurant(name=restaurant))
                    session.commit()
                except:
                    print("An error occurred when creating the restaurant: %s" % bleach.clean(restaurant))
                session.close()

                #Redirect to restaurants page
                self.send_response(301) #301 status code indicates successful POST request
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):
                restaurant_id = int(self.path.split("/")[2])
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    content = fields.get('newRestaurantName')
                    new_restaurant_name = content[0]

                session = DBSession()
                try:
                    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                    restaurant.name = new_restaurant_name
                    session.add(restaurant)
                    session.commit()
                except:
                    print("An error occurred when editing the restaurant: %s" % bleach.clean(restaurant.name))
                session.close()

                #Redirect to restaurants page
                self.send_response(301) #301 status code indicates successful POST request
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/delete"):
                restaurant_id = int(self.path.split("/")[2]) #Grab Restaurant ID from URL path

                session = DBSession()
                try:
                    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
                    session.delete(restaurant)
                    session.commit()
                except:
                    print("An error occurred when deleting the restaurant: %s" % restaurant.name)
                session.close()

                #Redirect to restaurants page
                self.send_response(301) #301 status code indicates successful POST request
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/hello") or self.path.endswith("/hola"):
                self.send_response(301) #301 status code indicates successful POST request
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type')) #Parses html form-header into main value
                                                                                        #and dictionary of parameters
                if ctype == 'multipart/form-data': #Check that we're receiving form data
                    fields = cgi.parse_multipart(self.rfile, pdict) #Collect all the fields in a form
                    message_content = fields.get('message') #Get specific value of a field 'message' and store in array

                output = ""
                output += "<html><body>"
                output += "<h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % bleach.clean(message_content[0])
                output += "<form method='POST' enctype = 'multipart/form-data' action = '/" \
                          "hello'><h2>What would you like me to say?</h2><input name='message'" \
                          "type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                print(output)
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt: #Triggered when user holds 'CTRL + C' on keyboard
        print "CTRL+C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()