#!/usr/bin/env python3

import os
import sys

# show: https://docs.python.org/ja/3/howto/argparse.html
import argparse

# show: https://docs.python.org/ja/3/library/re.html
import re

# show: https://docs.python.org/ja/3/library/ipaddress.html
import ipaddress

# show: https://docs.python.org/ja/3/library/re.html#re.compile
ipre = re.compile(r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$')


# custom Exception
class NoMatchException(ValueError):
    pass


def parseLine(line):
    # show: https://qiita.com/kokorinosoba/items/eb72dac6b68fccbac04d
    words = [i for i in line.strip("\r\n").split(' ') if len(i) > 0]

    # tcp/udpやport評価も行う場合はここ以降を修正する
    ips = [i for i in words if ipre.match(i)]

    a = {
        'in': None,
        'out': None,
    }

    if len(ips) == 2:
        a['in'] = ipaddress.ip_network(ips[0], strict=False)
        a['out'] = ipaddress.ip_network(ips[1], strict=False)
        return a

    elif len(ips) == 3:
        pass
        try:
            a['in'] = ipaddress.ip_network(ips[0]+"/"+ips[1], strict=False)
            a['out'] = ipaddress.ip_network(ips[2], strict=False)
            return a
        except ValueError:
            pass

        try:
            a['in'] = ipaddress.ip_network(ips[0], strict=False)
            a['out'] = ipaddress.ip_network(ips[1]+"/"+ips[2], strict=False)
            return a
        except ValueError:
            pass

    elif len(ips) == 4:
        a['in'] = ipaddress.ip_network(ips[0]+"/"+ips[1], strict=False)
        a['out'] = ipaddress.ip_network(ips[2]+"/"+ips[3], strict=False)
        return a

    raise NoMatchException('no match')


def matchLines(lines, search):
    i = 0
    for line in lines:
        i += 1

        # try-except: https://docs.python.org/ja/3/tutorial/errors.html
        try:
            a = parseLine(line)
        except ValueError:
            continue

        if (a['in'] and search in a['in']) or (a['out'] and search in a['out']):
            # show: https://docs.python.org/ja/3/howto/functional.html?highlight=%E3%82%B8%E3%82%A7%E3%83%8D%E3%83%AC%E3%83%BC%E3%82%BF%E3%83%BC#generators
            yield i, line


if __name__ == '__main__':
    r = "\r\n"

    # show: https://docs.python.org/ja/3/howto/argparse.html
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-i', '--input', action='store', default=None, type=argparse.FileType('r'), help="haystack")
    parser.add_argument('ip', help="search ip address")

    args = parser.parse_args()

    # separate pipe and stdin
    if not os.isatty(0):
        # from pipe
        lines = sys.stdin.readlines()
        r = ""
    elif args.input:
        # from argument
        lines = args.input.read().split("\n")
        args.input.close()
    else:
        sys.stderr.write("input not found\r\n")
        parser.print_usage()
        sys.exit(1)

    try:
        search = ipaddress.ip_address(args.ip)
    except ValueError:
        sys.stderr.write(f"{args.ip} is not valid ip address\r\n")
        parser.print_usage()
        sys.exit(1)

    for lNo, line in matchLines(lines, search):
        sys.stdout.write(f"{lNo}: {line}{r}")

