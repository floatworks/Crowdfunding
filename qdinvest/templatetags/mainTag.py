#coding=utf-8 
from django import template
register = template.Library()

class NavTagItem(template.Node): 
    def __init__(self, nav_path, nav_displaytext,nav_class): 
        self.path = nav_path.strip('"') 
        self.text = nav_displaytext.strip('"') 
        self.nav_class = nav_class.strip('"')
         
    def render(self, context): 
        cur_path = context['request'].path 
        #print cur_path,self.path
        current = False 
        if self.path == '/': 
            current = cur_path == '/' 
        else: 
            current = cur_path.startswith(self.path) 
        cur_id = '' 
        if current: 
            cur_id = 'class="hover"' 
             
        return '<li %s><a href="%s" class="%s">%s</a></li>' % (cur_id, self.path,self.nav_class, self.text) 

#注册tag，函数基本就是这个样子，不怎么会有变化     
@register.tag 
def navtagitem(parser, token): 
    try: 
        tag_name, nav_path, nav_text, nav_class= token.split_contents() 
    except ValueError: 
        raise template.TemplateSyntaxError, \
                "%r tag requires exactly two arguments: path and text" % \
                token.split_contents[0] 
     
    return NavTagItem(nav_path, nav_text,nav_class) 