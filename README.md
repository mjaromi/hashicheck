# hashicheck

## Description

`hashicheck` is a service to provide version information for various HashiCorp products.

It allows you to check latest version of HashiCorp products.

All products listed on the `https://releases.hashicorp.com` are supported.

## Why?

As an official HashiCorp Checkpoint service (https://checkpoint.hashicorp.com/) does not provide version information for various products I've decided to write this service which solve that problem.

## Build

```bash
git clone https://github.com/mjaromi/hashicheck.git
cd hashicheck
docker build -t hashicheck:latest .
docker run -dit -p80:80 hashicheck:latest
```

## Endpoints

* `/` list all products
* `/<product>/` list available versions for provided `product`
* `/<product>/<version>/` list available files for provided `product` and `version`
* `/<product>/latest/` show latest version for provided `product` (exclude 'ent', 'beta, 'rc')
* `/<product>/latest/ent` show latest enterprise version for provided `product` (exclude 'beta, 'rc')

## Waypoint

```
waypoint install -platform=docker -accept-tos
waypoint init
waypoint up
```
