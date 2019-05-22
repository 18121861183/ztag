#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import pkgutil
import os
import os.path
import imp
import ztag.annotations

from ztag import protocols
from ztag.errors import InvalidTag


class MetadataBase(object):

    def __init__(self):
        self.manufacturer = None
        self.product = None
        self.version = None
        self.revision = None
        self._description = None

    @property
    def description(self):
        # Populate the description field
        desc_fields = [
            self.manufacturer,
            self.product,
            self.version,
            self.revision,
        ]
        populated_fields = [field for field in desc_fields if field]
        if populated_fields:
            return " ".join(populated_fields)
        return None

    def merge(self, other):
        if self.manufacturer is None:
            self.manufacturer = other.manufacturer
        if self.product is None:
            self.product = other.product
        if self.version is None:
            self.version = other.version
        if self.revision is None:
            self.revision = other.revision

    def to_dict(self, with_description=True):
        out = dict()
        if self.manufacturer is not None:
            out['manufacturer'] = self.manufacturer
        if self.product is not None:
            out['product'] = self.product
        if self.version is not None:
            out['version'] = self.version
        if self.revision is not None:
            out['revision'] = self.revision
        if len(out) > 0 and with_description:
            out['description'] = self.description
        return out


class LocalMetadata(MetadataBase):

    def __init__(self):
        super(LocalMetadata, self).__init__()


class GlobalMetadata(MetadataBase):

    def __init__(self):
        super(GlobalMetadata, self).__init__()
        self.os = None
        self.os_version = None
        self.device_type = None

    def merge(self, other):
        super(GlobalMetadata, self).merge(other)
        if self.os is None:
            self.os = other.os
        if self.os_version is None:
            self.os_version = other.os_version
        if self.device_type is None:
            self.device_type = other.device_type

    def to_dict(self, with_description=True):
        out = super(GlobalMetadata, self)\
                .to_dict(with_description=with_description)
        if self.os is not None:
            out['os'] = self.os
        if self.os_version is not None:
            out['os_version'] = self.os_version
        if self.device_type is not None:
            out['device_type'] = self.device_type
        return out


class Metadata(object):

    def __init__(self):
        self.local_metadata = LocalMetadata()
        self.global_metadata = GlobalMetadata()
        self.tags = set()

    def merge(self, other):
        self.local_metadata.merge(other.local_metadata)
        self.global_metadata.merge(other.global_metadata)
        self.tags |= other.tags

    def empty(self):
        if len(self.local_metadata.to_dict()) == 0 \
                and len(self.global_metadata.to_dict()) == 0:
            return True
        else:
            return False


# types of devices, e.g., primary purpose of an embedded device
class Type(object):

    ACCESS_CONTROL = "访问控制器"
    ALARM_SYSTEM = "服务器"
    CABLE_MODEM = "ADSL"
    CAMERA = "Camera"
    CFS = "CFS"
    CINEMA = "cinema"
    DSL_MODEM = "ADSL"
    DVR = "DVR"
    ENVIRONMENT_MONITOR = "服务器"
    FIRE_ALARM = "服务器"
    FIREWALL = "Firewall"
    GENERIC_PRINTER = "Printer"
    HMI = "控制器"
    HVAC = "hvac"
    INDUSTRIAL_CONTROL = "控制器"
    INFRASTRUCTURE_ROUTER = "Router"
    INKJET_PRINTER = "Printer"
    IPMI = "IPMI"
    KVM = "KVM"
    LASER_PRINTER = "Printer"
    LIGHT_CONTROLLER = "控制器"
    MODEM = "ADSL"
    MUTLIFUNCTION_PRINTER = "Printer"
    NAS = "NAS"
    NETWORK = "网络设备"
    NETWORK_ANALYZER = "服务器"
    PDU = "工业控制器"
    PHASER_PRINTER = "Printer"
    PLC = "工业控制器"
    POWER_CONTROLLER = "工业控制器"
    POWER_MONITOR = "工控设备"
    PRINT_SERVER = "Printer"
    PRINTER = "Printer"
    RTU = "RTU"
    SCADA_CONTROLLER = "控制器"
    SCADA_FRONTEND = "服务器"
    SCADA_GATEWAY = "Gateway"
    SCADA_PROCESSOR = "服务器"
    SCADA_ROUTER = "Router"
    SCADA_SERVER = "服务器"
    SDS = "SDS"
    SERVER_MANAGEMENT = "IPMI"
    SIGN = "Sign"
    SOHO_ROUTER = "Router"
    SOLAR_PANEL = "嵌入式"
    STORAGE = "NAS"
    SWITCH = "Switch"
    TEMPERATURE_MONITOR = "服务器"
    THERMOSTAT = "IOT"
    TV_BOX = "IOT"
    TV_TUNER = "IOT"
    UPS = "工控设备"
    USB_HUB = "USB"
    VOIP = "VOIP"
    WATER_FLOW_CONTROLLER = "工控设备"
    WIFI = "Wireless Router"
    WIRELESS_MODEM = "Wireless Router"


class Manufacturer(object):
    ABB_STOTZ_KONTAKT = "ABB-Stotz-Kontakt"
    ACTL = "ACTL"
    ADTRAN = "ADTRAN"
    AGRANAT = "Agranat"
    ALCATEL = "Alcatel"
    ALERTON = "Alerton"
    ALLEGRO = "Allegro"
    ALLWORKS = "allworx"
    AMERICANMEGATRENDS = "American-Megatrends-Inc."
    ANNKE = "Annke"
    APACHE = "Apache"
    APC = "APC"
    APPLE = "苹果"
    ARUBA = "Aruba-Networks"
    ASUS = "华硕"
    AVM = "AVM"
    AVTECH = "AVTech"
    AXIS = "Axis"
    BELKIN = "Belkin"
    BIGIP = "BigIP"
    BOMGAR = "Bomgar"
    BROTHER = "Brother"
    CANON = "佳能"
    CHEROKEE = "Cherokee"
    CISCO = "思科"
    CLARIION = "Clariion"
    COMPUTEC = "Computec-OY"
    COMTROL = "Comtrol-Corporation"
    CROUZET = "Crouzet"
    DAHUA = "Dahua-Technology"
    # DAHUA = "Dahua"
    DEDICATED_MICROS = "Dedicated-Micros"
    DELL = "戴尔"
    DIGI = "Digi"
    DISTECH = "Distech-Controls"
    DLINK = "DLink"
    DRAYTEK = "DrayTek"
    DREAMBOX = "DreamBox"
    ECONET = "EcoNet"
    ECOSENSE = "EcoSense"
    EDGEWATER = "Edgewater-Networks"
    EIG = 'Electro Industries GaugeTech'
    EIQ = "eIQ"
    EMC = "EMC"
    EMERSON = "Emerson"
    ENTES = "Entes"
    ENTROLINK = "Entrolink"
    EPSON = "Epson"
    FACEXP = "FacExp"
    FIBERCOM = "Fiberhome-Telecom-Tech"
    FLEXIM = "Flexim"
    FULLRATE = "FullRate"
    GE = "GE"
    GEOVISION = 'Geovision'
    HANBANGGAOKE = "hanbanggaoke"
    HIKVISION = "Hikvision"
    HONEYWELL = "Honeywell"
    HP = "Hewlett-Packard"
    # HP = "HP"
    HUAWEI = "华为"
    IBM = "IBM"
    INTEG = "INTEG"
    INTEGRA = "Integra"
    INTELBRAS = "Intelbras"
    INTERCON = "Intercon"
    IPTIME = "IPTime"
    IQEYE = "IQeye"
    IXSYSTEM = "Ixsystem"
    JUNGO = "Jungo"
    KEDA = "keda"
    KONICA_MINOLTA = "Konica-Minolta"
    LAB_EL = "LAB-EL"
    LACIE = "LaCie"
    LANCOM = "Lancom-Systems"
    LANTRONIX = "Lantronix"
    LEIGHTRONIX = "Leightronix"
    LENOVO = "联想"
    LEXMARK = "Lexmark"
    LIFESIZE = "LifeSize"
    LINKSYS = "Linksys"
    LUTRON = "Lutron"
    MAYGION = "Maygion"
    MCGS = 'MCGS'
    MICROSOFT = "微软"
    MIKROTIK = "MikroTik"
    MOTOROLA = "Motorola"
    MULTITECH = "Multitech"
    NATIONAL_INSTRUMENTS = "National-Instruments"
    NETAPP = "Net-App"
    NETGEAR = "NetGear"
    NETKLASS = "NetKlass"
    NETWAVE = "Netwave"
    NEXREV = "NexRev"
    NGINX = "Nginx"
    NIVUS = "Nivus"
    NOVAR = "Novar"
    NRG_SYSTEMS = "nrg-systems"
    OPTO22 = "Opto22"
    OSNEXUS = "Osnexus"
    OVERLAND_STORAGE = "Overland-Storage"
    PANABIT = "Panabit"
    PANASONIC = "Panasonic"
    PANO_LOGIC = "Pano-Logic"
    POLABS = "PoLabs"
    POLYCOM = "Polycom"
    QNAP = "QNAP"
    RARITAN = "Raritan"
    REALTEK = "Realtek"
    RICOH = "Ricoh"
    ROCKWELL = "Rockwell"
    ROOMWIZARD = "RoomWizard"
    ROUTER_BOARD = "routerboard"
    SANGFOR = "Sangfor"
    SAP = 'SAP'
    SCANNEX = "Scannex"
    SCHNEIDER = "Schneider-Electric"
    SE_ELECTRONIC = "SE-Electronic"
    SEAGATE = "Seagate"
    SENSATRONICS = "Sensatronics"
    SERCOMM = "Sercomm"
    SHARP = "Sharp"
    SIEMENS = "Siemens"
    SOFT_AT_HOME = "SoftAtHome"
    SOLAR_LOG = "Solar-Log"
    SOMFY = "Somfy"
    SONUS = "SONUS"
    SONY = "索尼"
    SPEEDPORT = "SpeedPort"
    SUN_MICROSYSTEMS = "Sun-Microsystems"
    SUPERMICRO = "SuperMicroComputer"
    SUPERMICROCOMPUTER = "SuperMicroComputer"
    # SUPERMICROCOMPUTER = "SuperMicroComputer"
    SYNCHRONIC = "Synchronic"
    SYNOLOGY = "Synology"
    TANDBERG_DATA = "Tandberg-Data"
    TECHNICOLOR = "Technicolor"
    TELEMECANIQUE = "Telemecanique"
    TELRAD = "Telrad"
    THECUS = "Thecus"
    THINK_SIMPLE = "Think-Simple"
    TIANDY = "Tiandy"
    TIVO = "TiVo"
    # TPLINK = "TPLink"
    TPLINK = "TP-LINK"
    TRANE = "Trane"
    TREND = "Trend"
    TRENDCHIP = "TrendChip"
    TRIDIUM = "Tridium"
    UBIQUITI = "Ubiquiti-Networks"
    UNIVIEW = "Uniview"
    VARNISH = "Varnish"
    VERIS = "Veris-Industries"
    VIA = "Via"
    VIRITA = "Virata"
    VODAPHONE = "VodaPhone"
    VSTARCAM = "Vstarcam"
    VYKON = "Vykon"
    WATTSTOPPER = "WattStopper"
    WD = "西部数据"
    # WD = "Western Digital"
    WEBEASY = "Webeasy"
    WEG = "WEG"
    WESTERN_DIGITAL = "西部数据"
    WIND_RIVER = "Wind-River"
    WURM = "Wurm"
    XEROX = "Xerox"
    ZTE = "中兴"
    ZYXEL = "ZyXEL"


class ScadaProduct(object):
    SHUIWU = 'Waterpower'
    HUAGONG = 'Chemical'
    QIXIANG = 'Weather'
    DIANLI = 'Electric'
    RANQI = 'Gas'
    SHIYOU = 'Petroleum'
    ZAIHAI = 'Disaster'
    YEJIN = 'Metallurgy'
    YANCAO = 'Tobacco'
    GPS = 'GPS'
    YILIAO = 'Medicine'


class OperatingSystem(object):
    # Linuxes
    ARCH = "Arch Linux"
    DEBIAN = "Debian"
    FEDORA = "Fedora"
    GENTOO = "Gentoo"
    KALI = "Kali Linux"
    MANDRIVE = "Mandriva"
    REDHAT = "RedHat"
    CENTOS = "CentOS"
    SUNOS = "SunOS"
    SUSE = "openSUSE"
    UBUNTU = "Ubuntu"
    # UCLINUX = "uClinux"
    RASPBIAN = "Raspbian"
    # BSDs
    FREEBSD = "FreeBSD"
    NETBSD = "NetBSD"
    OPENBSD = "OpenBSD"
    SLACKWARE = "Slackware"
    # Other Unixes
    HPUX = "HP-UX"
    VXWORKS = "VXWORKS"
    # Windows
    WINDOWS = "Windows"
    WINDOWS_SERVER = "Windows Server"
    UCLINUX = "UClinux"
    TIMOS = "TiMOS"
    # RTOS's
    QNX = "QNX"
    # Router OSes
    CISCO_IOS = "Cisco IOS"
    MIKROTIK_ROUTER_OS = "MikroTik RouterOS"
    DOPRA = "Dopra Linux OS" # Huawei


class Annotation(object):

    LOCAL_METADATA_KEYS = [
        "manufacturer",
        "product",
        "version",
        "revision",
        "description"
    ]

    GLOBAL_METADATA_KEYS = [
        "manufacturer",
        "product",
        "version",
        "revision",
        "os",
        "os_version",
        "os_description",
        "device_type",
        "description",
    ]

    port = None
    protocol = None
    subprotocol = None

    name = None

    tests = {}

    # some simple checks
    def check_port(self, port):
        return self.port is None or self.port == port

    def check_protocol(self, protocol):
        return self.protocol is None or self.protocol.value == protocol.value

    def check_subprotocol(self, subprotocol):
        return self.subprotocol is None or self.subprotocol.value == subprotocol.value

    @classmethod
    def iter(cls):
        for klass in cls.find_subclasses():
            if hasattr(klass, "process") and not hasattr(klass, "read_rule"):
                yield klass

    @classmethod
    def itec(cls):
        for klass in cls.find_subclasses():
            if hasattr(klass, "read_rule"):
                yield klass

    @classmethod
    def find_subclasses(cls):
        return set(cls.__subclasses__() + [g for s in cls.__subclasses__()
                                           for g in s.find_subclasses()])

    _annotation_annotations_total = 0
    _annotation_annotations_fail = 0

    @classmethod
    def load_annotations(cls, safe=False):
        def recursive_add(paths, prefix):
            for i, modname, ispkg in pkgutil.iter_modules(paths, prefix):
                if ispkg:
                    inner_paths = [os.path.join(paths[0], modname.split(".")[-1]),]
                    recursive_add(inner_paths, modname+".")
                else:
                    cls._annotation_annotations_total += 1
                    if safe:
                        try:
                            __import__(modname)
                        except:
                            cls._annotation_annotations_fail += 1
                            print "WARNING: unable to import %s" % modname
                    else:
                        __import__(modname)
        recursive_add(ztag.annotations.__path__, "ztag.annotations.")

    def simple_banner_version(self, b, server, meta):
        if b.lower().startswith(server.lower()):
           meta.local_metadata.product = server
           if "/" in b:
               meta.local_metadata.version = b.split("/", 1)[1].strip()
           return meta

    banner_re = re.compile(r"([\w\d_\.-]+)(?:/([\w\d_\.-]+))?(?: \(([\w\d_\.-]+)\))?")

    def http_banner_parse(self, b, meta):
        g = self.banner_re.search(b).groups()
        if g[0]:
           meta.local_metadata.product = g[0]
           meta.local_metadata.version = g[1]
           meta.global_metadata.os = g[2]
           return meta


class TLSTag(Annotation):

    @staticmethod
    def get_subject(d):
        return d["certificate"]["parsed"]["subject"]

    @staticmethod
    def get_sha256p(self, d):
        return d["certificate"]["parsed"]["fingerprint_sha256"]
