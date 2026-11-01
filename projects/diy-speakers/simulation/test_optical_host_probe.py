import socket
import threading
import time
import unittest
from optical_host_probe import (
    HEADER, MAGIC, REQUEST, REPLY, MAX_PAYLOAD,
    pack, unpack, payload_pattern, echo_server, probe
)


class OpticalHostProbeTests(unittest.TestCase):
    def test_packet_header_is_portable_and_bounded(self):
        self.assertEqual(HEADER.size,28)
        self.assertEqual(MAX_PAYLOAD,1444)
        raw=pack(REQUEST,5,2,b"abc")
        self.assertEqual(unpack(raw),(REQUEST,5,2,b"abc"))
        self.assertEqual(raw[:4],MAGIC)

    def test_payload_identity_deterministic(self):
        self.assertEqual(payload_pattern(3,4,5,512),payload_pattern(3,4,5,512))
        self.assertNotEqual(payload_pattern(3,4,5,512),payload_pattern(3,4,6,512))

    def test_crc_error_rejected(self):
        bad=bytearray(pack(REQUEST,5,2,b"abc"))
        bad[-1]^=1
        with self.assertRaisesRegex(ValueError,"CRC"):
            unpack(bytes(bad))

    def test_truncation_error_rejected(self):
        with self.assertRaises(ValueError):
            unpack(pack(REQUEST,1,0,b"test")[:-1])

    def test_unknown_magic_or_type_rejected(self):
        raw=bytearray(pack(REQUEST,1,0,b"abc"))
        raw[0]^=1
        with self.assertRaises(ValueError):
            unpack(bytes(raw))
        raw=bytearray(pack(REQUEST,1,0,b"abc"))
        raw[5]=99
        with self.assertRaises(ValueError):
            unpack(bytes(raw))

    def test_oversized_packet_rejected(self):
        with self.assertRaises(ValueError):
            pack(REQUEST,1,0,b"x"*(MAX_PAYLOAD+1))

    def test_actual_localhost_udp_loopback(self):
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
            s.bind(("127.0.0.1",0))
            port=s.getsockname()[1]
        result=[]
        thread=threading.Thread(target=lambda: result.append(
            echo_server("127.0.0.1",port,limit=8,timeout_s=5.0)))
        thread.start()
        try:
            # Bind in a separate thread; retry a few times to allow startup.
            time.sleep(.06)
            response=probe("127.0.0.1",port,count=8,payload_size=1024,timeout_s=.5)
            self.assertEqual(response["correct_echoes"],8)
            self.assertEqual(response["timeouts"],0)
            self.assertEqual(response["mismatches"],0)
        finally:
            thread.join(timeout=5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(result[0]["valid_echoes"],8)

    def test_not_raw_BER_or_clock_measurement(self):
        with self.assertRaises(ValueError):
            probe("127.0.0.1",count=0)


if __name__=="__main__":
    unittest.main()
