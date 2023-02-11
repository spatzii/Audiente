import pathlib
import datetime


digi24_slots = [{'tronson': "Selectează tronsonul ", 'value': 'dummy'},
                {'tronson': '2:00 - 6:00', 'loc_q': list(range(0, 17))},
                {'tronson': '6-9 Matinal', 'loc_q': list(range(17, 30)), 'loc_m': list(range(0, 180))},
                {'tronson': '9-12 Știrile Dimineții', 'loc_q': list(range(30, 43)), 'loc_m': list(range(180, 360))},
                {'tronson': '12-15 Știrile Amiezii', 'loc_q': list(range(43, 56)), 'loc_m': list(range(360, 540))},
                {'tronson': 'Studio Politic', 'loc_q': list(range(56, 61)), 'loc_m': list(range(540, 600))},
                {'tronson': '16-19 Știrile Zilei', 'loc_q': list(range(61, 74)), 'loc_m': list(range(600, 780))},
                {'tronson': 'Business Club', 'loc_q': list(range(74, 79)), 'loc_m': list(range(780, 840))},
                {'tronson': 'Jurnalul de Seară', 'loc_q': list(range(79, 92)), 'loc_m': list(range(840, 1020))},
                {'tronson': '23:00 Știrile Serii', 'loc_q': list(range(92, 106)), 'loc_m': list(range(1020, 1140))}]

digi24_slot_names = [x.get('tronson') for x in digi24_slots]

all_channels = [{'tv': 'Digi 24', 'loc': 2}, {'tv': 'Antena 3 CNN', 'loc': 3},
                {'tv': 'B1TV', 'loc': 4}, {'tv': 'Realitatea Plus', 'loc': 5},
                {'tv': 'Romania TV', 'loc': 6}]




