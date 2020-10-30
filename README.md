# HITO Database Frontend

## Database

Requires an IMISE account and your SSH public key registered with both the star and the bruchtal server.

Add the following to your `.ssh/config`:

    Host star
    Hostname star.imise.uni-leipzig.de
    User myusername

    Host hitotunnel                                                                                                                                               
    Hostname 139.18.158.56
    ProxyJump  star
    LocalForward 5432 localhost:5433
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h:%p
    User snik

Create the directory `~/.ssh/sockets` if it doesn't exist.

### Open the Tunnel

    $ ssh -fN hitotunnel

### Close the Tunnel
If you need to free the port or you want to reopen the tunnel, close the tunnel:

    $ ssh -S ~/.ssh/sockets/snik@139.18.158.56:22 -O exit hitotunnel

##  Setup

Run `source init` or the following commands: 

    $ echo "PASSWORD = 'inserthitodatabasepasswordhere' > private.py"
    $ python -m venv venv
    $ . venv/bin/activate
    (venv) $ pip install -r requirements.txt
    (venv) $ deactivate
    $. venv/bin/activate
    (venv) $ export FLASK_APP=app
    (venv) $ export HITO_DATABASE_HOST=myhost       # defaults to localhost
    (venv) $ export HITO_DATABASE_PORT=myport       # defaults to 5432
    (venv) $ export HITO_DATABASE_PASSWORD=insertpasswordhere

    (venv) $ flask fab create-admin

## Run
    $ . venv/bin/activate
    (venv) $ flask run
