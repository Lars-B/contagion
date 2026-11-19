from dash import Input, Output, State

from contagion.app import app as myapp
from contagion.callbacks import build_highlight_stylesheet
from contagion.dash_logger import logger


@myapp.callback(
    Output("search-matches", "data"),
    Input("node-search", "value"),
    Input("graph-store", "data"),
    Input("cytoscape", "elements"),
    prevent_initial_call=True,
)
def search_nodes(query, graph_data, elements):
    if not query or not graph_data:
        return []

    nodes = graph_data.get("nodes", [])

    # node ids currently rendered (excludes filtered / suppressed nodes)
    displayed_ids = {
        el["data"]["id"]
        for el in (elements or [])
        if "source" not in el["data"]
    }

    logger.debug(f'we are here {displayed_ids}')

    matches = []
    for node in nodes:
        node_info = node.get("data", ())
        # todo could have different categories of matches, ones with partial others with full matches?
        for label in node_info:
            added = False
            if query in node_info[label] or query == node_info[label]:
                # todo some more detail on how to match things in here...
                matches.append(node_info.get('id', None))
                added = True
            if added:
                break
    logger.info(f'we found {len(matches)} matches, they are {matches}')
    return matches


def build_search_rules(node_ids):
    return [
        {"selector": f'node[id = "{nid}"]',
         "style": {"opacity": 1,
                   "underlay-color": "#00b4d8",
                   "underlay-padding": 8,
                   "underlay-opacity": 0.6}}
        for nid in node_ids
    ]


FADE_RULES = [
    {"selector": "node", "style": {"opacity": 0.2}},
    {"selector": "edge", "style": {"opacity": 0.1}},
]


@myapp.callback(
    Output("cytoscape", "stylesheet", allow_duplicate=True),
    Input("base-stylesheet", "data"),
    Input("highlighted-node", "data"),
    Input("search-matches", "data"),
    State("cytoscape", "tapNode"),
    prevent_initial_call=True,
)
def render_highlights(base, clicked_id, search_ids, tap_node):
    stylesheet = list(base or [])
    if not clicked_id and not search_ids:
        return stylesheet

    stylesheet += FADE_RULES
    if search_ids:
        stylesheet += build_search_rules(search_ids)
    if clicked_id and tap_node and tap_node["data"]["id"] == clicked_id:
        # todo this might need to be configurable
        stylesheet += build_highlight_stylesheet(tap_node, [])  # click on top
    return stylesheet
