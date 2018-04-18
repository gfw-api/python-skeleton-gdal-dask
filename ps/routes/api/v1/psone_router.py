"""API ROUTER"""

import logging
import json

import dask
from flask import request, jsonify, Blueprint

import ps.micro_functions.poly_intersect as analysis_funcs

psone_endpoints = Blueprint('psone_endpoints', __name__)


@psone_endpoints.route('/dissolve', strict_slashes=False, methods=['POST'])
def say_hello():
    geojson = request.json['geojson']
    geojson = json.dumps(geojson) if isinstance(geojson, dict) else geojson

    graph = {"aoi": ["geojson", geojson],
             "aoi-dissolved": ["dissolve", "aoi"],
             "dissolved-geom": ["split", "aoi-dissolved"],
             "aoi-prj": ["project_local", "dissolved-geom"],
             "aoi-area": ["get_area", "aoi-prj"]}

    graph = create_dag_from_json(graph)
    outputs = ['dissolved-geom', 'aoi-area']
    results = dask.get(graph, outputs)

    final_output = {}

    for result, name in zip(results, outputs):
        if isinstance(result, dict) and 'features' in result.keys():
            final_output[name] = analysis_funcs.ogr2json(result)
        else:
            final_output[name] = result

    return jsonify(final_output), 200



def create_dag_from_json(graph_obj):

    graph = dict()

    for k, v in graph_obj.items():

        func_name = v[0]
        func_args = v[1:] if len(v) else []

        if func_name == 'geojson':
            graph[k] = tuple([analysis_funcs.json2ogr] + func_args)
        else:
            graph[k] = tuple([getattr(analysis_funcs, func_name)] + func_args)

    return graph
