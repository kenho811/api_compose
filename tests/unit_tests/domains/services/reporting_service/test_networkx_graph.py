from pathlib import Path

import networkx as nx

from api_compose.services.reporting_service.utils.plots import dump_actions_digraph


def test_can_dump_actions_graph(
        tmp_path: Path,
):
    digraph = nx.DiGraph(
        [
            ('a', 'b'),
            ('b', 'c'),
            ('d', 'c')
        ]
    )
    dump_file_path = tmp_path.joinpath('graph.jpeg')
    dump_actions_digraph(digraph, dump_file_path)
    assert dump_file_path.is_file()
