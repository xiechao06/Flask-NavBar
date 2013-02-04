
# -*- coding: UTF-8 -*-
"""
flask_navbar.py
"""
__author__ = "xiechao"
__author_email__ = "xiechao06@gmail.com"
__version__ = "0.9.0"

from flask import url_for, request
from flask.ext.principal import Permission
from flask.templating import render_template_string
import jinja2



#ul_tpl = """

#ul
    #each nav_link in nav_links
        #if request.blueprint == nav_link.name:
            #li(class=highlight_class): a(href=nav_link.url): strong= nav_link.anchor
        #else:
            #li(class=normal_class): a(href=nav_link.url)= nav_link.anchor

#"""

ul_tpl = """

<ul class="nav">
{% for nav_link in nav_links %}

{% if request.blueprint == nav_link.name %}
    <li class="{{highlight_class}}">
    	<a href="{{nav_link.url}}">
            <strong>{{nav_link.anchor}}</strong>
        </a>
    </li>
{% else %}
    <li class="{{normal_class}}">
    	<a href="{{nav_link.url}}">{{nav_link.anchor}}</a>
    </li>
{% endif %}

{% endfor %}
</ul>

"""

class NavLink(object):

    def __init__(self, name, anchor, permissions, lazy_url):
        self.name = name
        self.anchor = anchor
        self.permissions = permissions
        self.__lazy_url = lazy_url
        
    @property
    def url(self):
        return self.__lazy_url()

class FlaskNavBar(object):

    def __init__(self, app):
        self.app = app
        self.__all_nav_links = []
    
    def register(self, blueprint, default_url="", name="", permissions=[]):
        from flask import url_for
        url = lambda: (default_url if default_url else url_for(blueprint.name+".index"))
        self.__all_nav_links.append(NavLink(blueprint.name, blueprint.name if not name else name, permissions, url))
        
    @property
    def nav_links(self):
        registered_bluprint_names = set(b.name for b in self.app.blueprints.values())
        for nav_link in self.__all_nav_links:
            if nav_link.name in registered_bluprint_names:
                if all(perm.can() for perm in nav_link.permissions):
                    yield nav_link
    
    def as_ul(self, highlight_class="", normal_class=""):
        return render_template_string(ul_tpl, nav_links=self.nav_links, 
            highlight_class=highlight_class, 
            normal_class=normal_class)

if __name__ == "__main__":
    from flask import Flask, Blueprint
    app = Flask(__name__)
    nav_bar = FlaskNavBar(app)
    
    test1 = Blueprint("test1", __name__)
    @test1.route("/index.html")
    def index():
        return "test1"
    app.register_blueprint(test1, url_prefix="/test1")
    
    test2 = Blueprint("test2", __name__)
    @test2.route("/")
    def index():
        return "test2"
    app.register_blueprint(test2, url_prefix="/test2")

    test3 = Blueprint("test3", __name__)
    @test3.route("/")
    def index():
        return "test3"
    app.register_blueprint(test3, url_prefix="/test3")
    
    class FakePermission(object):
        def can(self):
            return False

    test4 = Blueprint("test4", __name__)
    @test3.route("/")
    def index():
        return "test4"
    
    nav_bar.register(test1)
    nav_bar.register(test2, "/test2/index")
    nav_bar.register(test3, "/test3/index", permissions=[FakePermission()])
    nav_bar.register(test3, "/test3/index")
    nav_bar.register(test4, "/test4/index")
    
    
    with app.test_request_context("/test1/index.html"):
        from flask.templating import render_template_string
        print render_template_string('<html>{{nav_bar.as_ul("highlight")|safe}}</html>', 
                                    nav_bar=nav_bar)
        
