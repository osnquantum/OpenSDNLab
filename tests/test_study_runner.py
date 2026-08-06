from studies.study import Study
from studies.study_runner import StudyRunner


def delay_analysis():

    print("Delay analysis completed.")

    return {

        "analysis":"Delay",

        "status":"SUCCESS"

    }


def bandwidth_analysis():

    print("Bandwidth analysis completed.")

    return {

        "analysis":"Bandwidth",

        "status":"SUCCESS"

    }


study = Study(

    title="QoS Study",

    description="Compare major QoS parameters."

)

study.analyses.append(

    {

        "name":"Delay Analysis",

        "runner":delay_analysis

    }

)

study.analyses.append(

    {

        "name":"Bandwidth Analysis",

        "runner":bandwidth_analysis

    }

)

runner = StudyRunner()

results = runner.run(study)

print()

print(results)
