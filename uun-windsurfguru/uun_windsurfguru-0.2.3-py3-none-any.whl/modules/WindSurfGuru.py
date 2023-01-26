import json
from requests.exceptions import ConnectionError
from enum import IntEnum, Enum, auto
from typing import Optional, Dict, Any
import logging

from uun_iot_libledstrip import Action, ActionType, hex2rgb
from uun_iot_libledstrip import StripOverlayBundle, LedStrip, LedStripSegment, MeterStrip, MeterStripSegment
from uun_iot_libledstrip.devices import LedDev
from uun_iot import Module, on

logger = logging.getLogger(__name__)

# currently active app mode - SPECIAL state (error etc., see SpecialState) or normal METER functionality
class Overlay(IntEnum):
    """ Overlays of LED strip for different functionalities. """
    #: basic functionality
    METER = auto()
    #: abnormal behaivour - :class:`SpecialState`
    SPECIAL = auto()

# possible special states of the app (not normal functionality)
# right sides are the keys in config file
class SpecialState(Enum):
    """ Special states of the LED strip signaling some abormality. """
    NO_CONNECTION = "noConnection"
    ERROR = "error"
    BLANK = "blank"

class WindSurfGuru(Module):
    """ Module for visualization of wind speeds on a LED strip.

    The method :meth:`on_tick` is repeatedly executed by the `:pkg:uun-iot` library. The method  gets data from uuCmd ``weatherConditions/getLast``. If it successfuly retrieved the weather data, it will attempt to display them on the strip. If there was an error (internet connection error or any other code-related Exception), go into special state and display the error on the LED strip.

    .. raw:: html

       <hr>

    The display of error, or the actual wind speed data on the strip is exweather data, it will attempt to display them on the strip. If there was an error (internet connection error or any other code-related Exception), go into special state and display the error on the LED strip.

    The LED strip device can be realized by various physical hardwares. Examples are:

    - a simple array of one-colored LEDs controled over GPIO,
    - the same array but with a I2C controller, or
    - an individually color-controllable LED strip such as Neopixel driven by an external library.

    For each of these examples, there is a corresponding :class:`uun_iot_libledstrip.devices.LedDev` driver -- called :class:`~uun_iot_libledstrip.devices.GPIODev`, :class:`~uun_iot_libledstrip.devices.I2CDev` and :class:`~uun_iot_libledstrip.devices.NeopixelDev`, respectively. All of these drivers inherit from the `LedDev` interface and are thus interchangeable. Of course, the simple one-colored LED strip cannot have different colours, but the driver behaves like they can -- this is done for interchangeability of the underlying code. The code should not depend on the current realization of the hardware LED strip backend. The LED strip type can be chosen in configuration.

    .. raw:: html

       <hr>

    The display of an error, or the actual wind speed data on the strip, is exclusive -- meaning that only the error, or the data can be displayed at the same time. For this reason, there is a :class:`uun_iot_libledstrip.StripOverlayBundle` which provides exactly this exclusive access to the underlying hardware device. 

    On module initialization, two :class:`uun_iot_libledstrip.LedStrip`-s are created. One responsible for the error display and the second :class:`uun_iot_libledstrip.MeterStrip`, inheriting from class `LedStrip`, responsible for linear display of the wind speed on the strip. The `StripOverlayBundle` can then change in between the two by clearing the old one and activating the new one. This ensures exclusivity.

    A `LedStrip` instance is created using a `LedDev` driver and a list or a dictionary of :class:`uun_iot_libledstrip.LedStripSegments`-s. Each of the segments has a fixed LED position span (for example from 2nd to 5th LED) and the segments act as basic building blocks. Each of the segments can be lit with a solid color or can blink with given color and with given period. This display action can be encapsulated in a :class:`uun_iot_libledstrip.Action` object, which is a "container" for these two kinds of visualization. `Action` can be stored in a segment and then activated later, activating the saved display action (blinking/solid color).

    .. raw:: html

       <hr>

    A :class:`uun_iot_libledstrip.MeterStrip` bases on `LedStrip` and is composed of :class:`uun_iot_libledstrip.MeterStripSegment`-s which base on `LedStripSegment`. Each `MeterStripSegment` is given a `LedDev`, array of led IDs and two crucial values: ``value_min`` and ``value_max``. As the name `MeterStripSegment` suggests, the segment is supposed to measure some quantity. The segment linearly interpolates between tuning on no LEDs and turning on all of the allocated LEDs in the segment, based on ``value``. The ratio of turned on LEDs is computed simply as ``value/(value_max-value_min)`` and the LEDs turn on up from lowest to highest IDs (or positions). This is done by virually decreasing the number of LEDs in a segment. If the value is less than `value_min`, all LEDs are off and if above `value_max`, all LEDs are on. The ``value`` can be set using a :meth:`uun_iot_libledstrip.MeterStripSegment.set_value`.

    .. raw:: html

       <hr>

    Additionaly, a `MeterStripSegment` can be initialized with an optional **hook** function. The hook function is called at the end of :meth:`uun_iot_libledstrip.MeterStripSegment.set_value` and is given current `value` together with some `MeterStripSegment` properties. The function should return an Action, which will be stored into the segment and can be activated later. This can be used to dynamically change stored `Action` for the `MeterStripSegment` based on current `value` given in :meth:`~uun_iot_libledstrip.MeterStripSegment.set_value`. 

    The `MeterStrip` has a method with the same name :meth:`~MeterStripSegment.set_value` which calls `set_value` on each of its segments and additionaly activates their action.

    The following example illustrates this behaviour:

        .. code-block:: python

            def hook(value, leds, action):
                if value > 100:
                    action = Action(ActionType.SOLID, color=(255,0,0))
                else:
                    action = Action(ActionType.SOLID, color=(0,255,0))
                return leds, action

            segment = MeterStripSegment(
                device, autoshow=True, leds=[0,1,2,3,4],
                value_min=5, value_max=200,
                hook_set_value=hook
            )

            # definition of MeterStrip strip containing the segment
            strip = MeterStrip(device,[segment])

            strip.set_value(200)
            strip.set_value(50)

        >>> # the whole segment is lit red (255, 0, 0)
        >>> # some LEDs in the segment are lit green (0, 255, 0)

    This **hook** behaviour is used to set special actions if the wind speed is less than 15 knt or more than 30 knt for the first and the last segments. The whole process can be directly controlled from the configuration file.

    .. raw:: html

       <hr>

    In the **configuration file**, there are the definitions of the segments. Each segment contains a default action in keys ``color, action, interval``. The LED positions are in the ``settings`` subkey together with definitions for minimal and maximal wind values for the given segment. The segment may have defined a ``specialAction`` key. The key contains information about the associated `Action` together with a ``condition`` key. The key indicates, when to activate the special action using the **hook** `MeterStripSegment` functionality.

    Possible values of configuration ``<severity>/specialAction/condition`` are the following:

        Each `condition` translates to one of:

            - `ifWindBelow`: ``wind < windMin``,

            - `ifWindBetween`: ``windMin <= wind <= windMax``,

            - `ifWindGreater`: ``windMax < wind``,

        where `wind` is the value of wind at the time of calling :meth:`self._meter_strip.set_value`.
        If the wind conditions above are satisfied, apply the special action to the segment.
        Otherwise apply normal action.

    Example of configuration file:

        .. code-block:: json
            
            {
                "oidcGrantToken": {
                    "gateway": "uuidentity.plus4u.net",
                    "uuAppName": "uu-oidc-maing02",
                    "awid": "xxx",
                    "uuCmd": "oidc/grantToken",
                    "tokenPath": "./oidc-token"
                },
                "uuThing": {
                    "accessCode1": "xxx",
                    "accessCode2": "xxx"
                },
                "uuApp": {
                    "gateway": "uuapp.plus4u.net",
                    "uuAppName": "ucl-weatherstation-maing01",
                    "awid": "xxx",
                    "uuCmdList": {
                        "weatherConditionsGetLast": "weatherConditions/getLast"
                    }
                },
                "gateway": {
                    "moduleTimers": {
                        "windSurfGuru": 120
                    },
                    "windSurfGuru": {
                        "weatherStationCode": "MELTEMI",
                        "ledStrip": {
                            "device": "virtual",
                            "pixels": 16,
                            "pin": "D10"
                        },
                        "state": {
                            "noConnection": {
                                "color": "#ff0000",
                                "action": "blink",
                                "interval": 0.2
                            },
                            "blank": {
                                "color": "#000000",
                                "action": "solid",
                                "interval": null
                            },
                            "error": {
                                "color": "#ff0000",
                                "action": "blink",
                                "interval": 0.2
                            }
                        },
                        "severity": {
                            "low": {
                                "color": "#0000ff",
                                "action": "solid",
                                "interval": null,
                                "specialAction": {
                                    "condition": "ifWindBetween",
                                    "color": "#0000ff",
                                    "action": "blink",
                                    "interval": 0.2
                                },
                                "settings": {
                                    "windMin": 0,
                                    "windMax": 14,
                                    "ledMinPosition": 0,
                                    "ledMaxPosition": 0
                                }
                            },
                            "light": {
                                "color": "#0000ff",
                                "action": "solid",
                                "interval": null,
                                "settings": {
                                    "windMin": 16,
                                    "windMax": 18,
                                    "ledMinPosition": 1,
                                    "ledMaxPosition": 3
                                }
                            },
                            "optimal": {
                                "color": "#00ff00",
                                "action": "solid",
                                "interval": null,
                                "settings": {
                                    "windMin": 19,
                                    "windMax": 22,
                                    "ledMinPosition": 4,
                                    "ledMaxPosition": 7
                                }
                            },
                            "heavy": {
                                "color": "#ff8000",
                                "action": "solid",
                                "interval": null,
                                "settings": {
                                    "windMin": 23,
                                    "windMax": 26,
                                    "ledMinPosition": 8,
                                    "ledMaxPosition": 11
                                }
                            },
                            "extreme": {
                                "color": "#ff0000",
                                "action": "solid",
                                "interval": null,
                                "specialAction": {
                                    "condition": "ifWindGreater",
                                    "color": "#ff0000",
                                    "action": "blink",
                                    "interval": 0.2
                                },
                                "settings": {
                                    "windMin": 27,
                                    "windMax": 30,
                                    "ledMinPosition": 12,
                                    "ledMaxPosition": 15
                                }
                            }
                        }
                    }
                }
            }



    Args:
        config: gateway configuration
        get_uucmd: uucmd for getting new weather conditions, uucmd(weatherstation_code) -> :class:`requests.Response`
        device: optional external :class:`uun_iot_libledstrip.LedDev`

    Raises:
        ValueError: if ``device`` was specified and is not an instance of :class:`LedDev`
    """
    _device: LedDev
    _meter_segments: Dict[any, MeterStripSegment]
    _wind_knt_min: float
    #_wind_knt_max: float
    #: bundle a MeterStrip for normal usage and a general LedStrip for special state display
    _sbundle: StripOverlayBundle

    def __init__(self, config: dict, get_uucmd, device: LedDev=None):
        super().__init__(config=config)
        self._get_uucmd = get_uucmd

        if device is None:
            self._device = self._init_hw()
        else:
            if isinstance(device, LedDev):
                self._device = device
            else:
                raise ValueError("specified `device`, if used, must inherit from LedDev")

        # meter strip
        # initialized segments from configuration entry "severity"
        self._meter_segments = self._init_meter_segments()
        mstrip = MeterStrip(
                device=self._device,
                segments=self._meter_segments,
            )

        # wmin = wmax = None
        # for _, x in self._c("severity").items():
        #     if x["settings"]["windMax"] is None:
        #         continue
        #     wmin = wmin if wmin is None else min(wmin, x["settings"]["windMin"])
        #     wmax = wmax if wmax is None else max(wmax, x["settings"]["windMax"])

        self._wind_knt_min = min([x["settings"]["windMin"] for _,x in self._c("severity").items()]) #wmin
        #self._wind_knt_max = wmax

        # special state (errors) strip
        # initialized segments from configuration entry "state"
        sstrip = LedStrip(
                device=self._device,
                segments=self._init_state_segments(),
            )

        self._sbundle = StripOverlayBundle({
            Overlay.METER: mstrip,
            Overlay.SPECIAL: sstrip
        })

    def _init_hw(self) -> LedDev:
        """
        Initialize underlying LED strip.
        Look at configuration ``ledStrip/device`` to determine what type of LED
        strip to use. Also read ``ledStrip/pixels`` to determine number of pixels to use.
        Some ``devices`` might use the ``ledStrip/pin`` setting (such as `neopixel`). The numbering of `pin` depends on used ``device``.

        ``ledStrip/device``: `neopixel`, `i2c`, `virtual` (`virtual` is default, if none of the before were found)
        """
        n_pixels = self._c("ledStrip/pixels")
        dev = self._c("ledStrip/device")

        try:
            if dev == "neopixel":
                pin_id = self._c("ledStrip/pin")

                import board
                from uun_iot_libledstrip.devices import NeopixelDev

                try: 
                    pin = getattr(board, pin_id)
                except AttributeError:
                    raise ValueError("Invalid `pin` setting, cannot find this pin in package `board`.")

                device = NeopixelDev(
                    pin, n_pixels, brightness=0.1 #, auto_write=False #unnecessary
                )

            #elif dev == "gpio":
            #    pins = self._c("ledStrip/pin")

            #    from uun_iot_libledstrip.devices import GPIODev
            #    device = GPIODev(
            #        pins, len(pins), pin_numbering="BOARD"
            #    )
            elif dev == "i2c":
                from uun_iot_libledstrip.devices import I2CPixelDev
                device = I2CPixelDev(n_pixels, addr=0x20)
            else:
                from uun_iot_libledstrip.devices import DebugLedDev
                logger.info("Creating virtual led strip.")
                device = DebugLedDev(n_pixels)

        except ImportError as e:
            logger.exception(e)
            raise ValueError(f"This gateway does not have installed packages for `{dev}`.")

        return device

    def _init_state_segments(self) -> Dict[Any, LedStripSegment]:
        """
        Special states have a single common segment stretching over the whole strip
        with variable actions depending on state (see :meth:`._set_special_state`). 
        """
        return {
            0: LedStripSegment(
                device=self._device,
                leds = list(range(0, self._c("ledStrip/pixels"))),
                autoshow=False
            )
        }

    def _init_meter_segments(self) -> Dict[Any, MeterStripSegment]:
        """
        Each ``severity`` key in configuration corresponds to one LED segment.

        For severities which have special action ``specialAction`` and ``specialAction/condition``
        configured, add ``hook_set_value`` hook to the severity segment.
        See ``uun_iot_libledstrip.MeterStripSegment`` for more information about hooks.

        Possible values of configuration ``<severity>/specialAction/condition`` are the following.
        Each `condition` translates to one of:

            - `ifWindBelow`: ``wind < windMin``,

            - `ifWindBetween`: ``windMin <= wind <= windMax``,

            - `ifWindGreater`: ``windMax < wind``,

        where `wind` is the value of wind at the time of calling :meth:`self._meter_strip.set_value`.
        If the wind conditions above are satisfied, apply the special action to the segment.
        Otherwise apply normal action.
        """
        seg_map = {}
        for (name, centry) in self._c("severity").items():
            settings = centry["settings"]
            wind_min = settings["windMin"]
            wind_max = settings["windMax"]
            min_led = settings["ledMinPosition"]
            max_led = settings["ledMaxPosition"]

            # normal action
            naction = self._create_action_from_config(centry)

            if "specialAction" in centry and "condition" in centry["specialAction"]:
                # create factory function and call it
                # otherwise, because of delayed execution, centry and other loop parameters
                #   would be the same for all hook functions
                # cell-var-from-loop: Cell variable wind_max, centry defined in loop
                def hook_factory(wind_min, wind_max, centry, naction):
                    sacentry = centry["specialAction"]
                    saction = self._create_action_from_config(sacentry)
                    if sacentry["condition"] == "ifWindLess":
                        def hook(value, leds, action):
                            return leds, saction if value < wind_min else naction
                    elif sacentry["condition"] == "ifWindBetween":
                        def hook(value, leds, action):
                            return leds, saction if wind_min <= value <= wind_max else naction
                    elif sacentry["condition"] == "ifWindGreater":
                        def hook(value, leds, action):
                            return leds, saction if wind_max < value else naction
                    else:
                        logger.error("Condition for the `specialAction` of severity `%s` must be "
                        "one of `ifWindLess`, `ifWindBetween`, or `ifWindGreater`.", name)
                        return None
                    return hook
            else:
                def hook_factory(*args, **kwargs):
                    return None

            seg = MeterStripSegment(
                    device=self._device,
                    autoshow=False,
                    leds=list(range(min_led, max_led +1)),
                    value_min=wind_min,
                    value_max=wind_max,
                    hook_set_value=hook_factory(wind_min, wind_max, centry, naction)
                )

            # store predefined action for this segment
            seg.store_action( naction )
            seg_map[name] = seg

        return seg_map

    @on("tick")
    def on_tick(self) -> None:
        """Method to be called on each timer hit.

        Receive information about weather from uuApp and call :meth:`.evaluate_conditions` to display the wind speed on the strip.

        When ConnectionError occurs (when getting weather conditions), set special state to :attr:`SpecialState.NO_CONNECTION` using :meth:`._set_special_state`. When any other exception occurs, set state to :attr:`SpecialState.ERROR` by same procedure.

        """
        try:
            response = self._get_uucmd(self._c('weatherStationCode'))
            if (response.status_code >= 200 and response.status_code < 300):
                weather_conditions_data = json.loads(response.text)
                wind_speed_kph = weather_conditions_data['currentConditions']['type1']['windSpeedAvgLast10Min']
                self.evaluate_conditions(wind_speed_kph)
            else:
                self._set_special_state(SpecialState.NO_CONNECTION)

        except ConnectionError:
            logger.debug("Connection error.")
            self._set_special_state(SpecialState.NO_CONNECTION)

        except Exception as e:
            self._set_special_state(SpecialState.ERROR)
            raise e

    def _set_special_state(self, state: SpecialState) -> None:
        """Set application special state.
        
        Display a :class:`SpecialState` on the LED strip (currently whole strip, see :meth:`._init_state_segments`),
        action for the strip/segments are taken from configuration.

        Args:
            state: :class:`SpecialState` state to display
        """
        logger.info(f"Going into special app state {state}.")
        centry = self._c("state")[state.value]
        action = self._create_action_from_config(centry)

        self._sbundle.set_strip(Overlay.SPECIAL)
        self._sbundle.strip.activate(action)
        self._sbundle.strip.show()

    def evaluate_conditions(self, wind_speed_kph: float) -> None:
        """Process wind speed and display it on a LED strip accordingly.

        Args:
            wind_speed_kph: wind speed in km/h

        """
        wind_speed_knt = round(wind_speed_kph * 0.5399568035)
        logger.info("Wind speed: %i knot, %i kph.", wind_speed_knt, round(wind_speed_kph,2))

        self._sbundle.set_strip(Overlay.METER)
        self._sbundle.strip.set_value(wind_speed_knt)
        self._sbundle.strip.show()

    def _create_action_from_config(self, centry: dict) -> Action:
        """
        Create :class:`~uun_iot_libledstrip.Action` object from configuration dictionary
        with keys ``{"action": ..., "color": ..., "interval": ...}``.

        Args:
            centry: configuration dictionary. Key ``action`` can be ``solid`` or ``blink``,
                ``color`` is in hex format and ``interval`` is in seconds.

        Returns:
            Action: :class:`~uun_iot_libledstrip.Action` object constructed from ``centry``
        """
        atype = ActionType.SOLID if centry["action"] == "solid" else ActionType.BLINK
        interval = centry["interval"]
        return Action(type=atype, color=hex2rgb(centry["color"]), period=interval)
