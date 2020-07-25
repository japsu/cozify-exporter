#!/usr/bin/env python3

import re
from pprint import pprint

from cozify import hub
from flask import Flask, Response


app = Flask(__name__)

EXCLUDE_KEYS = [
    'cozify_type',
    'cozify_use_pir',
    'cozify_upgrade_status',
    'cozify_user',

    # ZigBee Light Link (IKEA Trådfri etc.) static values, not interesting
    'cozify_min_temperature',
    'cozify_max_temperature',
    'cozify_color_mode',
]

COUNTERS = [
    'cozify_last_change',
    'cozify_last_seen',
    'cozify_last_motion',
    'cozify_moisture_at',
    'cozify_twilight_start',
    'cozify_twilight_stop',
]


# https://stackoverflow.com/a/1176023/1012299
def camel_to_snake(key):
    key = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', key).lower()


@app.route('/metrics')
def metrics():
    registry = dict()

    for device in hub.devices().values():
        # pprint(device)
        name = device['name']

        for key, value in device['state'].items():
            key = 'cozify_' + camel_to_snake(key)

            if key in EXCLUDE_KEYS or value is None:
                continue

            try:
                value = float(value)
            except (TypeError, ValueError) as e:
                app.logger.exception("Failed to cast %s", key)
                continue

            # HACK: Both temperature and color temperature are reported under same key, bad
            capabilities = device.get("capabilities", {}).get("values", [])
            if (
                key == "cozify_temperature" and
                "COLOR_TEMP" in capabilities and
                "TEMPERATURE" not in capabilities
            ):
                key = "cozify_color_temperature"

            registry.setdefault(key, {})
            registry[key][name] = value

    output_lines = []

    for key, values_by_name in registry.items():
        metric_type = 'counter' if key in COUNTERS else 'gauge'
        output_lines.append(f'# TYPE {key} {metric_type}')
        for name, value in values_by_name.items():
            output_lines.append(f'{key}{{name="{name}"}} {value}')

    output_lines.append('')

    response = Response('\n'.join(output_lines))
    response.headers['Content-Type'] = 'text/plain; version=0.0.4'
    return response


if __name__ == "__main__":
    print(metrics().data.decode('UTF-8'))
