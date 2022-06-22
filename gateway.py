import json
from matplotlib.font_manager import json_dump
from nameko.rpc import RpcProxy
from nameko.web.handlers import http
from werkzeug.wrappers import Response
from dependencies.session import SessionProvider

class GatewayService:
    name='gateway'
    database=RpcProxy('department_service')
    session_provider = SessionProvider()

    @http('POST','/registration')
    def registration(self,request):
        data = format(request.get_data(as_text=True))
        arr  =  data.split("&")

        username = "" 
        password = "" 

        for separator in arr:
            node = separator.split("=")
            if node[0] == "username":
                username = node[1]
            if node[0] == "password":
                password = node[1]
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
        flags = self.database.login(username, password)
        
        if(flags == 1):
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
            if (confirm):
                response = Response('Logout Successful')
                response.delete_cookie('SESSID')
            else:
                response = Response("Logout Failed")
            return response
    
    @http('GET', '/getallnews')
    def getallnews(self, request):
        news = self.database.getallnews()
        return json.dumps(news)

    @http('GET', '/getnewsindex/<int:id>')
    def getnewsindex(self, request,id):
        news = self.database.getnewsindex(id)
        return json.dumps(news)