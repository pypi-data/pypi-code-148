"""
Personal tracker for your personal website.

Track your physical movement: GPS locations and trip circuits (eg. Overland)

Track your web movement: webpage visits (eg. Liana)

"""

import web

app = web.application(
    __name__,
    prefix="tracker",
    args={"start": r".*"},
    model={
        "locations": {
            "location": "JSON",
        },
        "trips": {
            "start": "DATETIME",
            "distance": "TEXT",
            "location": "JSON",
        },
        "web": {
            "location": "JSON",
        },
    },
)


@app.control("")
class Tracker:
    """"""

    owner_only = ["get"]

    def get(self):
        """"""
        return app.view.index(app.model.get_trips())


@app.control("physical")
class Physical:
    """"""

    owner_only = ["get"]

    def get(self):
        """"""
        return app.view.physical(app.model.get_locations(), app.model.get_trips())

    def post(self):
        """"""
        for location in web.tx.request.body["locations"]:
            app.model.add_location(location)
        if trip := web.tx.request.body.get("trip"):
            app.model.add_trip_location(trip)
        return {"result": "ok"}


@app.control("physical/trips/{start}")
class Trip:
    """"""

    owner_only = ["get"]

    def get(self, start):
        """"""
        if not web.tx.user.session:
            raise web.NotFound("nothing to see here.")
        return app.view.trip(app.model.get_trip(start))


@app.control(r"web")
class Web:
    """"""

    owner_only = ["get", "post"]

    def get(self):
        """"""
        if not web.tx.user.session:
            raise web.NotFound("nothing to see here.")
        return app.view.web(app.model.get_web_locations())

    def post(self):
        """"""
        app.model.add_web_location(web.tx.request.body["location"])
        return {"result": "ok"}


@app.query
def add_location(db, location):
    db.insert("locations", location=location)


@app.query
def get_locations(db):
    return db.select("locations")[::100]


@app.query
def add_trip_location(db, location):
    db.insert(
        "trips",
        start=location["start"],
        distance=location["distance"],
        location=location,
    )


@app.query
def get_trips(db):
    return db.select("trips", group="start")


@app.query
def get_trip(db, start):
    return db.select(
        "trips",
        where="start = ?",
        vals=[str(start).replace("+00:00", "Z")],
        order="distance ASC",
    )


@app.query
def add_web_location(db, location):
    db.insert("web", location=location)


@app.query
def get_web_locations(db):
    return db.select("web")
