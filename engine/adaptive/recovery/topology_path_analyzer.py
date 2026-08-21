"""
Topology Path Analyzer

Builds a graph from OpenSDNLab inventory links
and discovers available paths between nodes.

No external dependencies are required.
"""


class TopologyPathAnalyzer:


    def build_graph(
        self,
        links
    ):

        graph = {}


        for link in links:

            source = link.source
            destination = link.destination


            graph.setdefault(
                source,
                set()
            ).add(
                destination
            )


            graph.setdefault(
                destination,
                set()
            ).add(
                source
            )


        return graph


    def find_all_paths(
        self,
        graph,
        source,
        destination,
        max_paths=10
    ):

        paths = []


        def search(
            current,
            path
        ):

            if len(paths) >= max_paths:

                return


            if current == destination:

                paths.append(
                    list(path)
                )

                return


            for neighbor in graph.get(
                current,
                []
            ):

                if neighbor in path:

                    continue


                search(
                    neighbor,
                    path + [neighbor]
                )


        if source not in graph:

            return paths


        if destination not in graph:

            return paths


        search(
            source,
            [source]
        )


        return paths


    def analyze(
        self,
        links,
        source,
        destination
    ):

        graph = self.build_graph(
            links
        )

        paths = self.find_all_paths(
            graph,
            source,
            destination
        )


        return {

            "source":
                source,

            "destination":
                destination,

            "paths":
                paths,

            "path_count":
                len(paths),

            "alternative_path_available":
                len(paths) > 1

        }
