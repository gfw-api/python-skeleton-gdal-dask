# python-skeleton-gdal-dask

This endpoint performs the full suite of Blue Raster's dissolve calculations. This uses a Directed Acyclic Graph (DAG) to execute various geometry operations - splitting the geometry in single parts, dissolving it by attributes, etc. The python library dask is used to compute these DAGs. I'm unclear if this uses additional CPU compared to a more linear process; hopefully this test will help us make that determination.


### Endpoint
Please send POST requests to: /v1/test-gdal-dask/dissolve

### Payload
The payload must be in the following format:

{"geojson": <feature collection>}

For initial testing, please use this feature collection: https://gist.github.com/mappingvermont/3980b2e096b9aac91e7f7636549c6228

### Development
1. Run the ps.sh shell script in development mode.

```ssh
./ps.sh develop
```
