Filename
P#_S#_CT.eeg
  
  P# = Participant number
  S# = Sessions number (Session 2 - first EEG session, first cognitive training session or Session 5 - second EEG, 4th cognitive training session)
  CT = Cognitive Training (meditation or audiobook)

Cognitive Training was preceded by Eyes Open/Eyes Closed protocol - triggers demark EO/EC, recording continued into the cognitive training session - triggers demark start and end of cognitive training

For Session 2 Eyes Open/Eyes Closed - measure IAF + overall resting alpha and theta
For Session 5 Eyes Open/Eyes Closed - overall resting alpha and theta
For Cognitive Training in Session 2 and 5 - overall resting alpha and theta

Place into csv/xls to merge with behavioural data
Columns
P# S# IAF S2EO/EC_alpha S2EO/EC_theta S2CT_alpha S2CT_theta S5EO/EC_alpha S5EO/EC_theta S5CT_alpha S5CT_theta

NOTE: due to technical issues some P# might be missing or have corrupt files

IAF start and end triggers. Session 2 only
'ParticipantID': [(EC1-start, EC1-end), (EC2-start, EC2-end)]
{
    'P1': [(11,12), (24,25)],
    'P2': [(12,13), (16,17)],
    'P3': [(7,8), (196,197)],
    'P5': [(3,4), (7,8)],
    'P6': [(3,4), (7,8)],
    'P7': [(3,4), (7,8)],
    'P8': [(4,5), (22,24)],
    'P9': [(3,4), (62,125)],
    'P10': [(3,4), (7,8)],
    'P11': [(3,83), (222,223)],
    'P12': [(3,4), (62,77)],
    'P13': [(42,43), (55,56)],
    'P14': [(3,4), (7,8)],
    'P15': [(20,35), (46,47)],
    'P16': [(3,4), (7,8)],
    'P17': [(3,4), (7,8)],
    'P18': [(3,4), (7,8)],
    'P19': [(3,4), (7,8)],
    'P20': [(3,4), (7,8)],
    'P21': [(3,4), (7,8)],
    'P22': [(3,4), (7,8)],
    'P23': [(4,5), (9,10)],
    'P24': [(3,4), (7,8)],
    'P25': [(3,4), (7,8)],
    'P26': [(3,4), (7,8)],
    'P27': [(3,4), (8,9)],
    'P28': [(3,4), (7,8)],
    'P29': [(3,4), (7,8)],  # No S2, had to use S5
    'P30': [(3,4), (8,9)],
    'P31': [(3,4), (7,8)],
}

Alpha/theta power start and end triggers. -1 means missing data
'ParticipantID': [
    # Session 2
    (EO1-start, EO1-end),  # 0
    (EC1-start, EC1-end),  # 1
    (CT-start, CT-end),    # 2
    (EO2-start, EO2-end),  # 3
    (EC2-start, EC2-end),  # 4
    # Session 5
    (EO1-start, EO1-end),  # 5
    (EC1-start, EC1-end),  # 6
    (CT-start, CT-end),    # 7
    (EO2-start, EO2-end),  # 8
    (EC2-start, EC2-end),  # 9
]

{
    'P1': [
        # Session 2
        (2,7),
        (7,12),
        (13,15),
        (15,20),
        (20,25),
        # Session 5
        (2,7),
        (7,12),
        (13,15),
        (15,20),
        (20,25),
    ],
    'P2': [
        # Session 2
        (11,12),
        (12,13),
        (14,15),
        (15,16),
        (16,17),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P3': [
        # Session 2
        (6,7),
        (7,8),
        (9,196),
        (-1,-1),
        (-1,-1),
        # Session 5
        (2,3),
        (3,4),
        (5,20),
        (20,21),
        (21,31),
    ],
    'P5': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (30,58),
        (58,61),
        (63,319),
        (-1,-1),
        (320,355),
    ],
    'P6': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (-1,-1),
        (6,7),
    ],
    'P7': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P8': [
        # Session 2
        (2,3),
        (3,4),
        (5,21),
        (21,22),
        (22,24),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P9': [
        # Session 2
        (2,3),
        (3,4),
        (5,38),
        (38,62),
        (62,125),
        # Session 5
        (5,6),
        (6,7),
        (8,9),
        (9,10),
        (10,11),
    ],
    'P10': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P11': [
        # Session 2
        (2,3),
        (3,83),
        (91,221),
        (221,222),
        (222,223),
        # Session 5
        (2,3),
        (3,10),
        (11,293),
        (-1,-1),
        (306,308),
    ],
    'P12': [
        # Session 2
        (2,3),
        (3,4),
        (5,36),
        (36,76),
        (-1,-1),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P13': [
        # Session 2
        (41,42),
        (42,43),
        (44,51),
        (51,55),
        (55,56),
        # Session 5
        (2,3),
        (3,7),
        (9,10),
        (10,11),
        (11,12),
    ],
    'P14': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P15': [
        # Session 2
        (19,20),
        (20,35),
        (36,45),
        (45,46),
        (46,47),
        # Session 5
        (2,3),
        (3,4),
        (5,7),
        (7,8),
        (8,9),
    ],
    'P16': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P17': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P18': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P19': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P20': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P21': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P22': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P23': [
        # Session 2
        (2,4),
        (4,5),
        (6,8),
        (8,9),
        (9,10),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P24': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,7),
        (7,8),
        (8,9),
    ],
    'P25': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P26': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P27': [
        # Session 2
        (2,3),
        (3,4),
        (5,7),
        (7,8),
        (8,9),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P28': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P29': [
        # Session 2
        (-1,-1),
        (-1,-1),
        (-1,-1),
        (-1,-1),
        (-1,-1),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P30': [
        # Session 2
        (2,3),
        (3,4),
        (5,7),
        (7,8),
        (8,9),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
    'P31': [
        # Session 2
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
        # Session 5
        (2,3),
        (3,4),
        (5,6),
        (6,7),
        (7,8),
    ],
}
