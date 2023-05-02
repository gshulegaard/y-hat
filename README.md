# y-hat

For portability, some docker containers are provided.  With `docker`,
`docker-compose`, and `make` available you should be able to build the
containers with:

``` bash
make docker-build
```

There is a dev container that is provided for running tests:

``` bash
$ make docker
(container) $ pytest tests/
```


There is also an api development image that will start the api server in
container and bind to port `8000`:

``` bash
$ make api
```

A docker network is not specified, so the local system's default docker network
will be used.  You should be able to find the address using `docker ps` and
`docker inspect [container]`.

Openapi docs are available at `<docker_network_ip>:8000/docs`.  For sanity
checking, you can try to hit the ping endpoint at
`<docker_network_ip>:8000/ping`.


An example curl against the schedule endpoint:

``` bash
curl -X POST 172.23.0.3:8000/amortization/schedule \
   -H 'Content-Type: application/json' \
   -d '{"initial_principal":100000.00,"rate":5.000, "n": 120}'
```

Replace `172.23.0.3` with docker network IP assigned on your system.
