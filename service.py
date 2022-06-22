from nameko.rpc import rpc

import dependencies.database as database

class DepartmentService:
    name = 'department_service'

    db=database.DatabaseProvider()

    @rpc
    def registration(self,username, password):
        regis = self.db.registration(username, password)
        return regis

    @rpc
    def login(self, username, password):
        logina = self.db.login(username, password)
        return logina

    @rpc
    def getallnews(self):
        news = self.db.getallnews()
        return news

    @rpc
    def getnewsindex(self, id):
        newsid = self.db.getnewsindex(id)
        return newsid
    
    @rpc
    def post(self, desc):
        post = self.db.post(desc)
        return post
    
    @rpc
    def edit(self, id, desc):
        edit = self.db.edit(id, desc)
        return edit
    
    @rpc
    def delete(self, id):
        delete = self.db.delete(id)
        return delete