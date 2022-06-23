# Department-News-Personal-Assignment

This is a deparment news service program for CRUD (Create, Edit, Upload, Edit) about news
<br>
I use nameko and redis for this project
<br>
For testing all of the feature in this project i use Postman
<br>
Features:
1. Register @http('POST','/registration/')
2. Login @http('GET','/login')
3. Logout @http('POST','/logout)
4. Get All News('GET', '/getallnews') (No need for login)
6. Get News by Index ('GET','/getnewsindex/<int:id>') (No need for login)
7. Post News ('POST','/post') ( Login needed & add data from Postman body with x-www-form-urlencoded)
8. Edit News ('POST','/edit/<int:id>') (Login needed & edit description from Postman body with x-www-form-urlencoded)
9. Delete News ('DELETE','/delete/<int:id>') (Login needed)
