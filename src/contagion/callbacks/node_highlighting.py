from dash import Input, Output, State, ctx, no_update

from contagion.app import app as myapp
from contagion.dash_logger import logger


@myapp.callback(
    Output("highlighted-node", "data", allow_duplicate=True),
    Input("cytoscape", "tapNode"),
    Input("cytoscape", "selectedNodeData"),
    State("highlighted-node", "data"),
    prevent_initial_call=True,
)
def node_click_highlight(node, selected, current_id):
    triggered = {t["prop_id"] for t in ctx.triggered}

    if "cytoscape.tapNode" in triggered:
        node_id = node["data"]["id"]
        logger.info(f"Node click highlighted: {node_id}")
        return None if node_id == current_id else node_id

    if not selected and current_id is not None:
        return None

    return no_update


def build_highlight_stylesheet(node, base):
    node_id = node["data"]["id"]
    neighbor_ids, edge_ids = set(), []
    for edge in node.get("edgesData", []):
        edge_ids.append(edge["id"])
        neighbor_ids.update((edge["source"], edge["target"]))
    neighbor_ids.discard(node_id)

    stylesheet = base + [
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
