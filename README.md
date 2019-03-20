README file for Item Catalog Project 

1. This is a flask web application, Item Catalog, that will start a 
   webserver at localhost:5000.
2. Data is stored in a SQLite database hosted on the local machine.
3. A third party authentication system is in place using OAuth 2.0 with Google API.
4. All the CRUD operations for Items are in place.


Dependencies

1. Virtual Machine (Virtualbox)
2. Vagrant software to configure and manage the virtual machine.
3. Use any IDE (used pyCharm)

How to start the application:

1. If using virtual machine, in gti bash, go to the root directory.
   of the git repo, and find the vagrant file.
2. Run vagrant up - wait till execution finishes, this may take time.
3. Run vagrant ssh - to SSH you into the VM.
4. Traverse to the /vagrant/item_catalog folder.
5. Run python models.py program to create the item-catalog database.
6. Run python lotsofitems.py program to populate the database.
7. Now, run the webserver - app.py - this should start the server.
8. Open browser, and type in localhost:5000 in the url. 


Design

1. The backend database is SQLite. The database is mapped to ORM using 
   SQLAlchemy.
2. Webserver framework used is Flask.
3. In line with PEP8 style guide.


Meeting all the Rubric requirements:

1. The project implements a JSON endpoint that shows all the data,
   all categories and items in each category.
2. Website reads category and item information from a database.
3. Website includes a form allowing users to add new items 
   and correctly processes submitted forms.
4. Website includes a form to edit/update a selected item 
   in the database table and correctly processes submitted forms.
5. Website includes a function to delete a selected item.
6. Create, delete and update operations do consider authorization 
   status prior to execution.
7. Page implements a third-party (Google API) authentication 
   & authorization service instead of implementing its own 
   authentication & authorization spec.
8. There is a 'Login' and 'Logout' button/link in the project.
9. Code is ready for personal review and neatly formatted 
   and compliant with the Python PEP 8 style guide.
10. Comments are present and effectively explain 
    longer code procedures. 
11. README file includes details of all the steps required 
    to successfully run the application.  

 
