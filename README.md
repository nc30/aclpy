## Examples

```
$ cat example_list.txt 
192.168.1.0 255.255.255.0 10.10.3.0 255.255.0.0
inside-in permit tcp 192.168.1.1 10.10.20.0 255.255.254.0 eq 5020
inside-in permit tcp 192.168.1.2 10.10.10.0 255.255.255.0 eq 5020
inside-in permit tcp 192.168.1.3 255.255.255.0 10.10.10.0 255.255.255.0 eq 5020
access-list cached ACL log flows: total 0, denided 0 (deny-flow-max 4096) alert interval 300
access-list inside-in; 9 elements; name hash: 0x532f06a
access-list inside-in line 1 extended permit icmp 192.168.208.0 255.255.255.0 host 172.3.3.1 log informational interval 300 (hitcnt=0) 0xcd28675c
access-list inside-in line2 extended permit tcp host 192.168.1.1. host 172.2.2.1 range ftp-data ftp log informational interval

$ python3 main.py -i example_list.txt 192.168.1.1
1: 192.168.1.0 255.255.255.0 10.10.3.0 255.255.0.0
2: inside-in permit tcp 192.168.1.1 10.10.20.0 255.255.254.0 eq 5020
4: inside-in permit tcp 192.168.1.3 255.255.255.0 10.10.10.0 255.255.255.0 eq 5020

```

or:

```
$ cat example_list.txt | python3 main.py 192.168.1.1
```
