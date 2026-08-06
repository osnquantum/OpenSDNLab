from core.event_bus import event_bus
import core.events as events


def experiment_started(data):

    print("Experiment Started")

    print(data)


event_bus.subscribe(

    events.EXPERIMENT_STARTED,

    experiment_started

)

event_bus.publish(

    events.EXPERIMENT_STARTED,

    {

        "name":"Demo",

        "topology":"linear"

    }

)
