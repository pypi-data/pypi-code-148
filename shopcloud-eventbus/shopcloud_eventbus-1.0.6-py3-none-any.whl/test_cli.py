from .events import Event


def test_lib():
    event = Event(
        name="de.talk-point.platform/module/model/sync",
        model=None,
    )
    event.add_task(
        queue="default",
        url="module/api/model/1/action/",
        json={}
    )
    event.fire()
