# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2026 Amy Parker & Adam Hahun Nam

from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, UDP, raw
from bitarray import bitarray

import os

def nfqp_test_no_reject(p) -> None:
    print(p)
    print(p.get_payload())
    p.accept()

def nfqp_test_rst_no_keras(p) -> None:
    pl = p.get_payload()
    if b"GET /.keras" in pl:
        return rst(p)
    p.accept()

def nfqp_test_rst_no_openvpn(p) -> None:
    pk = IP(p.get_payload())
    udp = False
    if pk.haslayer(UDP):
        pl = bytes(pk[UDP].payload)
        udp = True
    elif pk.haslayer(TCP):
        pl = bytes(pk[TCP].payload)
    else:
        return p.accept()
    # not a perfect wireshark-like detection
    # but works as an example
    # will have collateral damage of up to 9% of
    # packets with payloads
    if len(pl) > 0 and pl[0] >> 3 in (1,7,8):
        if udp:
            return p.drop()
        else:
            return rst(p)
    p.accept()

def nfqp_test_gfw_popcount_simplified(p) -> None:
    bits = bitarray()
    pl = p.get_payload()
    bits.frombytes(pl)
    r = bits.count() / len(pl)
    # without active mitigations like in the gfw,
    # horrendous collateral damage
    if r > 3.4 and r < 4.6:
        return p.drop()
    p.accept()

def rst(p) -> None:
    rx = IP(p.get_payload())
    p.set_payload(
        raw(
            (IP(src=rx.src,dst=rx.dst) /
             TCP(sport=rx[TCP].sport,dport=rx[TCP].dport,flags="R",seq=rx[TCP].seq))
        )
    )
    p.accept()

# note: only applies to v4 traffic for now
# would simply need to add an ip6 rule to q63
# must be invoked from a process running as root or that has iptables perms
def launch(f):
    os.system("iptables -I INPUT -d 0.0.0.0/0 -j NFQUEUE --queue-num 63")
    nfq = NetfilterQueue()
    nfq.bind(63, f)
    try:
        nfq.run()
    except KeyboardInterrupt:
        print('')
    nfq.unbind()
    os.system("iptables -D INPUT -d 0.0.0.0/0 -j NFQUEUE --queue-num 63")
