# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (c) 2026 Amy Parker & Adam Hahun Nam

from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, raw

import os

def nfqp_test(p):
    print(p)
    print(p.get_payload())
    p.accept()

def nfqp_test_rst_no_keras(p):
    pl = p.get_payload()
    if b"GET /.keras" not in pl:
        p.accept()
        return
    rx = IP(pl)
    tx = (
        IP(
            src=rx.src,
            dst=rx.dst
        ) /
        TCP(
            sport = rx[TCP].sport,
            dport = rx[TCP].dport,
            flags="R",
            seq=rx[TCP].seq
        )
    )
    p.set_payload(raw(tx))
    p.accept()


def launch(f):
    os.system("iptables -I INPUT -d 127.0.0.1/24 -j NFQUEUE --queue-num 63")
    nfq = NetfilterQueue()
    nfq.bind(63, f)
    try:
        nfq.run()
    except KeyboardInterrupt:
        print('')
    nfq.unbind()
    os.system("iptables -D INPUT -d 127.0.0.1/24 -j NFQUEUE --queue-num 63")
