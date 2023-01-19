import os


#################################  Plate boundary files  #######################################
PLATE_BOUNDARY_FILE = {
    'GSRM'   : os.path.abspath('./plate_boundary/GSRM/plate_outlines.lola'),
    'MORVEL' : os.path.abspath('./plate_boundary/MORVEL/plate_outlines.lalo'),
}

#################################  Plate Motion Models  ########################################
# Later will be moved to a separate script `pmm.py` in plate motion package

# 1). ITRF2014-PMM defined in Altamimi et al. (2017)
# Reference frame: ITRF2014
Tag = collections.namedtuple('Tag', 'Abbrev num_site omega_x omega_y omega_z omega wrms_e wrms_n')
ITRF2014_PMM = {
    'Antartica'     : Tag('ANTA'  ,   7,  -0.248,  -0.324,   0.675,  0.219,  0.20,  0.16),
    'Arabia'        : Tag('ARAB'  ,   5,   1.154,  -0.136,   1.444,  0.515,  0.36,  0.43),
    'Australia'     : Tag('AUST'  ,  36,   1.510,   1.182,   1.215,  0.631,  0.24,  0.20),
    'Eurasia'       : Tag('EURA'  ,  97,  -0.085,  -0.531,   0.770,  0.261,  0.23,  0.19),
    'India'         : Tag('INDI'  ,   3,   1.154,  -0.005,   1.454,  0.516,  0.21,  0.21),
    'Nazca'         : Tag('NAZC'  ,   2,  -0.333,  -1.544,   1.623,  0.629,  0.13,  0.19),
    'NorthAmerica'  : Tag('NOAM'  ,  72,   0.024,  -0.694,  -0.063,  0.194,  0.23,  0.28),
    'Nubia'         : Tag('NUBI'  ,  24,   0.099,  -0.614,   0.733,  0.267,  0.28,  0.36),
    'Pacific'       : Tag('PCFC'  ,  18,  -0.409,   1.047,  -2.169,  0.679,  0.36,  0.31),
    'SouthAmerica'  : Tag('SOAM'  ,  30,  -0.270,  -0.301,  -0.140,  0.119,  0.34,  0.35),
    'Somalia'       : Tag('SOMA'  ,   3,  -0.121,  -0.794,   0.884,  0.332,  0.32,  0.30),
}
PMM_UNIT = {
    'omega'   : 'deg/Ma',  # degree per megayear or one-million-year
    'omega_x' : 'mas/yr',  # milli-arcsecond per year
    'omega_y' : 'mas/yr',  # milli-arcsecond per year
    'omega_z' : 'mas/yr',  # milli-arcsecond per year
    'wrms_e'  : 'mm/yr',   # milli-meter per year, weighted root mean scatter
    'wrms_n'  : 'mm/yr',   # milli-meter per year, weighted root mean scatter
}


# 2). GSRMv2.1 defined in Kreemer et al. (2014)
# Reference frame: IGS08
# (unit: Lat: °N; Lon: °E; omega: °/Ma)
Tag = collections.namedtuple('Tag', 'Abbrev Lat Lon omega')
GSRM_V21_PMM = {
    'Africa'          : Tag('AF'  , 49.66   ,  -78.08   , 0.285),
    'Amur'            : Tag('AM'  , 61.64   ,  -101.29  , 0.287),
    'Antarctica'      : Tag('AN'  , 60.08   ,  -120.14  , 0.234),
    'Arabia'          : Tag('AR'  , 51.12   ,  -19.87   , 0.484),
    'AegeanSea'       : Tag('AS'  , 47.78   ,  59.86    , 0.253),
    'Australia'       : Tag('AU'  , 33.31   ,  36.38    , 0.639),
    'BajaCalifornia'  : Tag('BC'  , -63.04  ,  104.02   , 0.640),
    'Bering'          : Tag('BG'  , -40.62  ,  -53.84   , 0.333),
    'Burma'           : Tag('BU'  , -4.38   ,  -76.17   , 2.343),
    'Caribbean'       : Tag('CA'  , 37.84   ,  -96.49   , 0.290),
    'Caroline'        : Tag('CL'  , -76.41  ,  30.22    , 0.552),
    'Cocos'           : Tag('CO'  , 27.21   ,  -124.02  , 1.169),
    'Capricorn'       : Tag('CP'  , 42.13   ,  24.28    , 0.622),
    'Danakil'         : Tag('DA'  , 21.80   ,  36.05    , 2.497),
    'Easter'          : Tag('EA'  , 25.14   ,  67.55    , 11.331),
    'Eurasia'         : Tag('EU'  , 55.38   ,  -95.41   , 0.271),
    'Galapagos'       : Tag('GP'  , 2.83    ,  81.26    , 5.473),
    'Gonave'          : Tag('GV'  , 23.89   ,  -84.86   , 0.476),
    'India'           : Tag('IN'  , 50.95   ,  -8.00    , 0.524),
    'JuandeFuca'      : Tag('JF'  , -37.71  ,  59.44    , 0.977),
    'JuanFernandez'   : Tag('JZ'  , 34.33   ,  70.76    , 22.370),
    'Lwandle'         : Tag('LW'  , 52.20   ,  -60.68   , 0.273),
    'Mariana'         : Tag('MA'  , 11.20   ,  142.82   , 2.165),
    'NorthAmerica'    : Tag('NA'  , 2.19    ,  -83.75   , 0.219),
    'NorthBismarck'   : Tag('NB'  , -30.20  ,  135.30   , 1.201),
    'Niuafo`ou'       : Tag('NI'  , -3.51   ,  -174.04  , 3.296),
    'Nazca'           : Tag('NZ'  , 49.05   ,  -102.13  , 0.611),
    'Okhotsk'         : Tag('OK'  , 28.80   ,  -90.91   , 0.209),
    'Okinawa'         : Tag('ON'  , 39.11   ,  145.94   , 1.361),
    'Pacific'         : Tag('PA'  , -63.09  ,  109.63   , 0.663),
    'Panama'          : Tag('PM'  , 16.55   ,  -84.30   , 1.392),
    'PuertoRico'      : Tag('PR'  , 27.81   ,  -81.51   , 0.502),
    'PhilippineSea'   : Tag('PS'  , -46.62  ,  -28.39   , 0.895),
    'Rivera'          : Tag('RI'  , 20.27   ,  -107.10  , 4.510),
    'Rovuma'          : Tag('RO'  , 51.72   ,  -69.88   , 0.270),
    'SouthAmerica'    : Tag('SA'  , -14.10  ,  -117.86  , 0.123),
    'SouthBismarck'   : Tag('SB'  , 6.91    ,  -32.41   , 6.665),
    'Scotia'          : Tag('SC'  , 23.02   ,  -98.78   , 0.122),
    'Sinai'           : Tag('SI'  , 53.34   ,  -7.27    , 0.476),
    'Sakishima'       : Tag('SK'  , 27.31   ,  128.68   , 7.145),
    'Shetland'        : Tag('SL'  , 66.05   ,  134.03   , 1.710),
    'Somalia'         : Tag('SO'  , 47.59   ,  -94.36   , 0.346),
    'SolomonSea'      : Tag('SS'  , -3.33   ,  130.60   , 1.672),
    'Satunam'         : Tag('ST'  , 36.68   ,  135.30   , 2.846),
    'Sunda'           : Tag('SU'  , 51.11   ,  -91.75   , 0.350),
    'Sandwich'        : Tag('SW'  , -30.11  ,  -35.58   , 1.369),
    'Tonga'           : Tag('TO'  , 26.38   ,  4.27     , 8.853),
    'Victoria'        : Tag('VI'  , 44.96   ,  -102.19  , 0.330),
    'Woodlark'        : Tag('WL'  , -1.62   ,  130.63   , 1.957),
    'Yangtze'         : Tag('YA'  , 64.76   ,  -109.19  , 0.335),
}


# 3). NNR-MORVEL56 defined in Argus et al. (2011)
# (unit: Lat: °N; Lon: °E; omega: °/Ma)
# Note: we use "NU", instead of "nb" from Argus et al. (2011), for Nubia plate
#   to distinguish from "NB" for North Bismarck plate.
Tag = collections.namedtuple('Tag', 'Abbrev Lat Lon omega')
NNR_MORVEL56_PMM = {
    'Amur'            : Tag('AM'  , 63.17   , -122.82   , 0.297),
    'Antarctica'      : Tag('AN'  , 65.42   , -118.11   , 0.250),
    'Arabia'          : Tag('AR'  , 48.88   , -8.49     , 0.559),
    'Australia'       : Tag('AU'  , 33.86   , 37.94     , 0.632),
    'Capricorn'       : Tag('CP'  , 44.44   , 23.09     , 0.608),
    'Caribbean'       : Tag('CA'  , 35.20   , -92.62    , 0.286),
    'Cocos'           : Tag('CO'  , 26.93   , -124.31   , 1.198),
    'Eurasia'         : Tag('EU'  , 48.85   , -106.50   , 0.223),
    'India'           : Tag('IN'  , 50.37   , -3.29     , 0.544),
    'JuandeFuca'      : Tag('JF'  , -38.31  , 60.04     , 0.951),
    'Lwandle'         : Tag('LW'  , 51.89   , -69.52    , 0.286),
    'Macquarie'       : Tag('MQ'  , 49.19   , 11.05     , 1.144),
    'Nazca'           : Tag('NZ'  , 46.23   , -101.06   , 0.696),
    'NorthAmerica'    : Tag('NA'  , -4.85   , -80.64    , 0.209),
    'Nubia'           : Tag('NU'  , 47.68   , -68.44    , 0.292),
    'Pacific'         : Tag('PA'  , -63.58  , 114.70    , 0.651),
    'PhilippineSea'   : Tag('PS'  , -46.02  , -31.36    , 0.910),
    'Rivera'          : Tag('RI'  , 20.25   , -107.29   , 4.536),
    'Sandwich'        : Tag('SW'  , -29.94  , -36.87    , 1.362),
    'Scotia'          : Tag('SC'  , 22.52   , -106.15   , 0.146),
    'Somalia'         : Tag('SM'  , 49.95   , -84.52    , 0.339),
    'SouthAmerica'    : Tag('SA'  , -22.62  , -112.83   , 0.109),
    'Sunda'           : Tag('SU'  , 50.06   , -95.02    , 0.337),
    'Sur'             : Tag('SR'  , -32.50  , -111.32   , 0.107),
    'Yangtze'         : Tag('YZ'  , 63.03   , -116.62   , 0.334),
    'AegeanSea'       : Tag('AS'  , 19.43   , 122.87    , 0.124),
    'Altiplano'       : Tag('AP'  , -6.58   , -83.98    , 0.488),
    'Anatolia'        : Tag('AT'  , 40.11   , 26.66     , 1.210),
    'BalmoralReef'    : Tag('BR'  , -63.74  , 142.06    , 0.490),
    'BandaSea'        : Tag('BS'  , -1.49   , 121.64    , 2.475),
    'BirdsHead'       : Tag('BH'  , -40.00  , 100.50    , 0.799),
    'Burma'           : Tag('BU'  , -6.13   , -78.10    , 2.229),
    'Caroline'        : Tag('CL'  , -72.78  , 72.05     , 0.607),
    'ConwayReef'      : Tag('CR'  , -20.40  , 170.53    , 3.923),
    'Easter'          : Tag('EA'  , 24.97   , 67.53     , 11.334),
    'Futuna'          : Tag('FT'  , -16.33  , 178.07    , 5.101),
    'Galapagos'       : Tag('GP'  , 2.53    , 81.18     , 5.487),
    'JuanFernandez'   : Tag('JZ'  , 34.25   , 70.74     , 22.368),
    'Kermadec'        : Tag('KE'  , 39.99   , 6.46      , 2.347),
    'Manus'           : Tag('MN'  , -3.67   , 150.27    , 51.569),
    'Maoke'           : Tag('MO'  , 14.25   , 92.67     , 0.774),
    'Mariana'         : Tag('MA'  , 11.05   , 137.84    , 1.306),
    'MoluccaSea'      : Tag('MS'  , 2.15    , -56.09    , 3.566),
    'NewHebrides'     : Tag('NH'  , 0.57    , -6.60     , 2.469),
    'Niuafo`ou'       : Tag('NI'  , -3.29   , -174.49   , 3.314),
    'NorthAndes'      : Tag('ND'  , 17.73   , -122.68   , 0.116),
    'NorthBismarck'   : Tag('NB'  , -45.04  , 127.64    , 0.856),
    'Okhotsk'         : Tag('OK'  , 30.30   , -92.28    , 0.229),
    'Okinawa'         : Tag('ON'  , 36.12   , 137.92    , 2.539),
    'Panama'          : Tag('PM'  , 31.35   , -113.90   , 0.317),
    'Shetland'        : Tag('SL'  , 50.71   , -143.47   , 0.268),
    'SolomonSea'      : Tag('SS'  , -2.87   , 130.62    , 1.703),
    'SouthBismarck'   : Tag('SB'  , 6.88    , -31.89    , 8.111),
    'Timor'           : Tag('TI'  , -4.44   , 113.50    , 1.864),
    'Tonga'           : Tag('TO'  , 25.87   , 4.48      , 8.942),
    'Woodlark'        : Tag('WL'  , 0.10    , 128.52    , 1.744),
}
