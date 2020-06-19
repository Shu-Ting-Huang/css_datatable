##########################################################################
#
# The way to use this package for converting DataFrame to html file:
# >>> import my_html
# >>> my_html.create_html(df,title="No Title",file_name="No Name")
#
##########################################################################
#
# Configuration variables:
# hovering
# separator
# create_link
#
##########################################################################

import pandas
import os
from decimal import Decimal

hovering=True
separator=True
create_link=True

def add_sep(x):
    if type(x)==int or type(x)==Decimal:
        return "{:,}".format(x)
    else:
        return x

def link(url,text,new_tab=True):
    attr={'href':url}
    if new_tab==True:
        attr['target']='_blank'
    return HTMLElement('a',text,attribute=attr)

def url_link(x):
    if type(x)==str and (x[:7]=="http://" or x[:8]=="https://"):
        return link(x,"Link")
    else:
        return x

class HTMLElement:
    """
    HTMLElement is the class of html elements. Its instance consists of
        (1) tag
        (2) content
            type(content) may be
            (a) str
            (b) HTMLElement
            (c) list consisting of HTMLElement or str
        (3) attribute={}
        (4) one_line and indent, which deal with organizing html code
    """
    def __init__(self,tag,content,one_line=None,indent=None,attribute={}):
        assert type(tag)==str
        assert isinstance(content,(str,HTMLElement,list))
        assert type(content)!=list or\
               all( isinstance(x,(str,HTMLElement)) for x in content )
        assert type(attribute)==dict
        assert all(type(x)==type(attribute[x])==str for x in attribute.keys())
        assert {one_line,indent}.issubset({True,False,None})
        
        if (one_line,indent)==(None,None):
            if tag in {"td","th","title","a"}:
                (one_line,indent)=(True,None)
            elif tag in set(): #{"html"}:
                (one_line,indent)=(False,False)
            else:
                (one_line,indent)=(False,True)
        else:
            if one_line==True:
                (one_line,indent)=(True,None)
            elif (one_line,indent)==(False,None):
                (one_line,indent)=(False,True)
            elif (one_line,indent)==(None,True) or (one_line,indent)==(None,False):
                (one_line,indent)=(False,indent)
        self.tag=tag
        self.content=content
        self.one_line=one_line
        self.indent=indent
        self.attribute=attribute
                 
    def to_str(self):
        #create start_tag
        start_tag="<"+self.tag
        for key in self.attribute.keys():
            start_tag+=(" "+key+'=\"'+self.attribute[key]+'\"')
        start_tag+=">"
        
        #create end_tag
        end_tag="</"+self.tag+">"

        #create content_text
        if type(self.content)==str: #(a) self.content is a string
            content_text=self.content
        elif type(self.content)==HTMLElement: #(b) self.content is HTMLElement object
            content_text=self.content.to_str()
        elif type(self.content)==list: #(c) self.content is a list of HTMLElement or str
            content_text=""
            for obj in self.content:
                if type(obj)==HTMLElement:
                    content_text += (obj.to_str()+"\n")
                elif type(obj)==str:
                    content_text += (obj+"\n")
            content_text=content_text[:-1]

        #create result
        if self.one_line==True:
            result=start_tag+content_text+end_tag
        elif self.indent==False:
            result=start_tag+"\n"+content_text+"\n"+end_tag
        else:
            result=start_tag+"\n\t"+content_text.replace("\n","\n\t")+"\n"+end_tag
        return result


def table(df):
    thead=HTMLElement('thead',HTMLElement('tr',[]))
    thead.content.content+=[HTMLElement('th',"&nbsp;"*3)]
    for j in range(df.shape[1]):
        thead.content.content+=[HTMLElement('th',str(df.columns[j]))]
    
    tbody=HTMLElement('tbody',[])
    for i in range(df.shape[0]):
        row=HTMLElement('tr',[HTMLElement('td',str(df.index[i]))])
        for j in range(df.shape[1]):
            if create_link==True:
                td_content=url_link(df.iat[i,j])
                if type(td_content)!=HTMLElement:
                    td_content=str(td_content)
            else:
                td_content=str(df.iat[i,j])                
            row.content+=[HTMLElement('td',td_content)]
        tbody.content+=[row]
           
    return HTMLElement("table",[thead,tbody])

def df2html(df,title="No Title"):
    if hovering==True:
        from my_html.style import hover as style_content
    else:
        from my_html.style import no_hover as style_content        
    style_elmt=HTMLElement("style",style_content,attribute={"type":"text/css"})
    table_elmt=table(df)
    body_elmt=HTMLElement("body",[style_elmt,table_elmt],attribute={"bgcolor":"#F1FAFA"})
    head_elmt=HTMLElement("head",HTMLElement("title",title))
    html_elmt=HTMLElement("html",[head_elmt,body_elmt])
    return html_elmt.to_str()
    
#html escape character?
# '<' --> '&lt;'
# '>' --> '&gt;'
# '\"' --> '&quot;'
# "\'" --> '&apos;'
# '/' --> '&#47;'
# '&' --> '&amp;'

def create_html(df,title="No Title",file_name="No Name"):
    cwd=os.getcwd()
    assert cwd!='C:\\Users\\Alan\\AppData\\Local\\Programs\\Python\\Python38'

    if separator==True:
        df=df.applymap(add_sep)

    f=open(file_name+".html",'w')
    f.write(df2html(df,title=title))
    f.close()
    os.system('start Chrome \"'+cwd+"\\"+file_name+'.html\"')
