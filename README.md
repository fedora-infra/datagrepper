# datagrepper

Datagrepper is a web application and JSON API to retrieve historical messages sent via Fedora Messaging. [Datanommer](https://github.com/fedora-infra/datanommer/) is a seperate project and service that consumes messages from the Fedora Messaging queue and puts them in a database. These messages is what datagrepper queries. 

Datagrepper is curently running in production at https://apps.fedoraproject.org/datagrepper/

## Development Environment

Vagrant allows contributors to get quickly up and running with a datagrepper development environment by automatically configuring a virtual machine. 

The datagrepper Vagrant environment configures configures and enables a datanommer service and database. The datanommer instance is configured to be empty when first provisioned, but to consume messages from the stage Fedora Messaging queue.

### Install vagrant
To get started, run the following commands to install the Vagrant and Virtualization packages needed, and start the libvirt service:

    $ sudo dnf install ansible libvirt vagrant-libvirt vagrant-sshfs vagrant-hostmanager
    $ sudo systemctl enable libvirtd
    $ sudo systemctl start libvirtd

### Checkout and Provision
Next, check out the datagrepper code and run vagrant up:

    $ git clone https://github.com/fedora-infra/datagrepper
    $ cd datanommer
    $ vagrant up

### Interacting with your development datagrepper
After successful provisioning of the Datagrepper vagrant setup, the datagrepper web application will be accessible from your host machine's web browser at

http://datagrepper.test:5000/




### Using the development environment
SSH into your newly provisioned development environment:

    $ vagrant ssh

The vagrant setup also defines 4 handy commands to interact with the service that runs the datagrepper flask application: 

    $ datagrepper-start
    $ datagrepper-stop
    $ datagrepper-restart
    $ dataprepper-logs

Additionally, the following commands are also available for interacting with the datanommer service:

    $ datanommer-consumer-start
    $ datanommer-consumer-stop
    $ datanommer-consumer-restart
    $ datanommer-consumer-logs

### Running the tests
Datanommer is comprised of 3 seperate modules in this single repository. There is a handy script in the top directory of this repo to run the tests on all 3 modules:

    $ ./runtests.sh

However, tests can also be run on a single module by invotking tox in that modules' directory. For example:

    $ cd datanommer.models/
    $ tox

Note, that the tests use virtual environments that are not created from scratch with every subsequent run of the tests. Therefore, **when changes happen to dependencies, the tests may fail to run correctly**. To recreate the virtual envrionments,  run the tests commands with the `-r` flag, for example:

    $ ./runtests.sh -r

or

    $ cd datanommer.models/
    $ tox -r
