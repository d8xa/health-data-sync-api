[comment]: # (mention that this is one component of a bigger project, once repos for other components and )

# Health Data Sync API

A REST API for uploading health data from iOS devices, using the iOS app [HealthAutoExport](https://www.healthyapps.dev/).

[comment]: # (TODO: badges for build | tests | etc.)


## Description

The API is a Flask app in a Docker container. It was developed for use in the local network, but it should take minimal effort to make the changes required to host it on a domain.


## Installation

1. Clone the repo.
2. Ensure credentials file `credentials.json` is present in the top level directory (see section [Authentication](#Authentication) for more info).
3. (Optional) Customize `docker-compose.yml`.
4. Run 

```bash
sh docker-rebuild.sh
```

or use you own command and your own `docker-compose.yml`.

When using the supplied `docker-compose.yml` and `docker-rebuild.sh`, ensure the following:

* That files `.env` and `.env.prod` are present.
* That `.env` contains environment variable `SAVE_DIR`.


### Environment variables

* `UPLOAD_DIR` (default: `/output`) the output directory inside the container where data is saved to. This value should not be modified when using the Docker container. It's only useful when using the Flask app outside of Docker.  

* `SAVE_DIR` (default: `/output`): the output directory outside the container, to which `/output` is bound to.

* Flask settings such as `MAX_CONTENT_LENGTH` can be set as environment variables, either directly, or in `.env.prod` file.


### Authentication

The app uses HTTP basic auth, i.e. username and password, which are stored encoded in a file `credentials.json` in the project directory.

Example

username: `"dummy-user"`
password: `"dummy-password"`

credentials.json:
```json
{
    "dummy-user": <token>
}
```
where token 

```python
token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
```


### License

This project is licensed under the MIT License.