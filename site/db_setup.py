from schmao import db

# Drop entirety of database
db.session.close()
db.drop_all()

# Recreate database
db.create_all()

from schmao.models import *

# Set up challenges
challs = [

	Challenge("Hitman", 
"""76 111 111 107 44 32 97 32 115 117 112 101 114 109 111 100 101 108 33 32 76 111 111 107 44 32 97 32 104 111 118 101 114 98 111 97 114 100 33 32 76 111 111 107 44 32 116 104 101 32 97 112 111 99 97 108 121 112 115 101 33 32 83 111 109 101 111 110 101 32 103 111 116 32 104 105 116 32 105 110 32 116 104 101 32 98 111 105 110 103 108 111 105 110 103 115 33 32 72 105 116 32 105 110 32 116 104 101 32 98 111 105 110 103 108 111 105 110 103 115 33 32 66 111 105 110 103 108 111 105 110 103 115 33 32 66 111 105 110 103 108 111 105 110 103 115 33 32 83 111 109 101 98 111 100 121 32 103 111 116 32 104 105 116 32 105 110 32 116 104 101 109 46 32 80 101 97 99 101 32 111 117 116 33 

98 48 105 110 103 108 48 105 110 103 115 95 98 48 105 110 103 108 48 105 110 103 115 95 98 48 105 110 103 108 48 105 110 103 115""",
	100, 'Crypto', '', 'b0ingl0ings_b0ingl0ings_b0ingl0ings'), 

	Challenge("Gossip", 
"""Lumpy Space Princess sent an insanely important secret letter to Ghost Princess but the courier got eaten alive by pixies! And what's worse, he's the only one who knew the key!"

We recovered the encryption scheme and the ciphertext, please recover the message as quickly as possible!

2106191b4e240e1b041143281b070d051104164f5863210b4a541a1c433f0501014a541213060a491d0a081712452014081c024607030a13080c0a430315030c0d1f49030607005b4569100c1c43151f1e0b43140601081554040a431f06010747543e450e1d08004f46071f00430b1d070f0a541b0a0c131a4e0507005b45010d1d42430a1d1c004f586327430515194217581a0f1a46001f041758031b0d0d54030a43100c1c43001514004d72633d0a0817121706141042436c3824356972413e4d355a5709571c005d103918471306271d0650392c47374a72""",
	300, 'Crypto', '', 'l4di3s_l0ve_th3_X0R'),

	Challenge("Enc0ded", 
"""BMO told us this server would send us a flag but its just sending us some stupid flipping picture! Would you straighten this out?

host:ip""",
	100, 'Forensics', '', 'b4bby5_f1rs7_b4rc0de_fl4g'),

	Challenge("Unacceptable", 
"""We've pulled the ultimate prank on mandatory! It'll probably get us one million years dungeon if he sees it, so we've hidden it in this pcap.""",
	100, 'Forensics', '', 'mandatorys_mother'),

	Challenge("Selfie", 
"""We've intercepted a message Ice King sent to one of his penguins but we can't decode it! Apparently none of the banana guards know how to work the pre-Mushroom War satellites. We have the message file but it's a little chopped up...""",
	200, 'Forensics', '', 'sewer_under_candy_kingdom'),

	Challenge("Marceline", 
"""""", 
	300, 'Forensics', '', ''),

	Challenge("Riddle", 
"""Solve the riddle... or just get the flag. 

host:ip""",
	100, 'Pwnable', '', 'ye3h_r1gh7_1ve_g0t_a_mi55il3!!'),

	Challenge("Diary?", 
"""BMO was scanning the internet earlier when he stumbled across someone's secret online diary! There's gotta be a flag around here somewhere, but... this diary is just so... disturbing.

host:ip""", 
	200, 'Pwnable', '', 'wh4t_th3_s7uff_am_1_r34d1ng?!?'),

	Challenge("Wenkbot", 
"""""", 
	200, 'Pwnable', '', ''),

	Challenge("Wizards Only", 
"""""",
	300, 'Pwnable', '', ''),

	Challenge("flag_gen", 
"""I paid the new intern to make me a flag generator... that was my first mistake.""", 
	100, 'Reverse', '', 'gr33tings_y0ung_her0_to_b3'),

	Challenge("Princess Tracker", 
"""The Ice King forgot his username and password for his Princess Tracker! Help him get it back so he can get some princess action.""",
	200, 'Reverse', '', 'ice_king_and_bubblegum_forever'),

	Challenge("Imagination Machine", 
"""The Imagination Machine is going bananas! Hopefully you can set it straight!

host:ip""",
	300, 'Reverse', '', '4nci3nt_psych1c_t4nd3m_w4r_el3ph4nt_any0ne?'),

	Challenge("Bad Cookie", 
"""Finn and Jake are trying to get in to Wizard City, but they know the rules - wizards only, fools. Help them get in.

host:ip""", 
	100, 'Web', '', 'w1z4rdz__rul3'),

	Challenge("http://iceking.wenk", 
"""""", 
	200, 'Web', '', ''),

	Challenge("OooSQL", 
"""I think my dad is going to kill everyone or whatever. Maybe you can stop him if you hack his OooSQL account.

marceline:daddyslittlemonster
host""", 
	300, 'Web', '', '0ffer_y0ur_s0ul_t0_m3_d4rk_0ne')
]

# Add all challenges
for item in challs:
	db.session.add(item)

db.session.commit()