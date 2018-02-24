# DrunkSoulsStatTool
Over-engineered statistics tool for keeping track of a drinking game 

# Running the application
## Build executable zip archive
Run build script

`$ python3 ./build.py` 

The archive will be saved into the `build` folder. The file is completly standalone and can be run from anywhere.

`$ ./build/dsst`

## Run python script directly 
`$ python3 ./dsst/__main__.py`

# Dependencies
- GObject (Gtk3)
- mysqlclient (Python Mysql Driver)
- peewee (ORM Framework)
