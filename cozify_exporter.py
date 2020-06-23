#!/usr/bin/env python3

from cozify import hub
from flask import Flask, Response


app = Flask(__name__)


@app.route('/metrics')
def metrics():
    output_lines = [
        "# HELP temperature_celsius Temperature in degrees Celsius",
        "# TYPE temperature_celsius gauge",
    ]

    for device in hub.devices(capabilities=hub.capability.TEMPERATURE).values():
        name = device['name']
        temperature = device['state']['temperature']
        output_lines.append(f'temperature_celsius{{name="{name}"}} {temperature}')

    output_lines.append('')

    response = Response('\n'.join(output_lines))
    response.headers['Content-Type'] = 'text/plain; version=0.0.4'
    return response


if __name__ == "__main__":
    app.run()
