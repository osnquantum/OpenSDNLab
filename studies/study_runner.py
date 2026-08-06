"""
Study Runner
"""


class StudyRunner:

    ############################################################

    def run(self, study):

        results = []

        print()

        print("=" * 70)
        print(study.title)
        print("=" * 70)

        for analysis in study.analyses:

            print()

            print("Running Analysis:", analysis["name"])

            result = analysis["runner"]()

            results.append(result)

        return results
