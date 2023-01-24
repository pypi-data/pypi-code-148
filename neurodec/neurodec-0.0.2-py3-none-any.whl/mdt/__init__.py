from __future__ import annotations
from enum import auto, IntEnum
import numpy as np
from numpy.typing import ArrayLike
import os
import requests
import time
import trimesh
from typing import Callable, Collection, Iterable, Optional
from werkzeug.datastructures import ImmutableMultiDict

from .auth import Credentials

from .bracelet_electrodes import generate_bracelet_electrodes as generate_bracelet_electrode_centers

_API_URL = "http://0.0.0.0:8001"

wait = True


class Status(IntEnum):
    """The status of the objects in the Neurodec Myoelectric Digital Twin"""

    NEW = 0
    PENDING = auto()
    PROCESSING = auto()
    READY = auto()
    ERROR = auto()


class SurfaceType(IntEnum):
    """The surface types which are used to build a volume conductor"""

    OUTER_SKIN = 0
    INNER_SKIN = 1
    BONE = 2
    MUSCLE = 3
    ELECTRODE = 4


# Random seed to be used in new() calls when not explicitly given as parameter.
DEFAULT_RANDOM_SEED = 0


# This object is used to add authentication data to all API requests. By default, authentication credentials can be
# loaded from a file named ".credentials.txt" stored in the root of the `neurodec` repository, ie, this repository.
# Such file should contain two lines: the first one being the public key and the second one being the private key.
# As an alternative, one can create and store here a new Credentials object by passing the public and private keys.
credentials = Credentials.from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                                 ".credentials.txt"))


class MDTObject:
    """Base class for Neurodec Myoelectric Digital Twin classes"""

    _url_prefix: str = ""

    def __init__(self, dictionary: dict):
        """Initialize object from a mapping

        This function is not meant to be called directly by users. Use
        the `new` class method instead.

        """

        self._id = dictionary["id"]
        self._status = Status(dictionary["status"])
        self._data_json = None

    def __str__(self):
        """String representation of a surface"""
        return f"{self.__class__.__name__}({self._id}, {str(self._status)})"

    @property
    def id(self) -> int:
        """Returns the ID of the object"""
        return self._id

    @property
    def status(self) -> Status:
        """Returns the up-to-date status of the object, by performing an API request."""
        self._status = self._get_metadata(self._id)._status
        return self._status

    @classmethod
    def _get_metadata(cls, id: int):
        response = requests.get(f"{_API_URL}/{cls._url_prefix}/{id}/metadata", json={"credentials": credentials.get()})
        if not response.ok:
            raise ValueError("The metadata could not be retrieved.")

        return cls(response.json())

    @classmethod
    def _new_request(cls, json=None):
        if json is None:
            json = {}
        json.update({"credentials": credentials.get()})
        response = requests.post(f"{_API_URL}/{cls._url_prefix}", json=json)
        if not response.ok:
            raise ValueError(f"The {cls.__name__} could not be created.")

        # Wait the status to be READY if requested.
        obj = cls(response.json())
        if wait:
            obj.wait()

        return obj

    def wait(self):
        """Wait for the object to be ready"""

        while True:
            if self.status is Status.READY:
                break
            elif self.status is Status.ERROR:
                raise RuntimeError("An error occurred during the simulation.")

            time.sleep(1.0)

    def _retrieve_data(self):
        """Retrieve the data of this object.

        In this context, the term "data" refers to whatever is calculated by the API services that makes the object
        change its status from PENDING to READY.
        """
        # Get the raw data if we don't already have it.
        if self._data_json is None:
            # Wait for the data to be ready.
            self.wait()

            response = requests.get(f"{_API_URL}/{self._url_prefix}/{self.id}/data",
                                    json={"credentials": credentials.get()})
            if not response.ok:
                raise RuntimeError("The data of this object could not be retrieved.")
            self._data_json = response.json()

    @staticmethod
    def monitor_status(objects: Collection["MDTObject"], polling_interval: float = 5.0,
                       event_handler: Optional[Callable[["MDTObject", Status, Status], None]] = None,
                       print_function: Optional[Callable[[str], None]] = None):
        """Monitor the status of a set of objects until they are all ready.

        The function polls the API periodically until all monitored objects reach either the READY or ERROR state. In
        addition, when an object changes its state, the user is informed of the event by a message.

        Args:
            objects: A list of MDTObject instances to be monitored.
            polling_interval: Time to wait (in seconds) between subsequent API requests.
            event_handler: A function object to handle status changes. It should accept the object that just changed
                its status, the old status and the new status. If not given, a default handler is used, which creates
                a message every time an object changes its status to READY or to ERROR. The message is then passed to
                the function "print_function".
            print_function: Function to be called when an object changes its state and therefore the user need to be
                notified. The function should accept a string (the message to be shown to the user). By default, the
                'print' function is used. You can instead pass, eg, the "info" method of a logger instance, or a
                function that sends a notification to your phone to let you know that the resource is ready. This
                parameter is ignored if a custom event_handler is used instead.
        """
        for i, obj in enumerate(objects):
            if not isinstance(obj, MDTObject):
                raise ValueError(f"Object at index {i} is not of type MDTObject (type: {type(obj).__name__}).")

        # Make a copy of the array, so that we can modify it as needed.
        objects = [o for o in objects]

        # Get the last known status of each object.
        statuses = [o._status for o in objects]

        # States that make the resource drop from the list of objects of interest.
        exit_states = [Status.READY, Status.ERROR]

        # If the event handler is not given, create a default one.
        if event_handler is None:
            # If the print function is not given, fall back to console printing.
            if print_function is None:
                print_function = print

            def event_handler(obj, old_status, new_status):
                # A human-readable string that identifies the resource.
                source = f"{type(obj).__name__}[id={obj.id}]"

                # If the object is now ready or if there was an error, send a message to the user.
                if new_status == Status.READY:
                    msg = f"\a{source} was processed and is now ready!"
                elif new_status == Status.ERROR:
                    msg = f"\aThere was an error while processing {source}."
                else:
                    msg = None

                # If needed, notify the user.
                if msg is not None:
                    print_function(msg)

        while len(objects) > 0:
            # Wait for some time to reduce the traffic.
            time.sleep(polling_interval)

            # For each object, check it they have changed status. If so, handle the change.
            for obj, status in zip(objects, statuses):
                if obj.status != status:
                    event_handler(obj, Status(status), Status(obj._status))

            # Update the list of monitored objects and their states.
            objects = [o for o in objects if o._status not in exit_states]
            statuses = [o._status for o in objects]


class Surface(MDTObject):
    """A surface of an anatomical model"""

    _url_prefix: str = "surfaces"

    def __init__(self, dictionary: dict):
        """Initialize surface from a mapping

        This function is not meant to be called directly by users. Use
        Surface.new instead.

        """

        super().__init__(dictionary)
        self._type = SurfaceType(dictionary["type"])
        self._label = None
        self._vertices = None
        self._triangles = None

    def __str__(self):
        """String representation of a surface"""
        return f"Surface({self._id}, {str(self._status)}, {str(self._type)})"

    @property
    def type(self) -> SurfaceType:
        """Returns the type of the surface"""
        return self._type

    @classmethod
    def new(cls, vertices: ArrayLike, triangles: ArrayLike, surface_type: SurfaceType, label: Optional[str] = None,
            force_computation: bool = False) -> Surface:
        """Create a new surface

        Creates a new surface from raw data. This will initiate a call to the
        Neurodec Myoelectric Digital Twin (MDT) API that will save the surface,
        preprocess it, and return its metadata in the form of a dict.

        Args:
            vertices: A numpy array of float with a shape of (N, 3) that
                contains the location of the vertices.
            triangles: A numpy array of unsigned integers with a shape of
                (M, 3) that contains the indices of the vertices for each
                triangle.
            surface_type: The surface type, see neurodec.mdt.SurfaceType.
            label: A human-readable name to easily identify the surface. If not given, the label will be autogenerated
                from the surface type. Note that this label exists only locally and not in the database. This means that
                if two Surface objects are created with different labels but with same vertices, triangles and types,
                the result will be two instances that share the same id and status, despite having different labels.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The new surface. If another surfaces with the same parameters already exits, that one will be returned
            instead of creating a new surface.
        """

        # Make sure the vertices can be converted to a numpy array of (N, 3).
        vertices = np.array(vertices, dtype=np.float64)
        if vertices.ndim != 2 or vertices.shape[1] != 3:
            raise ValueError(
                "The vertices must be a 2D array of floats with a shape of (N, 3), not"
                f" {vertices.shape}."
            )

        # Same thing for the triangles.
        triangles = np.array(triangles, dtype=np.uint64)
        if triangles.ndim != 2 or triangles.shape[1] != 3:
            raise ValueError(
                "The triangles must be a 2D array of unsigned integers with a shape of"
                f" (M, 3), not {triangles.shape}."
            )

        # Avoid unused vertices and out of bounds triangle indices.
        indices = np.unique(triangles)
        if indices.max() >= len(vertices):
            raise ValueError(
                "The triangle indices is equal to or exceed the number of vertices"
                f" ({indices.max()} vs {len(vertices)})."
            )

        # Encode the vertices and triangles.
        data = {
            "force_computation": force_computation,
            "type": surface_type.value,
        }
        data.update(_encode_array(vertices, "vertices"))
        data.update(_encode_array(triangles, "triangles"))

        surface = cls._new_request(json={"surface": data})
        surface._vertices = vertices
        surface._triangles = triangles
        surface._label = label if label is not None else f"{surface_type.name.lower}_{surface.id}"
        return surface

    @property
    def vertices(self):
        return self._vertices.copy()

    @property
    def triangles(self):
        return self._triangles.copy()

    @property
    def label(self) -> str:
        """Returns the label of this Surface"""
        return self._label


class Conductor(MDTObject):
    """A volume conductor"""

    _url_prefix: str = "conductor"

    @classmethod
    def new(cls, surfaces: Iterable[Surface], force_computation: bool = False) -> Conductor:
        """Create a new volume conductor

        Creates a new volume conductor from surfaces. This will initiate a call
        to the Neurodec Myoelectric Digital Twin (MDT) API that will build
        the conductor and return its metadata in the form of a dict.

        Args:
            surfaces: The surfaces used to define the volume conductor. Must
                contain at least one OUTER_SKIN surface and one INNER_SKIN
                surface.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The metadata of the new conductor. If another conductor with the
            same parameters already exits, that one will be returned instead of
            building a new one.

        """

        # Encode the surfaces.
        json = {
            "force_computation": force_computation,
            "surfaces": [s.id for s in surfaces],
        }

        return cls._new_request(json=json)


class Electrode(MDTObject):
    """An electrode"""

    _url_prefix: str = "electrodes"

    def __init__(self, dictionary: dict):
        """Initialize surface from a mapping

        This function is not meant to be called directly by users. Use
        Surface.new instead.

        """

        super().__init__(dictionary)
        self._radius = dictionary["radius"]
        self._location = np.array(dictionary["location"])

    @classmethod
    def new(
            cls,
            location: ArrayLike,
            radius: float,
            force_computation: bool = False
    ) -> Electrode:
        """Create a circular electrode.

        Args:
            location: NumPy array with shape (3,) containing the 3D coordinates of the electrode.
            radius: Radius of the electrode.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The metadata of the new electrode. If another electrode with the same parameters already exists, it will be
            returned instead of building a new one.
        """
        # Encode the parameters.
        json = {
            "force_computation": force_computation,
            "radius": radius
        }
        json.update(_encode_array(location, "location"))

        # Send the request.
        return cls._new_request(json=json)

    @property
    def radius(self):
        return self._radius

    @property
    def location(self):
        return self._location.copy()


def generate_bracelet_electrodes(skin: Surface,
                                 radius: float,
                                 first_electrode_location: ArrayLike,
                                 rings_normal: ArrayLike,
                                 n_rings: int,
                                 distance_between_rings: float,
                                 n_electrodes_per_ring: int,
                                 distance_between_electrodes: Optional[float] = None):
    """Generate a bracelet of electrodes on the given surface.

    A bracelet is a series of electrodes arranged in multiple rings that should wrap around the given surface.

    Args:
        skin: A Surface object with type OUTER_SKIN where the electrodes will be placed.
        radius: Radius of an electrode. The same value is used for all electrodes in the bracelet.
        first_electrode_location: A numpy array containing 3D coordinates of the first electrode of the first ring.
            Does not have to be precisely on the skin mesh - the point will be projected onto it.
        rings_normal: A numpy array containing the direction of the normal vector defining the bracelet section planes.
            Note, that all the rings have the same normal vector.
        n_rings: The number of electrode rings in the bracelet. If larger than 1, the initial bracelet plan is shifted
            in the direction of the normal vector for a distance distance_between_rings.
        distance_between_rings: Distance between electrode rings in the bracelet, in meters. Note, that all the rings
            are equidistant.
        n_electrodes_per_ring: The number of electrodes in rings. The electrodes are ordered in a clockwise direction
            with respect to the rings_normal. If the distance_between_rings parameter is 0, all the rings will have the
            same number of electrodes uniformly covering the corresponding section circumferences. It will likely
            result in different inter electrode distances for different rings.
        distance_between_electrodes: The distance between electrodes in a ring, in meters. If not None, will generate
            equidistant in a clockwise direction starting from the first_electrode_location.
    """
    # Make sure the surface is indeed the skin.
    if skin.type != SurfaceType.OUTER_SKIN:
        raise ValueError(f"The provided Surface object shouild be of type 'OUTER_SKIN', not '{skin.type.name}'.")
    centers = generate_bracelet_electrode_centers(trimesh.Trimesh(vertices=skin.vertices, faces=skin.triangles),
                                                  first_electrode_location,
                                                  rings_normal,
                                                  n_rings,
                                                  distance_between_rings,
                                                  n_electrodes_per_ring,
                                                  distance_between_electrodes
                                                  ).reshape(-1, 3)
    # For each electrode center, create a new electrode and save it into a list that is returned to the user.
    electrodes = []
    for c in centers:
        new_electrode = Electrode.new(c, radius)
        if wait:
            new_electrode.wait()
        electrodes.append(new_electrode)
    return electrodes


class ForwardSolution(MDTObject):
    """A forward solution"""

    _url_prefix: str = "forward"

    @classmethod
    def new(
            cls,
            conductor: Conductor,
            electrodes: Collection[Electrode],
            force_computation: bool = False
    ) -> ForwardSolution:
        """Create a new forward solution

        Creates a new forward solution from a volume conductor and electrodes. This
        will initiate a call to the Neurodec Myoelectric Digital Twin (MDT) API that
        will build the forward solution and return its metadata.

        Args:
            conductor: The conductor for which we compute the forward solution.
            electrodes: The electrodes used to record EMGs.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The metadata of the new forward solution. If another forward solution with
            the same parameters already exits, that one will be returned instead of
            building a new one.

        """
        json = {
            "force_computation": force_computation,
            "conductor_id": conductor.id,
            "electrode_ids": [e.id for e in electrodes]
        }

        return cls._new_request(json=json)


class Fibers(MDTObject):
    """The fibers of a muscle"""

    _url_prefix: str = "fibers"

    def __init__(self, dictionary: dict):
        """Initialize fibers from a mapping

        This function is not meant to be called directly by users. Use Fibers.new() instead.
        """
        super().__init__(dictionary)
        self._random_seed = dictionary["random_seed"]

    @property
    def random_seed(self):
        return self._random_seed

    @classmethod
    def new(
            cls,
            surface: Surface,
            plane_origins: ArrayLike,
            plane_normals: ArrayLike,
            n_fibers: Optional[int] = None,
            fibers_radius: Optional[float] = 2.8e-5,
            force_computation: bool = False,
            random_seed: int = DEFAULT_RANDOM_SEED
    ) -> Fibers:
        """Create new fibers for a muscle

        Creates new fibers from a surface. This will initiate a call
        to the Neurodec Myoelectric Digital Twin (MDT) API that will generate
        fibers and return their metadata.

        Args:
            surface: The surface for which the fibers are generated.
            plane_origins: A numpy array with a shape of (2, 3) that defines
                the origins of the planes where fibers start and end.
            plane_normals: A numpy array with a shape of (2, 3) that defines
                the normals of the planes where fibers start and end.
            n_fibers: number of fibers to be generated in the muscle. It cannot
                be given if fibers_radius is given as well.
            fibers_radius: radius of the fibers. If n_fibers is None, the
                number of fibers is calculated from this parameter. If n_fibers
                and this parameter are both None, a default radius is used.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.
            random_seed: A specific random seed to be used for the calculations. Changing the seed allows to create
                multiple instances from the same parameters.
        Returns:
            The metadata of the new fibers. If another set of fibers with the
            same parameters already exits, those will be returned instead of
            building new ones.

        """

        # Convert the planes to numpy arrays and verify the shape.
        plane_origins = np.array(plane_origins, dtype=np.float)
        if plane_origins.shape != (2, 3):
            raise ValueError(
                "The plane origins must be a 2D array of floats with a shape of (2, 3),"
                f" not {plane_origins.shape}."
            )
        plane_normals = np.array(plane_normals, dtype=np.float)
        if plane_normals.shape != (2, 3):
            raise ValueError(
                "The plane normals must be a 2D array of floats with a shape of (2, 3),"
                f" not {plane_normals.shape}."
            )

        json = {
            "force_computation": force_computation,
            "surface_id": surface.id,
            "plane_origins": plane_origins.ravel().tolist(),
            "plane_normals": plane_normals.ravel().tolist(),
            "random_seed": random_seed,
        }

        if n_fibers is not None:
            json["n_fibers"] = n_fibers
        if fibers_radius is not None:
            json["fibers_radius"] = fibers_radius

        return cls._new_request(json=json)


class FiberProperties(MDTObject):
    """Properties of individual fibers"""

    _url_prefix: str = "fiber_properties"

    def __init__(self, dictionary: dict):
        """Initialize fiber properties from a mapping

        This function is not meant to be called directly by users. Use FiberProperties.new() instead.
        """
        super().__init__(dictionary)
        self._random_seed = dictionary["random_seed"]

    @property
    def random_seed(self):
        return self._random_seed

    @classmethod
    def new(cls,
            fibers: Fibers,
            neuromuscular_junction_min: float = 0.5,
            neuromuscular_junction_max: float = 0.5,
            tendon_1_ratio_min: float = 0.,
            tendon_1_ratio_max: float = 0.,
            tendon_2_ratio_min: float = 0.,
            tendon_2_ratio_max: float = 0.,
            velocity_min: float = 3.,
            velocity_max: float = 3.,
            force_computation: bool = False,
            random_seed: int = DEFAULT_RANDOM_SEED
            ) -> FiberProperties:
        """Create new fiber properties for individual fibers

        Creates new fiber properties from each fiber of a muscle. This will
        initiate a call to the Neurodec Myoelectric Digital Twin (MDT) API
        that will generate fiber properties and return their metadata.

        The input values define lower and upper bounds for each of the fiber parameters. Individual fiber properties
        will be then randomly sampled from a uniform distribution within corresponding ranges.

        Args:
            fibers: The fibers for which to generate the individual properties.
            neuromuscular_junction_min: the lower bound for the neuromuscular junction location ratio (between 0 and 1).
            neuromuscular_junction_max: the upper bound for the neuromuscular junction location ratio (between 0 and 1).
            tendon_1_ratio_min: the lower bound for the tendon 1 ratio (between 0 and 1).
            tendon_1_ratio_max: the upper bound for the tendon 1 ratio (between 0 and 1).
            tendon_2_ratio_min: the lower bound for the tendon 2 ratio (between 0 and 1).
            tendon_2_ratio_max: the upper bound for the tendon 2 ratio (between 0 and 1).
            velocity_min: the lower bound for the action potential propagation velocity, in m/s.
            velocity_max: the upper bound for the action potential propagation velocity, in m/s.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.
            random_seed: A specific random seed to be used for the calculations. Changing the seed allows to create
                multiple instances from the same parameters.

        Returns:
            The metadata of the new fiber properties. If another set of fiber
            properties with the same parameters already exits, those will be returned
            instead of building new ones.

        """

        json = {
            "neuromuscular_junction_min": neuromuscular_junction_min,
            "neuromuscular_junction_max": neuromuscular_junction_max,
            "tendon_1_ratio_min": tendon_1_ratio_min,
            "tendon_1_ratio_max": tendon_1_ratio_max,
            "tendon_2_ratio_min": tendon_2_ratio_min,
            "tendon_2_ratio_max": tendon_2_ratio_max,
            "velocity_min": velocity_min,
            "velocity_max": velocity_max,
            "force_computation": force_computation,
            "fibers_id": fibers.id,
            "random_seed": random_seed,
        }

        return cls._new_request(json=json)


class FiberBasis(MDTObject):
    """Basis (leadfields/transfer function) for the fibers of a single muscle"""

    _url_prefix: str = "fiber_basis"

    @classmethod
    def new(cls, fibers: Fibers, forward_solution: ForwardSolution, force_computation: bool = False) -> FiberBasis:
        """Create new fiber basis for a single muscle

        Creates new fiber basis for the fibers of a muscle. This will
        initiate a call to the Neurodec Myoelectric Digital Twin (MDT) API
        that will generate the fiber basis and return their metadata.

        Args:
            fibers: The fibers for which to generate the motor units.
            forward_solution: The forward solution of the volume conductor
                where the fibers live.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The metadata of the new fiber basis. If another fiber basis
            with the same parameters already exits, it will be returned
            instead of building a new one.

        """

        json = {
            "force_computation": force_computation,
            "fibers_id": fibers.id,
            "forward_solution_id": forward_solution.id,
        }

        return cls._new_request(json=json)


class MotorUnits(MDTObject):
    """Motor units of a single muscle"""

    _url_prefix: str = "motor_units"

    def __init__(self, dictionary: dict):
        """Initialize motor units from a mapping

        This function is not meant to be called directly by users. Use MotorUnits.new() instead.
        """
        super().__init__(dictionary)
        self._sizes = None
        self._random_seed = dictionary["random_seed"]

    @property
    def random_seed(self):
        return self._random_seed

    @classmethod
    def new(
            cls,
            fibers: Fibers,
            n_motor_units: int,
            area_min: float = 0.1,
            area_max: float = 0.7,
            distribution_radius: float = 0.95,
            force_computation: bool = False,
            random_seed: int = DEFAULT_RANDOM_SEED
    ) -> MotorUnits:
        """Create new motor units for a single muscle

        Creates new motor units by grouping the fibers of a muscle. This will
        initiate a call to the Neurodec Myoelectric Digital Twin (MDT) API
        that will generate motor units and return their metadata.

        Args:
            fibers: The fibers for which to generate the motor units.
            n_motor_units: The number of motor units to generate.
            area_min: The minimum area of motor units.
            area_max: The maximum area of the motor units.
            distribution_radius: The maximum radius inside a unit circle at which the motor unit centers can be created.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.
            random_seed: A specific random seed to be used for the calculations. Changing the seed allows to create
                multiple instances from the same parameters.

        Returns:
            The metadata of the new motor units. If another set of motor
            units with the same parameters already exits, those will be returned
            instead of building new ones.

        """

        json = {
            "force_computation": force_computation,
            "fibers_id": fibers.id,
            "n_motor_units": n_motor_units,
            "distribution_radius": distribution_radius,
            "area_min": area_min,
            "area_max": area_max,
            "random_seed": random_seed,
        }

        return cls._new_request(json=json)

    @property
    def sizes(self) -> ArrayLike:
        """Returns the sizes of the MUs

        Returns:
            A NumPy array of length N (total number of motor units). The i-th entry corresponds to the number of fibers
            associated to the i-th motor unit.
        """
        if self._sizes is None:
            self._retrieve_data()
            self._sizes = np.array([len(_decode_array(p, "partition")) for p in self._data_json["partition"]],
                                   dtype=int)
        return self._sizes


class MotorUnitsActionPotentials(MDTObject):
    """The action potentials for all motor units of a single muscle"""

    _data: Optional[ArrayLike] = None
    _url_prefix: str = "muap"

    @classmethod
    def new(
            cls,
            fibers: Fibers,
            fiber_basis: FiberBasis,
            fiber_properties: FiberProperties,
            motor_units: MotorUnits,
            sampling_frequency: float,
            force_computation: bool = False
    ) -> MotorUnitsActionPotentials:
        """Create new motor units action potentials for a single muscle

        Creates new motor units action potentials (MUAPs) for the fibers of a muscle.
        This will initiate a call to the Neurodec Myoelectric Digital Twin (MDT) API
        that will generate MUAPs and return their metadata.

        Args:
            fibers: The fibers for which to generate the MUAPs.
            fiber_basis: The fiber basis for which to generate the MUAPs.
            fiber_properties: The fiber properties for which to generate the MUAPs.
            motor_units: The motor units for which to generate the MUAPs.
            sampling_frequency: The sampling frequency of the output MUAPs, in Hertz.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The metadata of the new MUAPs. If another set of MUAPs with the same
            parameters already exits, those will be returned instead of generating a
            new ones.

        """

        json = {
            "force_computation": force_computation,
            "fibers_id": fibers.id,
            "fiber_basis_id": fiber_basis.id,
            "fiber_properties_id": fiber_properties.id,
            "motor_units_id": motor_units.id,
            "sampling_frequency": sampling_frequency,
        }

        return cls._new_request(json=json)

    @property
    def data(self) -> ArrayLike:
        """Returns the data associated with this MUAP"""
        if self._data is None:
            self._retrieve_data()
            self._data = _decode_array(self._data_json, "muap")
        return self._data


class ImpulseTrains(MDTObject):
    """The impulse trains of the motor units of a single muscle"""

    _url_prefix: str = "impulse_trains"

    def __init__(self, dictionary: dict):
        """Initialize impulse trains from a mapping

        This function is not meant to be called directly by users. Use ImpulseTrains.new() instead.
        """
        super().__init__(dictionary)
        self._data = None
        self._random_seed = dictionary["random_seed"]

    @property
    def random_seed(self):
        return self._random_seed

    @classmethod
    def new(
            cls,
            muaps: MotorUnitsActionPotentials,
            activation: ArrayLike,
            recruitment_rate: float = 75.0,
            excitation_frequency_min: float = 8.0,
            excitation_frequency_max: float = 32.0,
            inter_impulse_variance: float = 0.2,
            force_computation: bool = False,
            random_seed: int = DEFAULT_RANDOM_SEED
    ) -> ImpulseTrains:
        """Create new impulse trains for the motor units of a single muscle

        Creates new impulse trains for the motor units of a muscle.  This will initiate
        a call to the Neurodec Myoelectric Digital Twin (MDT) API that will generate
        impulse trains and return their metadata.

        Args:
            muaps: The MUAPs of the motor units for which the impulse trains are
                generated.
            activation: The % of muscle contraction in time.
            recruitment_rate: The recruitment rate of the motor units.
            excitation_frequency_min: The minimum excitation frequency of the motor
                units.
            excitation_frequency_max: The maximum excitation frequency of the motor
                units.
            inter_impulse_variance: The inter impulse variance.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.
            random_seed: A specific random seed to be used for the calculations. Changing the seed allows to create
                multiple instances from the same parameters.

        Returns:
            The metadata of the new impulse trains. If another set of impulse trains
            with the same parameters already exits, those will be returned instead of
            generating new ones.

        """

        json = {
            "force_computation": force_computation,
            "muap_id": muaps.id,
            "recruitment_rate": recruitment_rate,
            "excitation_frequency_min": excitation_frequency_min,
            "excitation_frequency_max": excitation_frequency_max,
            "inter_impulse_variance": inter_impulse_variance,
            "random_seed": random_seed,
        }
        json.update(_encode_array(activation, "activation"))

        return cls._new_request(json=json)

    @property
    def data(self) -> ArrayLike:
        """Returns the data associated with this impulse train"""
        if self._data is None:
            self._retrieve_data()
            self._data = _decode_array(self._data_json, "impulse_trains")
        return self._data


class Electromyography(MDTObject):
    """The electromyography of a single muscle"""

    _url_prefix: str = "emg"

    def __init__(self, dictionary: dict):
        """Initialize object from a mapping

        This function is not meant to be called directly by users. Use
        the `new` class method instead.

        """

        super().__init__(dictionary)
        self._data = None

    @property
    def data(self) -> ArrayLike:
        """Returns the EMG data"""

        # Get the data if we don't already have it.
        if self._data is None:
            # Wait for the data to be ready.
            self.wait()

            response = requests.get(f"{_API_URL}/{self._url_prefix}/{self.id}/data",
                                    json={"credentials": credentials.get()})
            if not response.ok:
                raise ValueError("The EMG data could not be retrieved.")
            self._data = np.array(response.json()["data"], dtype=np.float)

        return self._data

    @classmethod
    def new(cls, impulse_trains: ImpulseTrains, force_computation: bool = False) -> Electromyography:
        """Create a new electromyography (EMG) recording of a single muscle

        Creates a new EMG recording of a muscle.  This will initiate a call to the
        Neurodec Myoelectric Digital Twin (MDT) API that will generate a new EMG
        recording and return its metadata.

        Args:
            impulse_trains: The impulse trains of the muscle.
            force_computation: Boolean flag that allows to bypass a status check. Normally, the API would check if an
                object with the requested parameters was already present in the database. If this was the case, the API
                would not request its computation and would simply return its identifier. By setting this flag to
                `True`, the user can bypass this logic and force the computation of the resource even if it existed
                already. The main reason is to allow starting a calculation again in case of unexpected errors.

        Returns:
            The metadata of the new electromyography recording. If another EMG
            recording with the same parameters already exits, it will be returned
            instead of generating a new one.

        """

        json = {
            "force_computation": force_computation,
            "impulse_trains_id": impulse_trains.id,
        }

        return cls._new_request(json=json)


def _encode_array(array, name: str) -> dict:
    """Encodes an array to send it in an HTTP request

    Encodes an array into a dict that can be sent as data in an HTTP request. The
    type of the array is preserved.

    Args:
        array: The numpy array to encode.
        name: The name of the array in the output dict.

    Returns:
        A dict that can be appended to HTTP request data.

    """

    return {
        name: str(array.tobytes(), "ISO-8859-1"),
        f"{name}-shape": array.shape,
        f"{name}-dtype": str(array.dtype),
    }


def _decode_array(response: dict, name: str):
    """Decodes an array from an HTTP request
    Decodes an array from an HTTP request that was encoded using encode_array. The
    type of the array is preserved.
    Args:
        response: The HTTP response in dict format.
        name: The name of the array to decode.
    Returns:
        A numpy array decoded from the response.
    """
    # Depending on the source of the data (requests, or flask request), the shape
    # is not encoded in the same way.
    if isinstance(response, ImmutableMultiDict):
        shape = [int(i) for i in response.getlist(f"{name}-shape")]
    else:
        shape = response[f"{name}-shape"]
    dtype = response[f"{name}-dtype"]
    array = np.frombuffer(bytes(response[name], "ISO-8859-1"), dtype=dtype)
    array = array.reshape(shape)
    return array
