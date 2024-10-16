'''
Various profiles for weapons and targets in WH40K 10th ed
'''



'''
Some notes:
- All melee weapon profiles should have 'ignores_cover': True,
- Use extra_effects for things like hit rerolls from oath of moment, or debuffs from death guard contagion
- ANTI-X is implemented using 'crit_wound_roll': 4+, and simply assuming the target has the X-keyword
'''



# Here are weapon and target profiles containing all possible keywords.  Most keywords have default values of 0 or False.

attack_profile_template = {
    'attacks': 2,                   # NOTE:  use 'num_weapons' to attack multiple times without changing the weapon profile
    'attacks_d3': 0,                # number of d3 dice in the number of attacks
    'attacks_d6': 0,                # number of d6 dice in the number of attacks
    'reroll_attacks': False,        # rerolls number of attacks (if number of attacks used d3 or d6)
    'blast': False,

    'torrent': False,
    'ballistic_skill': 3,
    'crit_hit_roll': 6,             # roll needed to crit
    'hit_reroll_1': False,          # rerolls a 1
    'hit_reroll': True,             # rerolls a miss
    'hit_reroll_no_crit': False,    # rerolls a non-crit
    'lethal_hits': False,
    'sustained_hits': 0,            # the integer indicates the added attacks, NOTE: sus hits d3 is not yet implemented

    'strength': 4,
    'crit_wound_roll': 6,           # use this for any 'ANTI-X' profiles
    'wound_reroll_1': False,
    'wound_reroll': False,
    'wound_reroll_no_crit': False,
    'dev_wounds': False,

    'ap': 3,
    'ignores_cover': True,
    'damage': 1,
    'damage_d6': 1,                 # number of d6 dice in the damage
    'damage_d3': 0,                 # number of d3 dice in the damage
    'damage_reroll': False,
}

target_profile_template = {
    'toughness': 5,
    'armour_save': 2,               # NOTE:  armour, invuln, and fnp of 7 or more means there is no armour/invuln/fnp save.  None also works
    'cover': False,
    'invuln_save': None,
    'halve_damage': False,          # always applied first and rounded up
    'damage_mod': -1,               # damage_mod is always applied after halving damage
    'feel_no_pain': None,
    # 'starting strength': 5,       # TODO: implement 'below_half_strength'.  but does it really matter though?  not unless there are multiple attacking units.
    'unit_wounds_profile': [4, 4, 3, 3, 3],    # target will always be selected first to last (left to right)
}


# Attacks are often modified by abilities, stratagems, etc.  Use this to add new and/or overwrite other keywords.
extra_effects_template = {
    'attacks_mod': 0,               # each 'mod' keyword simply adds its value to its characteristic/roll
    'hit_mod': 0,                   # this adds to the hit roll, but does not change the roll required to crit
    'strength_mod': 0,
    'toughness_mod': 0,
    'wound_mod': 0,                 # this adds to the wound roll, but does not change the roll required to crit wound
    'ap_mod': 0,                    # NOTE: +1 ap_mod improves ap, -1 ap_mod worsens ap
    'armour_mod': 0,                # NOTE: +1 armour_mod worsens armour, -1 armour_mod improves armour
    'damage_mod': 0,
    'halve_damage': False,          # half damage applies before damage_mod
}







##### WEAPON PROFILES #####



### Space Marines ###

sm_bolt_rifle = {
    'attacks': 2,
    'ballistic_skill': 3,
    'strength': 4,
    'ap': 1,
    'damage': 1,
}
sm_astartes_grenade_launcher ={
    'attacks_d3': 1,
    'blast': True,
    'ballistic_skill': 3,
    'strength': 4,
    'ap': 0,
    'damage': 1,
}
sm_ballistus_lascannon = {
    'attacks': 2,
    'ballistic_skill': 3,
    'hit_reroll': True,         # assumes enemy is not below half strength
    'strength': 12,
    'ap': 3,
    'damage': 1,
    'damage_d6': 1,
}
sm_ballistus_missile_launcher_krak = {
    'attacks': 2,
    'ballistic_skill': 3,
    'hit_reroll': True,         # assumes enemy is not below half strength
    'strength': 9,
    'ap': 3,
    'damage_d6': 1
}
sm_plasma_incinerator_supercharge = {
    'attacks': 2,
    'ballistic_skill': 3,
    'strength': 8,
    'ap': 3,
    'damage': 2,
}
sm_terminator_power_fists = {
    'attacks': 3,
    'ballistic_skill': 3,
    'strength': 8,
    'ap': 2,
    'ignores_cover': True,
    'damage': 2,
}
sm_thunder_hammer = {
    'attacks': 3,
    'ballistic_skill': 4,
    'strength': 8,
    'ap': 2,
    'dev_wounds': True,
    'ignores_cover': True,
    'damage': 2,
}
sm_chaplain_crozius = {
    'attacks': 5,
    'ballistic_skill': 3,
    'strength': 6,
    'ap': 1,
    'ignores_cover': True,
    'damage': 2
}
sm_plasma_pistol = {
    'attacks': 1,
    'ballistic_skill': 3,
    'strength': 7,
    'ap': 2,
    'damage': 1,
}
sm_plasma_pistol_charge = {
    'attacks': 1,
    'ballistic_skill': 3,
    'strength': 8,
    'ap': 3,
    'damage': 2,
}



### Custodes ###

guardian_spear = {
    'attacks': 5,
    'ballistic_skill': 2,
    'strength': 7,
    'wound_reroll_1': False,
    'ap': 2,
    'damage': 2,
}
# # buffed gigachad victus
# blade_champion_victus = {
#     'attacks': 7,
#     'ballistic_skill': 2,
#     'dev_wounds': True,
#     'lethal_hits': True,
#     'sustained_hits': 1,
#     'crit_hit_roll': 5,
#     'strength': 7,
#     'wound_reroll': False,
#     'ap': 3,
#     'damage': 4,
# }
# regular victus
blade_champion_victus = {
    'attacks': 5,
    'ballistic_skill': 2,
    'dev_wounds': True,
    'strength': 7,
    'ap': 3,
    'damage': 3,
}


### Deathguard ###

# All death guard melee is within contagion range, hence all DG melee profiles have toughness_mod = -1

dg_deathshroud_plaguespurt = {
    'attacks_d6': 1,
    'torrent': True,
    'strength': 3,
    'crit_wound_roll': 4,       # this is anti-infantry 4+, assuming attacking infantry
    'ap': 0,
    'ignores_cover': True,
    'damage': 1,
}
dg_deathshroud_manreaper_strike = {
    'attacks': 4,
    'ballistic_skill': 2,
    'lethal_hits': True,
    'strength': 8,
    'toughness_mod': -1,        # all death guard melee is within contagion range, hence I'm including this here
    'ap': 2,
    'ignores_cover': True,
    'damage': 2,
}
dg_typhus_manreaper_strike = {
    'attacks': 5,
    'ballistic_skill': 2,
    'lethal_hits': True,
    'strength': 9,
    'toughness_mod': -1,
    'ap': 2,
    'ignores_cover': True,
    'damage': 3,
}

dg_plague_boltgun = {
    'attacks': 2,
    'ballistic_skill': 3,
    'lethal_hits': True,
    'strength': 4,
    'ap': 0,
    'damage': 1,
}
dg_plague_spewer = {
    'attacks_d6': 1,
    'torrent': True,
    'strength': 5,
    'crit_wound_roll': 2,
    'ap': 1,
    'ignores_cover': True,
    'damage': 1,
}
dg_plague_belcher = {
    'attacks_d6': 1,
    'torrent': True,
    'strength': 4,
    'crit_wound_roll': 4,
    'ap': 0,
    'ignores_cover': True,
    'damage': 1,
}
dg_blight_launcher = {
    'attacks': 2,
    'ballistic_skill': 3,
    'lethal_hits': True,
    'strength': 6,
    'ap': 1,
    'damage': 2,
}
dg_plague_knives = {
    'attacks': 3,
    'ballistic_skill': 3,
    'lethal_hits': True,
    'strength': 4,
    'toughness_mod': -1,        # all death guard melee is within contagion range
    'ap': 0,
    'ignores_cover': True,
    'damage': 1,
}
dg_bubotic_weapons = {
    'attacks': 4,
    'ballistic_skill': 3,
    'lethal_hits': True,
    'strength': 5,
    'toughness_mod': -1,
    'ap': 2,
    'ignores_cover': True,
    'damage': 1,
}
dg_heavy_plague_weapons = {
    'attacks': 3,
    'ballistic_skill': 4,
    'lethal_hits': True,
    'strength': 8,
    'toughness_mod': -1,
    'ap': 2,
    'ignores_cover': True,
    'damage': 2,
}
dg_tallyman_close_combat = {
    'attacks': 4,
    'ballistic_skill': 2,
    'lethal_hits': False,
    'strength': 4,
    'toughness_mod': -1,
    'ap': 0,
    'ignores_cover': True,
    'damage': 1,
}
dg_biologis_putrifier = {
    'attacks': 4,
    'ballistic_skill': 3,
    'lethal_hits': True,        # biologis putrifier gives crits on 5+ to the unit he leads
    'crit_hit_roll': 5,
    'strength': 4,
    'toughness_mod': -1,
    'ap': 0,
    'ignores_cover': True,
    'damage': 1,
}



### Astra Militarum ###

guard_lasgun = {
    'attacks': 1,               # use 'attacks_mod': 1, to account for rapid fire
    'ballistic_skill': 4,
    # 'lethal_hits': False,
    'strength': 3,
    'ap': 0,
    'damage': 1,
}
guard_grenade_krak = {
    'attacks': 1,
    'ballistic_skill': 4,
    'strength': 9,
    'ap': 2,
    'damage_d3': 1,
}
guard_plasma_gun_standard = {
    'attacks': 1,               # use 'attacks_mod': 1, to account for rapid fire
    'ballistic_skill': 4,
    'strength': 7,
    'ap': 2,
    'damage': 1,
}
guard_plasma_gun_supercharge = {
    'attacks': 1,               # use 'attacks_mod': 1, to account for rapid fire
    'ballistic_skill': 4,
    'strength': 8,
    'ap': 3,
    'damage': 2,
}
guard_plasma_pistol_standard = {
    'attacks': 1,
    'ballistic_skill': 4,
    'strength': 7,
    'ap': 2,
    'damage': 1,
}
guard_plasma_pistol_supercharge = {
    'attacks': 1,
    'ballistic_skill': 4,
    'strength': 8,
    'ap': 3,
    'damage': 2,
}
guard_meltagun = {
    'attacks': 1,
    'ballistic_skill': 4,
    'strength': 9,
    'ap': 4,
    'damage_d6': 1,             # use 'damage_mod': 2 to account for extra damage from melta distance
}
guard_lascannon = {
    'attacks': 1,
    'ballistic_skill': 5,
    'strength': 12,
    'ap': 3,
    'damage': 1,
    'damage_d6': 1,
}
guard_autocannon = {
    'attacks': 2,
    'ballistic_skill': 5,
    'strength': 9,
    'ap': 1,
    'damage': 3,
}
guard_heavy_bolter = {
    'attacks': 3,
    'ballistic_skill': 5,
    'sustained_hits': 1,
    'strength': 5,
    'ap': 1,
    'damage': 2,
}



### Eldar ###

eldar_wraithcannon = {
    'attacks': 1,
    'ballistic_skill': 4,
    'strength': 14,
    'ap': 4,
    'damage_d6': 1,
    'dev_wounds': True,
}






##### TARGET PROFILES #####


# TODO:  add points values, allows measurement of points per wound, or attacks needed to kill 100 pts worth of models, etc


target_profile_land_raider = {
    'toughness': 12,
    'armour_save': 2,
    'unit_wounds_profile': [16],
}
target_profile_rhino = {
    'toughness': 9,
    'armour_save': 3,
    'unit_wounds_profile': [10],
}
target_profile_custodes_guard = {
    'toughness': 6,
    'armour_save': 2,
    'invuln_save': 4,
    'feel_no_pain': 7,
    'unit_wounds_profile': [4, 4, 3, 3, 6],     # assumes 2 shields, 2 spears, 1 leader
}
target_profile_termies = {
    'toughness': 5,
    'armour_save': 2,
    'invuln_save': 4,
    'unit_wounds_profile': [3]*5,
}
target_profile_space_marines = {
    'toughness': 4,
    'armour_save': 3,
    'unit_wounds_profile': [2]*10,
}
target_profile_krieg = {            # whole profile assumes optimal defensive options
    'toughness': 3,
    'armour_save': 4,
    'cover': True,
    'feel_no_pain': 6,
    'unit_wounds_profile': [1]*25,     
}
target_profile_necron_warriors = {
    'toughness': 4,
    'armour_save': 4,
    'unit_wounds_profile': [1]*20,
}
target_profile_tau_crisis = {
    'toughness':5,
    'armour_save': 3,
    'unit_wounds_profile': [5, 5, 4]
}
target_profile_wraithguard = {
    'toughness': 7,
    'armour_save': 2,
    'feel_no_pain': 6,
    'unit_wounds_profile': [3]*10
}
target_profile_screamer_killer = {
    'toughness': 9,
    'armour_save': 2,
    'unit_wounds_profile': [10]
}



target_profile_warhound_titan = {
    'toughness': 13,
    'armour_save': 2,
    'unit_wounds_profile': [40]
}