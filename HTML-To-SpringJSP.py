'''

HTML To Spring JSP converter

Input: <HTML Theme Directory > <Directory In WEBAPP>

Created By: Ajinkya Bhosale
Mobile Number : 9028571192
Email ID: ajinkyabhosale121@gmail.com

'''

import os
import re
import optparse
import shutil

def main():

    print("\n\t\tHTML To Spring JSP converter\n")
  
    p = optparse.OptionParser()
  
    p.add_option('--ThemeDir', '-t', default="CurrentDir")
    p.add_option('--ResourceDir', '-r', default="\\resources\\")
  
    options, arguments = p.parse_args()
  
    options.ThemeDir = os.path.abspath(options.ThemeDir)
    
    resourceDir = options.ResourceDir.replace("\\","").replace("/","")
  
    print ('ThemeDir : %s' % options.ThemeDir)
    print ('ResourceDir : %s' % resourceDir)
    
    
    if (os.path.isdir(options.ThemeDir)):
        
        outputcont = open(os.path.join(options.ThemeDir,"SpringMVCController.java"),'w+')        
        outputcont.write("package com.your.packge.controller;\n\n")
        outputcont.write("import org.springframework.stereotype.Controller;\n")
        outputcont.write("import org.springframework.ui.Model;\n")
        outputcont.write("import org.springframework.web.bind.annotation.RequestMapping;\n")
        outputcont.write("import org.springframework.web.bind.annotation.RequestMethod;\n\n")
        outputcont.write("@Controller\n")
        outputcont.write("public class SpringMVCController {\n")
        
        controllinks = []
        for file in os.listdir(options.ThemeDir):
            if file.endswith(".html"):
                
                myfile = os.path.join(options.ThemeDir, file)
                newfile = myfile.split('.')[0] + ".jsp"
                
                print("Processing file:" + myfile)
                print("Processing newfile:" + newfile)
                
                links = [];
                scripts = [];
                alinks = [];
                imgurls = [];
                bgimgurls = [];
                
                inputfile = open(myfile)
                
                outputfile = open(newfile,'w+')
                
                lines = inputfile.readlines()
        
                outputfile.write("<%@ taglib uri=\"http://java.sun.com/jsp/jstl/core\" prefix=\"c\" %>\n")
                outputfile.write("<%@ taglib prefix=\"spring\" uri=\"http://www.springframework.org/tags\"%>\n")
                outputfile.write("<%@ page session=\"true\" %>\n\n")
                
                for line in lines:
                    
                    matchObj = re.match( r'.*<link.*href=\".*\"', line, re.M|re.I)
                    if matchObj:
                        #print ("match --> matchObj.group() : ", matchObj.group())
            
                        searchObj = re.search(r'(?<=\s)href=\".*\"(?=\>|\/|\s|\t)', line)
                        if searchObj:
                            #print ("search --> searchObj.group() : ", searchObj.group().split()[0])
                            href = searchObj.group().split()[0].split('\"')[1]
                            #print(href)
                            if href not in links:
                                links.append(href)
                            
                    matchObj = re.match( r'.*<script.*src=\".*\"', line, re.M|re.I)
                    if matchObj:
                        #print ("match --> matchObj.group() : ", matchObj.group())
            
                        searchObj = re.search(r'(?<=\s)src=\".*\"(?=\>|\/|\s|\t)', line)
                        if searchObj:
                            #print ("search --> searchObj.group() : ", searchObj.group().split()[0])
                            src = searchObj.group().split()[0].split('\"')[1]
                            #print(src)
                            if src not in scripts:
                                scripts.append(src)
                            
                    matchObj = re.match( r'.*<a\s.*href=\".*\"', line, re.M|re.I)
                    if matchObj:
                        #print ("match --> matchObj.group() : ", matchObj.group())
            
                        searchObj = re.search(r'(?<=\s)href=\".*\"(?=\>|\/|\s|\t)', line)
                        if searchObj:
                            #print ("search --> searchObj.group() : ", searchObj.group().split()[0])
                            src = searchObj.group().split()[0].split('\"')[1]
                            #print(src)
                            if src not in alinks:
                                alinks.append(src)
                                
                    matchObj = re.match( r'.*<img.*src=\".*\"', line, re.M|re.I)
                    if matchObj:
                        #print ("match --> matchObj.group() : ", matchObj.group())
            
                        searchObj = re.search(r'(?<=\s)src=\".*\"(?=\>|\/|\s|\t)', line)
                        if searchObj:
                            #print ("search --> searchObj.group() : ", searchObj.group().split()[0])
                            src = searchObj.group().split()[0].split('\"')[1]
                            #print(src)
                            if src not in imgurls:
                                imgurls.append(src)
                                
                    matchObj = re.match( r'.*background-image:.*', line, re.M|re.I)
                    if matchObj:
                        #print ("match --> matchObj.group() : ", matchObj.group())
            
                        searchObj = re.search(r'((?<=:)url(.*)(?<=;|\s|"))', line)
                        if searchObj:
                            #print ("search --> searchObj.group() : ", searchObj.group().split()[0])
                            src = searchObj.group().split()[0].split('\'')[1]
                            #print(src)
                            if src not in bgimgurls:
                                bgimgurls.append(src)
               
                for line in lines:
                    if line.find("<head>") != -1:
                        outputfile.write(line + "\n\n")
                        for link in links:
                            linkname = (link.split('/')[-1].split('.')[0] + link.split('/')[-1].split('.')[1] + link.split('/')[-1].split('.')[-1]).replace("-","")
                            url = "\n<c:url value=\"/" + resourceDir +"/" + link + "\" var=\"" + linkname +"\" />\n"
                            outputfile.write(url)
                            #print(url)
                            
                        outputfile.write("\n")
                            
                        for script in scripts:
                            scriptname = (script.split('/')[-1].split('.')[0]  + script.split('/')[-1].split('.')[1]  + script.split('/')[-1].split('.')[-1]).replace("-","")
                            url = "\n<c:url value=\"/" + resourceDir + "/" + script + "\" var=\"" + scriptname +"\" />\n"
                            outputfile.write(url)
                            #print(url)
                        
                        outputfile.write("\n")
                         
                        for imgurl in imgurls:
                            imgurlname = (imgurl.split('/')[-1].split('.')[0]  + imgurl.split('/')[-1].split('.')[1]  + imgurl.split('/')[-1].split('.')[-1]).replace("-","")
                            url = "\n<c:url value=\"/" + resourceDir + "/" + imgurl + "\" var=\"" + imgurlname +"\" />\n"
                            outputfile.write(url)
                            #print(url)
                            
                        for bgimgurl in bgimgurls:
                            bgimgurlname = (bgimgurl.split('/')[-1].split('.')[0]  + bgimgurl.split('/')[-1].split('.')[1]  + bgimgurl.split('/')[-1].split('.')[-1]).replace("-","")
                            url = "\n<c:url value=\"/" + resourceDir + "/" + bgimgurl + "\" var=\"" + bgimgurlname +"\" />\n"
                            outputfile.write(url)
                            #print(url)
                        
                        outputfile.write("\n")
                        
                    elif line.find("<link") != -1:
                        for link in links:
                            #print("Link" + line)
                            if line.find(link) != -1:
                                linkname = ("${" + link.split('/')[-1].split('.')[0]  + link.split('/')[-1].split('.')[1]  + link.split('/')[-1].split('.')[-1] + "}").replace("-","")
                                newline = line.replace(link, linkname)
                                #print(link + " " + linkname + " " + newline)
                                outputfile.write(newline)
                     
                    elif line.find("<script") != -1:
                        for script in scripts:
                            #print("Script" + line)
                            if line.find(script) != -1:
                                scriptname = ("${" + script.split('/')[-1].split('.')[0]  + script.split('/')[-1].split('.')[1]  + script.split('/')[-1].split('.')[-1] + "}").replace("-","")
                                newline = line.replace(script, scriptname)
                                #print(script + " " + scriptname + " " + newline)
                                outputfile.write(newline)
                    
                    elif line.find("<a ") != -1:
                        for alink in alinks:
                            #print("Alink : " + line)
                            if line.find(alink) != -1:
                                searchObj = re.search(r'(?<=\s)href=\".*\"(?=\>|\/|\s|\t)', line)
                                if searchObj:
                                    #print ("search --> searchObj.group() : ", searchObj.group().split()[0])
                                    src = searchObj.group().split()[0].split('\"')[1]
                                
                                    if (alink == src):
                                        if alink.find(".") != -1:
                                            if (alink.split('.')[1] == "html"):
                                                alinkname = "<c:url value='/" + alink.split('.')[0] + "' />"
                                                newline = line.replace(alink, alinkname)
                                                #print(alink + " " + alinkname + " " + newline)
                                                outputfile.write(newline)
                                            else:
                                                outputfile.write(line)
                                        else:
                                            outputfile.write(line)
                                    
                    elif line.find("<img") != -1:
                        for imgurl in imgurls:
                            #print("imgurl" + line)
                            if line.find(imgurl) != -1:
                                imgurlname = ("${" + imgurl.split('/')[-1].split('.')[0]  + imgurl.split('/')[-1].split('.')[1]  + imgurl.split('/')[-1].split('.')[-1] + "}").replace("-","")
                                newline = line.replace(imgurl, imgurlname)
                                #print(imgurl + " " + imgurlname + " " + newline)
                                outputfile.write(newline)
                    
                    elif line.find("background-image:url") != -1:
                        for bgimgurl in bgimgurls:
                            #print("imgurl" + line)
                            if line.find(bgimgurl) != -1:
                                bgimgurlname = ("${" + bgimgurl.split('/')[-1].split('.')[0]  + bgimgurl.split('/')[-1].split('.')[1]  + bgimgurl.split('/')[-1].split('.')[-1] + "}").replace("-","")
                                newline = line.replace(bgimgurl, bgimgurlname)
                                #print(imgurl + " " + imgurlname + " " + newline)
                                outputfile.write(newline)
                    
                    
                    else:
                        outputfile.write(line)
                
                outputfile.truncate()
                
                # print(links)
                # print(scripts)
                # print(alinks)
                # print(bgimgurls)
                
                for link in alinks:
                    if link not in controllinks:
                        if link.find("#") == -1:
                             if link.find(".") != -1:
                                if link.split(".")[1] == "html":
                                    controllinks.append(link)
        
        #print(controllinks)
        
        for link in controllinks:
            outputcont.write("\n\t@RequestMapping(value = \"/\", method = RequestMethod.GET)".replace("/", "/" + link.split(".")[0]))
            outputcont.write("\n\tpublic String home(Model model, HttpSession session) {\n".replace("home", link.split(".")[0].replace("-","")))
            outputcont.write("\n\t\treturn \"index\";\n".replace("index", link.split(".")[0]))
            outputcont.write("\t}\n")
        
        outputcont.write("\n}\n")
        outputcont.truncate()
        
    else:
        print("Please Enter a Valid Directory!");

        
if __name__== "__main__":
    main()
