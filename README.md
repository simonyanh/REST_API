# REST_API
Design a REST API according to the following specification:
As an API user, I should be able to:
*** for the each commands use the parameters list below

- Create a bug. A bug should have a title, a body, and a status (resolved/unresolved).	
					POST	.../bugs?title=TITLENAME&body=BUGDESCRIPTION&status=STATUS

- Edit a bug.				PATCH	.../bugs?title=TITLENAME&newtitle=NEWTITLE&body=DESCRIPTION&status=STATUS	(newtitle/body/status optional)
- Delete a bug.				DELETE	.../bugs?title=TITLENAME
- View all bugs. 			GET	.../allbugs
- View a specific bug.			GET	.../bugs?title=TITLENAME
- Add a comment to a bug. A comment should have a title, and a body.
					PUT	.../comment?title=TITLENAME&commenttitle=COMMENTTITLE&comment=COMMENTBODY

- Delete a comment from a bug.		DELETE	.../comment?title=TITLENAME
- Mark a bug as "resolved".		PATCH	.../bugs?title=TITLENAME&status=resolved
- Mark a bug as "unresolved".		PATCH	.../bugs?title=TITLENAME&status=unresolved
- View all bugs marked as "resolved".	GET	.../allbugs/resolved
- Assign the bug to a user. A user is identified by its ID.
					PUT	.../assign?title=TITLENAME&userid=USERID

You can use any python framework and database you wish

*** used python modules - flask, flask-RESTful, numpy, pandas
*** as a database I have used "data.csv" file in the same directory
