import sys
from typing import List, Optional, Union

from selenium.common.exceptions import (  # type: ignore
    JavascriptException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from typing_extensions import Literal, TypedDict

from inspector_commons.bridge.bridge_browser import BrowserBridge  # type: ignore
from inspector_commons.bridge.mixin import traceback  # type: ignore


class SelectorType(TypedDict):
    strategy: str
    value: str


class MatchType(TypedDict):
    name: str
    value: str


class RecordedOperation(TypedDict):
    type: str
    value: Union[None, str, bool]
    selectors: List[SelectorType]
    path: Optional[str]
    time: Optional[int]
    trigger: Literal["click", "change", "unknown"]
    source: Optional[str]
    screenshot: Optional[str]
    matches: Optional[List[MatchType]]


class RecordedEvent(TypedDict):
    actions: Optional[List[RecordedOperation]]
    actionType: Literal["exception", "stop", "append"]
    url: Optional[str]


class RecorderBridge(BrowserBridge):
    """Javascript API bridge for the web recorder functionality."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_url: Optional[str] = None
        self._recorded_operations: Union[List[RecordedOperation], None] = None

    @traceback
    def start_recording(self) -> Union[List[RecordedOperation], None]:
        self.logger.debug("Starting recording event...")
        self._record()
        self.logger.debug("Recorded events: %s", self._recorded_operations)
        return self._recorded_operations

    @traceback
    def stop_recording(self) -> Union[List[RecordedOperation], None]:
        self.web_driver.stop_recording()
        self.logger.debug("Recording should stop...")
        return self._recorded_operations

    @traceback
    def show_guide(self):
        self.web_driver.show_guide("recording-guide")

    def _record(self):
        for attempt_number in range(3):
            self.logger.debug("Recording attempt: %s", attempt_number)
            try:
                self._wait_for_page_to_load()
                event: RecordedEvent = self.web_driver.record_event()
                self.logger.debug("Raw event: %s", event)
            except JavascriptException as exc:
                self.logger.debug("Ignoring Javascript exception: %s", exc)
                event: RecordedEvent = {
                    "actionType": "exception",
                    "actions": None,
                    "url": self._current_url,
                }
                continue
            except TimeoutException:
                self.logger.debug("Retrying after script timeout")
                event: RecordedEvent = {
                    "actionType": "exception",
                    "actions": None,
                    "url": self._current_url,
                }
                continue

            if not event:
                self.logger.error("Received empty event: %s", event)
                continue

            if self._handle_event(event):
                # valid event so just return from function
                return
        self._handle_stop_event("force stop")

    def _handle_event(self, event: RecordedEvent) -> bool:
        self._recorded_operations = None

        event_type = event["actionType"]
        event_url = event["url"]

        if event_url != self._current_url:
            message: RecordedOperation = {
                "path": None,
                "time": None,
                "selectors": [],
                "type": "comment",
                "value": f"Recorder detected that URL has changed from {event_url}",
                "trigger": "unknown",
                "source": event_url,
                "screenshot": None,
                "matches": None,
            }
            self._recorded_operations = [message]
        self._current_url = event_url

        if event_type == "exception":
            self.logger.debug("Event(s) is an exception: %s", event)
        elif event_type == "event":
            self.logger.debug("Received event from page: %s", event["actions"])
            if self._recorded_operations is None:
                self._recorded_operations = []
            valid_ops = self._get_valid_ops(event=event)
            if valid_ops is not None:
                self._recorded_operations.extend(valid_ops)
        elif event_type == "stop":
            self._recorded_operations = [self._handle_stop_event(event_url=event_url)]
        else:
            raise ValueError(f"Unknown event type: {event_type}")

        return True

    def _handle_stop_event(self, event_url):
        self.logger.debug("Received stop from page")
        message: RecordedOperation = {
            "path": None,
            "time": None,
            "selectors": [],
            "type": "command",
            "value": f"Received stop from: {event_url}",
            "trigger": "stop",
            "matches": None,
            "screenshot": None,
            "source": None,
        }
        self.web_driver.stop_recording()
        return message

    def _get_valid_ops(self, event: RecordedEvent):
        self.logger.debug("Testing operations: %s", event["actions"])
        valid_ops = []
        if event.get("actions", None) is not None and event["actions"] is not None:
            for operation in event["actions"]:
                if "selectors" not in operation or len(operation["selectors"]) == 0:
                    continue
                valid_selectors = []
                for selector in operation["selectors"]:
                    self.logger.debug("Raw event selector: %s", selector)
                    if selector is not None:
                        valid_selectors.append(selector)
                operation["selectors"] = valid_selectors
                if len(valid_selectors) > 0:
                    operation["source"] = event["url"]
                    valid_ops.append(operation)
        if len(valid_ops) == 0:
            self.logger.debug("No valid actions...")
            return None
        return valid_ops

    def set_window_height(self, height):
        self.logger.debug(
            "Content sizes: %s (height) x %s (width)",
            height,
            self.window.DEFAULTS["width"],
        )
        local_width = self.window.DEFAULTS["width"]
        local_width = local_width + 5 if sys.platform == "win32" else local_width
        local_height = height + 5 if sys.platform == "win32" else height
        self.logger.debug(
            "Setting the window to: %s (height) x %s (width)",
            local_height,
            local_width,
        )
        self.window.resize(local_width, local_height)

    def _wait_for_page_to_load(self):
        try:
            waiter = WebDriverWait(self.web_driver, 10)
            waiter.until(
                lambda x: x.selenium.execute_script("return document.readyState")
                == "complete"
            )
        except Exception as ex:  # pylint: disable=W0703
            self.logger.debug(
                "There was an exception while waiting for page to load: %s", ex
            )
