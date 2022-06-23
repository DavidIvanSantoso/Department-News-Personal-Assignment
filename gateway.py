import json
from matplotlib.font_manager import json_dump
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
import requests
from werkzeug.wrappers import Response
from dependencies.session import SessionProvider

class GatewayService:
    name = 'gateway'
    database=RpcProxy('department_service')
    session_provider = SessionProvider()

    @http('POST','/registration')
    def registration(self,request):
        username = "" 
        password = "" 
        data = format(request.get_data(as_text=True))
        array  =  data.split("&")

        for separator in array:
            cnt = separator.split("=")
            if cnt[0] == "username":
                username = cnt[1]
            if cnt[0] == "password":
                password = cnt[1]
        print(password)
        print(username)
        data_regis = self.database.registration(username, password)
        return json.dumps(data_regis)
    
    @http('GET', '/login')
    def login(self, request):
        username = "" 
        password = "" 
        data=format(request.get_data(as_text=True))
        array=data.split("&")
        for file in array:
            cnt     = file.split("=")
            if cnt[0] == "username":
                username = cnt[1]
            if cnt[0] == "password":
                password = cnt[1]
        check = self.database.login(username, password)
        
        if(check == 1):
            user_data = {
                'username': username,
                'password': password
            }
            session_id = self.session_provider.set_session(user_data)
            response = Response(str(user_data))
            response.set_cookie('SESSID', session_id)
            return response
        else:
            result = []
            result.append("Failed login")
            return json.dumps(result)
    
    @http('POST', '/logout')
    def logout(self, request):
        cookies = request.cookies
        if cookies:
            confirm = self.session_provider.delete_session(cookies['SESSID'])
            response = Response('Logout Successful')
            response.delete_cookie('SESSID')
    
    @http('GET', '/getallnews')
    def getallnews(self, request): 
        return json.dumps(self.database.getallnews())

    @http('GET', '/getnewsindex/<int:id>')
    def getnewsindex(self, request,id):
        return json.dumps(self.database.getnewsindex(id))

    @http('POST','/post')
    def post(self,request):
        cookies=request.cookies
        if(cookies):
            username = "" 
            news = "" 
            data=format(request.get_data(as_text=True))
            array=data.split("&")
            for file in array:
                cnt     = file.split("=")
                if cnt[0] == "username":
                    username = cnt[1]
                if cnt[0] == "news":
                    news = cnt[1]
            return json.dumps(self.database.post(username, news))
        else:
            return "Login first"

    @http('DELETE','/delete/<int:id>')
    def delete(self,request,id):
        cookies=request.cookies
        if(cookies):
            delete=self.database.delete(id)
            return json.dumps(delete)
        else:
            return "Login first"
    
    @http('POST','/update/<int:id>')
    def edit(self,request,id,news):
        cookies=request.cookies
        if(cookies):
            news=""
            data=format(request.get_data(as_text=True,buffered=True))
            array=data.split("&")
            for file in array:
                cnt     = file.split("=")
                if cnt[0] == "news":
                    news = cnt[1]
            return json.dumps(self.database.edit(id,news))
        
