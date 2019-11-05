# coding=utf-8
import sys
from io import BlockingIOError
import selectors
import json
import io
import uuid
import struct
from sense_hat import SenseHat


class SenseData:

    def __init__(self):
        self.keys = None
        self._W = 0
        self._A = 0
        self._S = 0
        self._D = 0
        self._F = 0
        self._right = 0
        self._left = 0
        self._sense = SenseHat()
        self._sense.clear()
        self._yaw0 = 0
        self._shift = 0
        self._sense.set_rotation(90)
        self.uuid = 0

    def _content_encode(self):
        self.keys = dict(
            type="text/json",
            encoding="utf-8",
            content=dict(W=self._W, A=self._A, S=self._S, D=self._D,
                         F=self._F, right=self._right, left=self._left, shift=self._shift, uuid=self.uuid),
        )

    def _sample(self):
        self._ResetBuffer()
        # mouse right button
        acceleration = self._sense.get_accelerometer_raw()
        x = round(acceleration['x'], 0)
        y = round(acceleration['y'], 1)
        z = round(acceleration['z'], 0)
        # key A D
        if y > 0.3:
            self._sense.show_letter("D",text_colour=[255, 255, 0])
            self._D = 1
        elif y < -0.3:
            self._sense.show_letter("A",text_colour=[255, 255, 0])
            self._A = 1
        else:
            self._A = 0
            self._D = 0
        if x < -0.7:
            self._shift = 1
        else:
            self._shift = 0
        o = self._sense.get_orientation()
        pitch = o["pitch"]
        roll = o["roll"]
        yaw = o["yaw"]
        # yaw_1 = round(yaw, 1)
        # if yaw_1 - self._yaw0 > 20:
        #     self._D = 1
        # elif yaw_1 - self._yaw0 < -20:
        #     self._A = 1
        # else:
        #     self._D = 0
        #     self._A = 0
        # self._yaw0 = yaw_1
        # key W S
        event = self._sense.stick.get_events()
        if len(event) > 0:
            if event[0].direction == 'left':
                if event[0].action == 'pressed' or event[0].action == 'held':
                    self._S = 1
                    self._sense.show_letter("S",text_colour=[255, 255, 0])
                elif event[0].action == 'released':
                    self._S = 0

            if event[0].direction == 'right':
                if event[0].action == 'pressed' or event[0].action == 'held':
                    self._W = 1
                    self._sense.show_letter("W",text_colour=[255, 255, 0])
                elif event[0].action == 'released':
                    self._W = 0

            if event[0].direction == 'middle':
                if event[0].action == 'pressed' or event[0].action == 'held':
                    self._left = 1
                    self._sense.show_letter("B",text_colour=[255, 255, 0])
                elif event[0].action == 'released':
                    self._left = 0

            if event[0].direction == 'up':
                if event[0].action == 'pressed' or event[0].action == 'held':
                    self._F = 1
                    self._sense.show_letter("F",text_colour=[255, 255, 0])
                elif event[0].action == 'released':
                    self._F = 0
        self.uuid = str(uuid.uuid1())

    def _ResetBuffer(self):
        self._S = 0
        self._W = 0
        self._A = 0
        self._D = 0
        self._left = 0
        self._right = 0
        self._F = 0
        self._shift = 0
        self.uuid = 0

    def build(self):
        self._sample()
        self._content_encode()
        response = self._create_response_json_content()
        message = self._create_message(**response)
        return message

    def _create_message(self, *, content_bytes, content_type, content_encoding):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _create_response_json_content(self):
        content = self.keys
        content_encoding = "utf-8"
        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        return response
