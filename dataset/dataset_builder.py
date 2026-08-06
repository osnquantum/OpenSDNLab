"""
Dataset Builder
"""

from dataset.dataset import Dataset


class DatasetBuilder:

    ############################################################

    def build(

        self,

        experiment_results,

        name="Experiment Dataset"

    ):

        dataset = Dataset(

            name=name

        )

        dataset.rows.extend(

            experiment_results

        )

        dataset.metadata["total_rows"] = len(dataset.rows)

        return dataset
