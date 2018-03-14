# DrunkSoulsStatTool
Over-engineered statistics tool for keeping track of a drinking game 

## Running the application
The application is split into an server and client part.
To run standalone on a single machine you will have to have a running
dsst-server that is connected to a mysql database.

Using the client you can then connect to the server via its 
specified port.
### Building
Run the build script with the desired option

`$ python3 ./build.py {gtk3|server|all}`

The archive(s) will be saved into the `build` folder.
To run either server or client, just execute the archive files.

`$ ./build/dsst-server-0.1` 

To run the server.

`$ ./build/dsst-gtk3-0.1`

To run the GTK client.

## Dependencies
- Python 3
### Client
- python-gi <= v3.16 (Gtk3)

### Server
- mysqlclient (Python Mysql Driver)
- peewee (ORM Framework)
