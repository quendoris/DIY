#!/usr/bin/env python3
"""Portable reference UDP packet-echo / probe for the optical lab.

Host-only transport harness: can run on localhost NOW; can run across 100BASE-FX
once a second endpoint implements the matching UDP echo protocol.
NOT an STM32 firmware, latency guarantee, cryptographic MAC, clock test or raw BER.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import socket
import struct
import time
import zlib

MAGIC = b"OPTF"
VERSION = 1
REQUEST = 1
REPLY = 2
PORT = 50808
HEADER = struct.Struct("!4sBBHIQII")
MAX_PAYLOAD = 1472 - HEADER.size


def payload_pattern(seed: int, epoch: int, seq: int, size: int) -> bytes:
    if not (0 <= seed < 2**64 and 0 <= epoch < 2**32 and 0 <= seq < 2**64
            and 0 <= size <= MAX_PAYLOAD):
        raise ValueError("invalid reproducible pattern parameters")
    key = struct.pack("!QIQ", seed, epoch, seq)
    return hashlib.shake_256(key).digest(size)


def pack(kind: int, epoch: int, seq: int, data: bytes) -> bytes:
    if kind not in (REQUEST, REPLY) or len(data) > MAX_PAYLOAD:
        raise ValueError("unsupported packet kind or size")
    if not (0 <= epoch < 2**32 and 0 <= seq < 2**64):
        raise ValueError("invalid epoch or sequence")
    body = struct.pack("!IQ", epoch, seq) + data
    crc = zlib.crc32(body)
    return HEADER.pack(MAGIC, VERSION, kind, 0, epoch, seq, len(data), crc) + data


def unpack(raw: bytes) -> tuple[int, int, int, bytes]:
    if len(raw) < HEADER.size:
        raise ValueError("truncated frame")
    magic, version, kind, flags, epoch, seq, size, crc = HEADER.unpack_from(raw)
    if magic != MAGIC or version != VERSION or kind not in (REQUEST, REPLY) or flags != 0:
        raise ValueError("unknown frame magic/version/type/flags")
    data = raw[HEADER.size:]
    if size != len(data) or size > MAX_PAYLOAD:
        raise ValueError("wrong payload length")
    if zlib.crc32(struct.pack("!IQ", epoch, seq) + data) != crc:
        raise ValueError("CRC mismatch")
    return kind, epoch, seq, data


def echo_server(bind: str = "127.0.0.1", port: int = PORT,
                limit: int = 0, timeout_s: float = 60.) -> dict:
    if limit < 0 or timeout_s <= 0:
        raise ValueError("invalid echo test parameters")
    received = 0
    dropped = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((bind, port))
        sock.settimeout(.25)
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline and (limit == 0 or received < limit):
            try:
                raw, peer = sock.recvfrom(2048)
            except socket.timeout:
                continue
            try:
                kind, epoch, seq, data = unpack(raw)
                if kind != REQUEST:
                    raise ValueError("unexpected reply on server")
                received += 1
                sock.sendto(pack(REPLY, epoch, seq, data), peer)
            except ValueError:
                dropped += 1
    return {"valid_echoes": received, "invalid_dropped": dropped}


def probe(target: str, port: int=PORT, count: int=100,
          payload_size: int=512, timeout_s: float=1.0,
          epoch: int=1, seed: int=0xD15EA5E) -> dict:
    """Sequential request/response round-trip test, NOT a bulk throughput test."""
    if count <= 0 or not 0 <= payload_size <= MAX_PAYLOAD or timeout_s <= 0:
        raise ValueError("invalid probe configuration")
    rtts = []
    mismatched = 0
    timeouts = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(timeout_s)
        sock.connect((target, port))
        for seq in range(count):
            data = payload_pattern(seed, epoch, seq, payload_size)
            sent = pack(REQUEST, epoch, seq, data)
            t0 = time.monotonic_ns()
            sock.send(sent)
            try:
                packet = sock.recv(2048)
                kind, got_epoch, got_seq, got_data = unpack(packet)
                if kind != REPLY or got_epoch != epoch or got_seq != seq or got_data != data:
                    mismatched += 1
                    continue
            except socket.timeout:
                timeouts += 1
                continue
            except ValueError:
                mismatched += 1
                continue
            rtts.append((time.monotonic_ns()-t0)/1e6)
    samples=sorted(rtts)
    return {
        "scope":"sequential UDP request/response application test; NOT physical BER or one-way sync",
        "sent_frames":count,"correct_echoes":len(samples),
        "timeouts":timeouts,"mismatches":mismatched,
        "payload_bytes_each":payload_size,
        "min_rtt_ms":round(samples[0],4) if samples else None,
        "median_rtt_ms":round(samples[len(samples)//2],4) if samples else None,
        "max_rtt_ms":round(samples[-1],4) if samples else None,
        "comment":"PC runtime scheduling dominates tiny 1m-vs-5m optical propagation differences",
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="mode",required=True)
    serve = sub.add_parser("serve")
    serve.add_argument("--bind",default="127.0.0.1")
    serve.add_argument("--port",type=int,default=PORT)
    serve.add_argument("--limit",type=int,default=0)
    serve.add_argument("--timeout",type=float,default=60.)
    pr = sub.add_parser("probe")
    pr.add_argument("--host",default="127.0.0.1")
    pr.add_argument("--port",type=int,default=PORT)
    pr.add_argument("--count",type=int,default=100)
    pr.add_argument("--size",type=int,default=512)
    pr.add_argument("--timeout",type=float,default=1.)
    args=p.parse_args()
    if args.mode=="serve":
        result=echo_server(args.bind,args.port,args.limit,args.timeout)
    else:
        result=probe(args.host,args.port,args.count,args.size,args.timeout)
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
