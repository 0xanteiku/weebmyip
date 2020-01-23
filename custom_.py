import radix
import os
from config import db_dir
from ipaddress import ip_address


class dedasn():
    asn_isp_url = "http://thyme.apnic.net/current/data-used-autnums"
    ip_asn_url = "http://thyme.apnic.net/current/data-raw-table"
    asn_isp_db = "asn_isp_db"
    isp_asn_db = "isp_asn_db"

    def __init__(self):
        self._cache_dir = db_dir
        self.asn_isp_raw = open(db_dir+self.asn_isp_db, 'rb').read()
        self.isp_asn_raw = open(db_dir+self.isp_asn_db, 'rb').read()
        self._build_radix_tree(self.asn_isp_raw, self.isp_asn_raw)

    def _build_radix_tree(self, asn_isp_raw, ip_asn_raw):
        self._rtree = radix.Radix()
        # build the asn -> ISP lookup
        asn_isp_map = {}
        lines = asn_isp_raw.decode('utf-8', 'ignore').splitlines()
        for line in lines:
            tokens = line.split()
            try:
                asn = int(line[:6])
            except Exception:
                continue
            isp = line[7:]
            asn_isp_map[asn] = isp
        # build the ipaddr -> ASN lookup
        lines = ip_asn_raw.decode('utf-8', 'ignore').splitlines()
        for line in lines:
            tokens = line.split()
            ipmask = tokens[0]
            asn = int(tokens[1])
            rnode = self._rtree.add(ipmask)
            rnode.data['asn'] = asn
            try:
                rnode.data['isp'] = asn_isp_map[asn]
            except Exception:
                rnode.data['isp'] = ''

    def _save_files(self, asn_isp_raw, ip_asn_raw):
        if self._cache_dir is None:
            return
        asn_isp_file = os.path.join(self._cache_dir, self.asn_isp_db)
        ip_asn_file = os.path.join(self._cache_dir, self.isp_asn_db)

        with open(asn_isp_file, 'wb') as f:
            f.write(asn_isp_raw)

        with open(ip_asn_file, 'wb') as f:
            f.write(ip_asn_raw)

    def isp(self, ipaddress):
        ipaddress = str(ip_address(ipaddress))
        rnode = self._rtree.search_best(ipaddress)
        if rnode is None:
            return None
        data_o = {'asn': rnode.data['asn'], 'isp': rnode.data['isp']}
        return data_o
