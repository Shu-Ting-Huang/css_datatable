import pandas
import os

hovering=True

class HTMLElement:
    """
    The type of content may be
    (1) string
    (2) HTMLElement
    (3) list consisting of HTMLElement or string
    """
    def __init__(self,tag,content,one_line=None,indent=None,attribute={}):
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
        if type(self.content)==str: #(1) self.content is a string
            content_text=self.content
        elif type(self.content)==HTMLElement: #(2) self.content is HTMLElement object
            content_text=self.content.to_str()
        elif type(self.content)==list: #(3) self.content is a list
            content_text=""
            for obj in self.content:
                content_text += (obj.to_str()+"\n")
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
            row.content+=[HTMLElement('td',str(df.iat[i,j]))]
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
    f=open(file_name+".html",'w')
    f.write(df2html(df,title=title))
    f.close()
    os.system('start Chrome \"'+cwd+"\\"+file_name+'.html\"')
