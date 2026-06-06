# ================================
# Name: 'a-umami-dashboard'/main.py
# Author: 'a-matthew'/Mateusz A.
# Year: 2026
# Comments: No LLMs are used.
# I wrote this prototype on the night of 5th of June as a simple dashboard 'concept'.
# I then ran out of energy and tea (, but mostly energy). I might built it into an AppImage with more functions.
# Quick references:
# https://docs.umami.is/docs/cloud/api-key
# https://stackoverflow.com/questions/24518944/try-except-when-using-python-requests-module # exception handling of 'requests' as proposed by the library maintainer
# ================================

from datetime import date, datetime, timedelta
from typing import Callable

import matplotlib
import requests
from environs import env

matplotlib.use("qtagg")

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

# Hardcoded time spans
LAST_30D = (
    int(
        datetime(
            (date.today() - timedelta(days=30)).year,
            (date.today() - timedelta(days=30)).month,
            (date.today() - timedelta(days=30)).day,
        ).timestamp()
        * 1000
    ),
    int(
        datetime(date.today().year, date.today().month, date.today().day).timestamp()
        * 1000
    )
    - 1,
)
LAST_7D = (
    int(
        datetime(
            (date.today() - timedelta(days=7)).year,
            (date.today() - timedelta(days=7)).month,
            (date.today() - timedelta(days=7)).day,
        ).timestamp()
        * 1000
    ),
    int(
        datetime(date.today().year, date.today().month, date.today().day).timestamp()
        * 1000
    )
    - 1,
)
LAST_24H = (
    int(
        datetime(
            (date.today() - timedelta(days=1)).year,
            (date.today() - timedelta(days=1)).month,
            (date.today() - timedelta(days=1)).day,
        ).timestamp()
        * 1000
    ),
    int(
        datetime(date.today().year, date.today().month, date.today().day).timestamp()
        * 1000
    )
    - 1,
)
TODAY = (
    int(
        datetime(date.today().year, date.today().month, date.today().day).timestamp()
        * 1000
    ),
    int(
        datetime(
            (date.today() + timedelta(days=1)).year,
            (date.today() + timedelta(days=1)).month,
            (date.today() + timedelta(days=1)).day,
        ).timestamp()
        * 1000
    )
    - 1,
)

DEBUG = 1


def websites_get(
    api_endpoint: str, api_route: str, request_headers: dict
) -> dict[str, str]:
    """
    Send REST API request for all list of pages
    """
    global DEBUG
    response = requests.get(f"{api_endpoint}{api_route}", headers=request_headers)
    try:
        response.raise_for_status()
        json_response = response.json()
        if DEBUG == 1:
            print(f"websites_get|Sent request: {api_endpoint}{api_route}")
            print(f"websites_get|Total number of pages: {json_response['count']}")
            # print(f"websites_get|Data: {json_response['data']}")
        return dict(json_response)
    except requests.exceptions.HTTPError as e:
        raise Exception("websites_get: " + str(e))


def website_metrics_get(
    api_endpoint: str,
    api_route: str,
    metric_type: str,
    time: tuple,
    request_headers: dict,
) -> tuple[list, str]:  # Metrics value, Metrics type
    """
    Send REST API request for page metrics
    """
    global DEBUG
    response = requests.get(
        f"{api_endpoint}{api_route}?type={metric_type}&startAt={time[0]}&endAt={time[1]}",
        headers=request_headers,
    )
    if DEBUG == 1:
        print(
            f"website_metrics_get|Sent request: {api_endpoint}{api_route}?type={metric_type}&startAt={time[0]}&endAt={time[1]}"
        )
    try:
        response.raise_for_status()
        json_response = response.json()
        return (json_response, metric_type)
    except requests.exceptions.HTTPError as e:
        raise Exception("website_metrics_get: " + str(e))


def page_switch(widget: QStackedWidget, offset: int, modulo_space: int) -> None:
    """
    Switch stack layout elements
    """
    index = (widget.currentIndex() + offset) % modulo_space
    widget.setCurrentIndex(index)


def page_build(index: int, page: tuple, lambda_call: list[Callable]) -> QWidget:
    """
    Build page layouts
    """
    widget_page = QWidget()
    layout_page = QVBoxLayout(widget_page)  # Page layout
    layout_page.addStretch()
    site_id, site_name, site_domain = page
    json_website_metrics, metric_type = lambda_call[index]()
    if DEBUG == 1:
        print(f"page_build|Response: {json_website_metrics}")
    metric = [item["x"] for item in json_website_metrics]
    values = [item["y"] for item in json_website_metrics]
    figure = Figure(figsize=(10, 5))
    axes = figure.subplots()
    axes.bar(metric, values)
    axes.set_xlabel(metric_type.title())
    axes.set_ylabel("Value")
    axes.set_title(f"{site_name} ({site_domain})")
    figure.autofmt_xdate(rotation=45, ha="right")
    figure.tight_layout()
    canvas = FigureCanvas(figure)
    layout_page.addWidget(canvas)
    return widget_page


def window_build(pages: list[tuple], lambda_call: list[Callable]) -> QWidget:
    """
    Build main window
    """
    widget_stack = QStackedWidget()  # Shared page layout
    for index, page in enumerate(pages):
        widget_page = page_build(index, page, lambda_call)
        widget_stack.addWidget(widget_page)
    button_previous = QPushButton("Next →")
    button_previous.clicked.connect(lambda: page_switch(widget_stack, -1, len(pages)))
    button_next = QPushButton("← Previous")
    button_next.clicked.connect(lambda: page_switch(widget_stack, 1, len(pages)))

    # Main Window
    widget_main = QWidget()
    layout_main = QVBoxLayout(widget_main)
    layout_main.addWidget(widget_stack)
    layout_main.addWidget(button_previous)
    layout_main.addWidget(button_next)
    return widget_main


if __name__ == "__main__":
    """
    Initialize main window
    """
    # Should be moved somewhere else
    env.read_env()
    API_ENDPOINT = f"{env.str('API_ENDPOINT_URL')}/v1"
    HEADERS = {
        "Accept": "application/json",
        "x-umami-api-key": env.str("API_ENDPOINT_KEY"),
    }
    # websites_get lambda
    lambda_websites_get = lambda api_endpoint=API_ENDPOINT, headers=HEADERS: (  # noqa: E731
        websites_get(api_endpoint, "/websites", headers)
    )
    json_websites: dict = lambda_websites_get()
    websites = [
        (site["id"], site["name"], site["domain"]) for site in json_websites["data"]
    ]
    # websites_get_metrics_path lambda
    lambda_metrics_get_path = [
        lambda api_endpoint=API_ENDPOINT, site_id=site_id, time=LAST_30D, headers=HEADERS: (
            website_metrics_get(
                api_endpoint, f"/websites/{site_id}/metrics", "path", time, headers
            )
        )
        for site_id, site_name, site_domain in websites
    ]
    # More metrics (lambdas) can be defined, then passed over to the window builder to build different types of plots.
    # Not implemented
    # Build window
    app = QApplication([])
    window = window_build(websites, lambda_metrics_get_path)
    window.setWindowTitle("A Umami dashboard")
    window.resize(1000, 600)
    window.show()
    app.exec()
