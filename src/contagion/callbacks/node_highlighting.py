from dash import Input, Output, State, ctx, no_update

from contagion.app import app as myapp
from contagion.dash_logger import logger

FADE_RULES = [
    {"selector": "node", "style": {"opacity": 0.2}},
    {"selector": "edge", "style": {"opacity": 0.1}},
]


@myapp.callback(
    Output("cytoscape", "stylesheet", allow_duplicate=True),
    Output("highlighted-node", "data", allow_duplicate=True),
    Input("cytoscape", "tapNode"),
    Input("cytoscape", "selectedNodeData"),
    State("highlighted-node", "data"),
    State("base-stylesheet", "data"),
    prevent_initial_call=True,
)
def node_click_highlight(node, selected, current_id, base):
    base = base or []
    triggered = {t["prop_id"] for t in ctx.triggered}

    if "cytoscape.tapNode" in triggered:
        node_id = node["data"]["id"]
        logger.info(f"Node click highlighted: {node_id}")
        if node_id == current_id:  # same node -> reset
            return base, None
        return build_highlight_stylesheet(node, base), node_id

    if not selected and current_id is not None:  # background click -> reset
        return base, None

    return no_update, no_update


def build_highlight_stylesheet(node, base):
    node_id = node["data"]["id"]
    neighbor_ids, edge_ids = set(), []
    for edge in node.get("edgesData", []):
        edge_ids.append(edge["id"])
        neighbor_ids.update((edge["source"], edge["target"]))
    neighbor_ids.discard(node_id)

    stylesheet = base + FADE_RULES + [
        {"selector": f'node[id = "{node_id}"]',
         "style": {"opacity": 1, "border-width": 4, "border-color": "#000",
                   "underlay-color": "#ffd60a",
                   "underlay-padding": 8,
                   "underlay-opacity": 0.6,
                   "underlay-shape": node['data']['shape']}},
    ]
    stylesheet += [
        {"selector": f'node[id = "{nid}"]',
         "style": {"opacity": 1, "border-width": 2, "border-color": "#555"}}
        for nid in neighbor_ids
    ]
    stylesheet += [
        {"selector": f'edge[id = "{eid}"]', "style": {"opacity": 1, "width": 3}}
        for eid in edge_ids
    ]
    return stylesheet
