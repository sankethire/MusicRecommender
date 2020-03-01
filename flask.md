# Flask

## Bsics

- WSGI
- Jinja2

### App

1. `app = Flask(name)`
   1. `app.run(host, port, options)`
	2. debug mode
3. route
   1. bind url to func
   2. input through route
      1. `'route/<int:var_name>'`
   3. `\name\` in route vs `\name`
   4. url for get url of alreay existing pages
4. http protocols
   1. get
   2. head
   3. post
   4. put
   5. delete
5. Global request objects
   1. Form
   2. args
   3. Cookies - save client data on user side
      1. `resp = make_response(render_template('.html')`
      2. `resp.set_cookie('string', value)`
      3. `value = request.cookie.get('string')`
   4. files
   5. Method
6. Redirect
   1. location
   2. statuscode
      1. `flask.abort(code)`
   3. response
7. Extensions
   1. like SQLAlchemy

### Jinja

1. Delimiters
   1. {%%} statement
      1. if endif
      2. for endfor
