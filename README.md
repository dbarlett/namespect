# namespect

namespect, configured for DreamHost shared hosting.

### Local Quickstart
```sh
$ git clone https://github.com/dbarlett/namespect.git namespect
$ cd namespect
$ cp config.py.dist config.py
$ nano config.py # SQLAlchemy URL
$ ./setup.sh
$ source env/bin/activate
$ python run.py
```
Browse to http://localhost:5000

### Deploying to DreamHost
Create a new (sub)domain with Passenger enabled.
- User: `myuser`
- Subdomain: `namespect.example.com`
- Web directory: `/home/myuser/namespect.example.com/public` 

Login as `myuser`, remove the default content, and clone this repo:
```sh
$ pwd
/home/myuser
$ rm -rf namespect.example.com
$ git clone https://github.com/dbarlett/namespect.git namespect.example.com
```

Configure the environment:
```sh
$ cd namespect.example.com
$ cp config.py.dist config.py
$ nano config.py
$ ./setup.sh
```
Browse to http://namespect.example.com.