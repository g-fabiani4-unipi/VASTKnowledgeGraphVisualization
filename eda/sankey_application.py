import argparse
import json
from pathlib import Path

import networkx as nx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html


def parse_args():
    parser = argparse.ArgumentParser(
        description=('Visualize sankey diagram for knowledge graph data.'),
    )
    parser.add_argument(
        'file',
        type=Path,
        help='Json file encoding the knowledge graph',
    )
    parser.add_argument(
        '--nodes',
        default='nodes',
        type=str,
        help='String identifying nodes',
    )
    parser.add_argument(
        '--edges',
        default='edges',
        type=str,
        help='String identifying edges',
    )
    parser.add_argument(
        '--node_type',
        default='type',
        type=str,
        help='String identifying the attribute that contains the node type',
    )

    parser.add_argument(
        '--edge_type',
        default='type',
        type=str,
        help='String identifying the attribute that contains the edge type',
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debugging of dash application',
    )
    return parser.parse_args()


def preprocess_data(data_path, edges, nodes, edge_type, node_type):
    """Export edge data from graph in pandas dataframe."""
    try:
        with open(data_path) as file:
            data = json.load(file)
    except OSError as e:
        print(e)
        return None

    graph = nx.node_link_graph(
        data,
        nodes=nodes,
        edges=edges,
    )

    edge_list = []
    for source, target, data in graph.edges(data=True):
        edge_list.append(
            {
                'source_type': graph.nodes[source].get(node_type, pd.NA),
                'edge_type': data.get(edge_type, pd.NA) if data else pd.NA,
                'target_type': graph.nodes[target].get(node_type, pd.NA),
            },
        )
    edges_df = pd.DataFrame(edge_list)
    node_types = (set(edges_df.source_type.dropna().unique())
    | set(edges_df.target_type.dropna().unique()))
    colorscale = dict(zip(sorted(node_types), px.colors.qualitative.D3, strict=False))
    edges_df = edges_df.fillna('NA')
    edges_df['source_color'] = edges_df.source_type.map(colorscale)
    edges_df['target_color'] = edges_df.target_type.map(colorscale)

    return edges_df


def create_app(data):
    """Create dash application from dataframe."""
    app = Dash()

    app.layout = [
        html.Div(
            [
                html.Label(
                    children=[
                        'Color by:',
                        dcc.RadioItems(
                            options=['source', 'target', 'none'],
                            value='source',
                            inline=True,
                            id='radio',
                        ),
                    ],
                ),
                html.Br(),
                html.Label(
                    children=[
                        'Edge type:',
                        dcc.Dropdown(
                            options=data.edge_type.value_counts().index, id='dropdown',
                        ),
                    ],
                ),
                dcc.Graph(id='graph'),
            ],
            # limit width and center horizontally
            style={'padding': 25,
                   'max-width': '800px',
                   'margin': 'auto'},
        ),
    ]

    @callback(
        Output(component_id='graph', component_property='figure'),
        Input(component_id='radio', component_property='value'),
        Input(component_id='dropdown', component_property='value'),
    )
    def update_graph(color, edge_type):
        """Create sankey plot."""
        filtered_data = data[data.edge_type == edge_type] if edge_type else data
        color = None if color == 'none' else filtered_data[f'{color}_color']

        source_dim = go.parcats.Dimension(
            values=filtered_data.source_type,
            label='Source type',
        )

        target_dim = go.parcats.Dimension(
            values=filtered_data.target_type,
            label='Target type',
        )
        fig = go.Figure(
            data=[
                go.Parcats(
                    dimensions=[source_dim, target_dim],
                    line={'color': color, 'shape': 'hspline'},
                ),
            ],
        )
        return fig

    return app


def main():
    args = parse_args()
    data = preprocess_data(
        args.file, args.edges, args.nodes, args.edge_type, args.node_type,
    )
    if data is not None:
        app = create_app(data)
        app.run(debug=args.debug)
    else:
        return


if __name__ == '__main__':
    main()
