
# -*- coding: UTF-8 -*-
"""
flask_navbar.py
"""

from collections import OrderedDict
from flask import request
from flask.templating import render_template_string


#ul_tpl = """

#ul
    #each nav_link in nav_links
        #if request.blueprint == nav_link.name:
            #li(class=highlight_class): a(href=nav_link.url): strong= nav_link.anchor
        #else:
            #li(class=normal_class): a(href=nav_link.url)= nav_link.anchor

#"""

ul_tpl = """
<ul class="nav navbar-nav">
  {% for nav_link in nav_links %}
    {% if request.blueprint == nav_link.name %}
      <li class="{{ highlight_class }}">
        <a href="{{ nav_link.url }}">
          <strong>{{ nav_link.anchor }}</strong>
        </a>
      </li>
    {% else %}
      <li class="{{ normal_class }}">
        <a href="{{ nav_link.url }}">{{ nav_link.anchor }}</a>
      </li>
    {% endif %}
  {% endfor %}
</ul>
"""

ul_tpl_grouped = """
<ul class="nav navbar-nav">
  {% for group, (highlighted, links) in nav_group_d.items() %}
    <li class={% if highlighted %}"{{ highlight_class }}"{% else %}"{{ normal_class }}"{% endif %}>
    <a href="{{ links[0].url }}">
      {% if highlighted %}
        <strong>
      {% endif %}
      {{ group }}
      {% if links[0].count is not none %}
        <span class="badge">{{ links[0].count }}</span>
      {% endif %}
      {% if highlighted %}
        </strong>
      {% endif %}
    </a>
    </li>
    {% if links|length > 1 %}
      <li class="dropdown {% if highlighted %}{{ highlight_class }}{% else %}{{ normal_class }}{% endif %}">
        <a class="dropdown-toggle" data-toggle="dropdown" href="#">
          <b class="caret"></b>
        </a>
        <ul class="dropdown-menu" role="menu" aria-labelledby="dLabel">
          {% for nav_link in links %}
            {% if nav_link.enabled() %}
              <li class="{{ highlight_class }}">
                <a href="{{ nav_link.url }}">
                  <strong>{{ nav_link.anchor }}</strong>
                </a>
              </li>
            {% else %}
              <li class="{{ normal_class }}">
                <a href="{{ nav_link.url }}">{{ nav_link.anchor }}</a>
              </li>
            {% endif %}
          {% endfor %}
        </ul>
      </li>
    {% endif %}
  {% endfor %}
</ul>
"""

class NavLink(object):

    def __init__(self, name, anchor, permissions, lazy_url, group, enabler, cnt=None):
        self.name = name
        self._anchor = anchor
        self.permissions = permissions
        self.__lazy_url = lazy_url
        self._group = group
        self.enabler = enabler
        self.__count__ = cnt

    @property
    def count(self):
        if isinstance(self.__count__, type):
            return self.__count__()
        else:
            return self.__count__

    @property
    def anchor(self):
        if isinstance(self._anchor, basestring):
            return self._anchor
        else:
            return self._anchor()

    @property
    def group(self):
        if isinstance(self._group, basestring):
            return self._group
        else:
            return self._group()

    def enabled(self):
        return self.enabler(self)
        
    @property
    def url(self):
        return self.__lazy_url()


class FlaskNavBar(object):
    def __init__(self, app, project_name=""):
        self.app = app
        self.project_name = project_name
        self.__all_nav_links = []
    
    def register(self, blueprint, default_url="", name="", permissions=None, group="", enabler=None, count=None):
        if not permissions:
            permissions = []
        from flask import url_for
        url = lambda: (default_url if default_url else url_for(blueprint.name+".index"))
        name = name or blueprint.name
        group = group or name
        enabler = enabler or (lambda nav: nav.name == request.blueprint)
        self.__all_nav_links.append(NavLink(blueprint.name, name, permissions, url, group, enabler, count))
        
    @property
    def nav_links(self):
        registered_bluprint_names = set(b.name for b in self.app.blueprints.values())
        for nav_link in self.__all_nav_links:
            if nav_link.name in registered_bluprint_names:
                if all(perm.can() for perm in nav_link.permissions):
                    yield nav_link
    
    def as_ul(self, highlight_class="", normal_class="", grouped=False):
        if not grouped:
            return render_template_string(ul_tpl, nav_links=self.nav_links, 
                                          project_name=self.project_name,
                                          highlight_class=highlight_class, 
                                          normal_class=normal_class)
        else:
            nav_group_d = OrderedDict()
            for link in self.nav_links:
                if link.group not in nav_group_d:
                    nav_group_d[link.group] = [False, []]
                nav_group_d[link.group][1].append(link)
            for link in self.nav_links:
                if request.blueprint == link.name:
                    nav_group_d[link.group][0] = True
                    break
            return render_template_string(ul_tpl_grouped, nav_group_d=nav_group_d, 
                                          project_name=self.project_name,
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
    nav_bar.register(test2, "/test2/index", group="test1")
    nav_bar.register(test3, "/test3/index", permissions=[FakePermission()])
    nav_bar.register(test3, "/test3/index")
    nav_bar.register(test4, "/test4/index")
    
    
    with app.test_request_context("/test2/index.html"):
        from flask.templating import render_template_string
        print render_template_string('<html>{{nav_bar.as_ul("highlight", grouped=True)|safe}}</html>', 
                                    nav_bar=nav_bar)
        print render_template_string('<html>{{nav_bar.as_ul("highlight")|safe}}</html>', 
                                    nav_bar=nav_bar)
        
