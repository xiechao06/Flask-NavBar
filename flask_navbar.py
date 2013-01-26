# -*- coding: UTF-8 -*-
"""
flask_navbar.py
"""
__author__ = "xiechao"
__author_email__ = "xiechao06@gmail.com"
__version__ = "0.9.0"

from collections import namedtuple
from flask import url_for, request
from flask.ext.principal import Permission
from flask.templating import render_template_string
import jinja2



ul_tpl = """

ul
    each nav_link in nav_links
        if request.blueprint == nav_link.name:
            li(class=highlight_class): a(href=nav_link.url): strong= nav_link.anchor
        else:
            li(class=normal_class): a(href=nav_link.url)= nav_link.anchor
        
"""

NavLink = namedtuple("NavLink", ["name", "anchor", "permissions", "url"])

class FlaskNavBar(object):

    def __init__(self, app, highlight_class="", normal_class=""):
        self.app = app
        self.__all_nav_links = {}
        self.highlight_class = highlight_class
        self.normal_class = normal_class
    
    def register(self, blueprint, default_url="", name="", permissions=[]):
        if self.__all_nav_links.has_key(blueprint.name):
            raise RunTimeError("blueprint %s has been registered" % blueprint.name)
        self.__all_nav_links[blueprint.name] = NavLink(blueprint.name, blueprint.name if not name else name, permissions, default_url)
        
    @property
    def nav_links(self):
        for blueprint in self.app.blueprints.values():
            try:
                nav_link = self.__all_nav_links[blueprint.name]
            except KeyError:
                continue
            
            if all(perm.can() for perm in nav_link.permissions):
                yield nav_link
        
    
    def as_ul(self):
        return render_template_string(ul_tpl, nav_links=self.nav_links, 
            highlight_class=self.highlight_class, 
            normal_class=self.normal_class)
    

if __name__ == "__main__":
    from flask import Flask, Blueprint
    app = Flask(__name__)
    nav_bar = FlaskNavBar(app, highlight_class="highlight")
    
    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

    test1 = Blueprint("test1", __name__)
    @test1.route("/")
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
    
    nav_bar.register(test1, "/test1/index")
    nav_bar.register(test2, "/test2/index")
    nav_bar.register(test3, "/test2/index", permissions=[FakePermission()])
    
    
    with app.test_request_context("/test1/"):
        print nav_bar.as_ul()
        
