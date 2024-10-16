from random import randint
from math import ceil
import numpy as np
import matplotlib.pyplot as plt 
from copy import deepcopy

from wh_profiles import *



# ~~~ ignoring these for now ~~~
# TODO: add options for spillover to characters in attached units?  best way is to just "slow roll" everything, forget
# numpy just use a for loop for number of attacks.
# TODO: sequence of attacks from multiple units?  where the conditions of the attack might change, e.g. the first unit
# gets the target below half strength, then the 2nd unit has a rule that benefits from that.  similarly for chewing 
# through a bodyguard unit, then the character gets a different profile.  or precision potentially killing the character 
# first, which changes the defensive characteristics of the bodyguard unit.
# TODO: for CP reroll, determine where best to reroll by getting statistics from different dice rolls and maximising
# either probability of destroying unit or avg damage (you choose).  E.g. is it better to reroll number of attacks when 
# you rolled a 3, or is it better to save until a damage roll?
# ~~~ ignoring these for now ~~~



def make_attacks(
    # required parameters
    strength,
    toughness,
    armour_save,
    unit_wounds_profile,

    # attacker parameters
    num_weapons = 1,
    attacks = 0,
    attacks_d3 = 0,
    attacks_d6 = 0,
    reroll_attacks = False,
    blast = False,

    ballistic_skill = 7,
    torrent = False,
    crit_hit_roll = 6,
    reroll_hits_of_1 = False,
    reroll_hits = False,
    reroll_hits_no_crit = False,
    reroll_1_hit = False,
    lethal_hits = False,
    sustained_hits = 0,

    crit_wound_roll = 6,
    reroll_wounds_of_1 = False,
    reroll_wounds = False,
    reroll_wounds_no_crit = False,
    reroll_1_wound = False,
    dev_wounds = False,

    ap = 0,
    ignores_cover = False,

    damage = 0,
    damage_d3 = 0,
    damage_d6 = 0,
    damage_reroll = False,
    cp_reroll = False,          # TODO:  a reroll used only once throughout this attack, prioritises damage > wound > hit

    # target parameters
    invuln_save = None,
    cover = False,
    halve_damage = False,
    feel_no_pain = None,

    # mods
    attacks_mod= 0,
    hit_mod = 0,
    strength_mod = 0,
    toughness_mod = 0,
    wound_mod = 0,
    ap_mod = 0,
    armour_mod = 0,
    damage_mod = 0,

    # statistics
    statistics_dict = {
        'total_damage': 0,
        'damage_spillover': 0
    }
):
    """
    Makes attacks against a unit with 1 weapon profile.  Resolve multiple attacks by stringing this function together and
    updating the target profile.  Modify the calculation by adding an 'extra_effects' dictionary.
    E.g.
    target_profile['unit_wounds_profile'] = make_attacks(num_weapons=4, **attack_profile_1, **target_profile)
    target_profile['unit_wounds_profile'] = make_attacks(**{**attack_profile_2, **extra_effects}, **target_profile)

    Returns: 
        List:   each entry is the remaining wounds of each model in the target unit
    """

    # so that invuln_save and feel_no_pain can be set to None without breaking anything
    if not invuln_save:
        invuln_save = 7
    if not feel_no_pain:
        feel_no_pain = 7

    # get which model in the unit to target
    for model_id in range(len(unit_wounds_profile)):
        if unit_wounds_profile[model_id] > 0:
            current_wounds = unit_wounds_profile[model_id]
            break
    models_in_unit = len(unit_wounds_profile) - model_id
    if model_id >= len(unit_wounds_profile):
        raise ValueError("Unit is already dead lmao")

    # TODO: initialise some attack statistics
    statistics_dict['damage_spillover'] = statistics_dict.get('damage_spillover', 0)
    # overkill = target_profile.get('overkill', 0)



    ### hit rolls ###
    
    # get number of attacks
    num_attacks = (attacks+attacks_mod) * num_weapons
    rolls = np.random.randint(1, 7, attacks_d6*num_weapons)
    if reroll_attacks:
        # currently assumes rerolling attacks if less than average (3.5)
        for i, roll in enumerate(rolls):
            if roll < 3.5:
                rolls[i] = randint(1,6)
    num_attacks += rolls.sum()
    rolls = np.random.randint(1,4, attacks_d3*num_weapons)
    if reroll_attacks:
        for i, roll in enumerate(rolls):
            if roll < 2:
                rolls[i] = randint(1,3)
    num_attacks += rolls.sum()
    if blast:
        num_attacks += models_in_unit//5*num_weapons


    # get hits and crit hits
    if num_attacks <= 0:
        pass
    elif torrent:
        hits = num_attacks
        crit_hits = 0
    else:
        # roll needed to hit
        hit_roll = ballistic_skill-hit_mod
        if hit_roll < 2:
            hit_roll = 2
        
        # make hit rolls
        rolls = np.random.randint(1, 7, num_attacks)
        if reroll_hits_no_crit:
            rolls[rolls<crit_hit_roll] = np.random.randint(1, 7, (rolls<crit_hit_roll).sum())
        elif reroll_hits:
            rolls[rolls<hit_roll] = np.random.randint(1, 7, (rolls<hit_roll).sum())
        elif reroll_hits_of_1:
            rolls[rolls==1] = np.random.randint(1, 7, (rolls==1).sum())
        elif reroll_1_hit:
            if rolls[rolls.argmin()] < hit_roll:
                rolls[rolls.argmin()] = np.random.randint(1, 7)

        hits = np.logical_and(rolls>=hit_roll, rolls<crit_hit_roll).sum()
        crit_hits = (rolls>=crit_hit_roll).sum()



    ### wound rolls ###

    # roll needed to wound
    str_tough_ratio = (strength+strength_mod)/(toughness+toughness_mod)
    if str_tough_ratio <= 0.5:
        wound_roll = 6
    elif str_tough_ratio > 0.5 and str_tough_ratio < 1:
        wound_roll = 5
    elif str_tough_ratio == 1:
        wound_roll = 4
    elif str_tough_ratio > 1 and str_tough_ratio < 2:
        wound_roll = 3
    elif str_tough_ratio >= 2:
        wound_roll = 2

    wound_roll -= wound_mod
    if wound_roll < 2:
        wound_roll = 2
    
    # number of rolls to make
    rolls_to_make = hits
    rolls_to_make += sustained_hits*crit_hits
    if not lethal_hits:
        rolls_to_make += crit_hits

    # do wound rolls
    if rolls_to_make > 0:
        rolls = np.random.randint(1, 7, rolls_to_make)
        if reroll_wounds_no_crit:
            rolls[rolls<crit_wound_roll] = np.random.randint(1, 7, (rolls<crit_wound_roll).sum())
        elif reroll_wounds:
            rolls[rolls<wound_roll] = np.random.randint(1, 7, (rolls<wound_roll).sum())
        elif reroll_wounds_of_1:
            rolls[rolls==1] = np.random.randint(1, 7, (rolls==1).sum())
        elif reroll_1_wound:
            if rolls[rolls.argmin()] < wound_roll:
                rolls[rolls.argmin()] = np.random.randint(1, 7)
    
    # calculate number of wounds and crit wounds
    wounds = np.logical_and(rolls>=wound_roll, rolls<crit_wound_roll).sum()
    if lethal_hits:
        wounds += crit_hits
    crit_wounds = (rolls>=crit_wound_roll).sum()



    ### armour + invuln saves ###

    # armour save modifications
    armour_save += armour_mod
    if armour_save < 2:
        armour_save = 2
    ap += ap_mod
    if ap < 0:
        ap = 0

    if cover and not ignores_cover:
        if armour_save > 3:
            armour_save -= 1
        elif ap > 0:
            ap -= 1
    
    # roll needed to save
    save_roll = invuln_save if invuln_save < armour_save + ap else armour_save + ap
    
    # make save rolls
    rolls_to_make = wounds
    if not dev_wounds:
        rolls_to_make += crit_wounds
    rolls = np.random.randint(1, 7, rolls_to_make)

    damage_instances = (rolls<save_roll).sum()
    if dev_wounds:
        damage_instances += crit_wounds



    ### damage ###

    # apply damage instances one by one to account for spillover
    for dmg_instance in range(damage_instances):
        # get wounds of targeted model
        current_wounds = unit_wounds_profile[model_id]

        # calculate damage
        dmg = damage
        dmg_d6 = damage_d6*randint(1,6)
        if damage_reroll:
            # current heuristic:  if no fnp, don't reroll if already killing.  With fnp, just reroll if below avg. 
            if dmg_d6 < 3.5:
                if feel_no_pain < 7:
                    dmg_d6 = randint(1,6)
                elif dmg + dmg_d6 < current_wounds:
                    dmg_d6 = randint(1,6)
        dmg += dmg_d6
        dmg_d3 = damage_d3*randint(1,3)
        if damage_reroll and dmg_d3 < 2:
            dmg_d3 = damage_d3*randint(1,3)
        
        if halve_damage:
            dmg = ceil(dmg/2)
        dmg += damage_mod

        # apply feel no pain
        if feel_no_pain < 7:
            rolls = np.random.randint(1, 7, dmg)
            dmg -= (rolls>=feel_no_pain).sum()

        # apply damage to model
        if dmg >= current_wounds:
            # if damage exceeds wounds, kill model and further damage is lost
            statistics_dict['total_damage'] += current_wounds
            unit_wounds_profile[model_id] = 0
            model_id += 1

            # this is literally just to record how much damage was lost due to model overkill
            # which isn't even an important stat, I was just curious lmao
            dmg -= current_wounds
            if model_id >= len(unit_wounds_profile):
                # unit has been wiped
                current_wounds = 0
                break
            statistics_dict['damage_spillover'] += dmg

        else:
            # if damage does not exceed wounds, subtract damage from wounds
            unit_wounds_profile[model_id] -= dmg
            statistics_dict['total_damage'] += dmg
    

    return unit_wounds_profile







LIST_OF_EXTRA_EFFECTS = {
    'attacks_mod': 0,
    'hit_mod': 0,
    'strength_mod': 0,
    'toughness_mod': 0,
    'wound_mod': 0,
    'ap_mod': 0,            # NOTE: +1 ap_mod improves ap, -1 ap_mod worsens ap
    'armour_mod': 0,        # NOTE: +1 armour_mod worsens armour, -1 armour_mod improves armour
    'damage_mod': 0,
    'halve_damage': False,  # halve damage applies before damage_mod

    # apart from the above mods, you can override literally any other characteristic here like so
    'lethal_hits': True,
    'sustained_hits': 2,
    'crit_wound_roll': 4,
    'toughness': 6,
}


# NOTE: use **dict to unpack a dictionary like so:
stinky = {
    'toughness_mod': -1,
    'armour_mod': +1
}
extra_effects = {
    'crit_hit_roll': 5,
    'lethal_hits': True,
    **stinky,
}







# ----- NOTE: CHANGE THIS TO SELECT TARGET ----- #
target = target_profile_land_raider
# ---------------------------------------------- #
target_profile = deepcopy(target)



# ----- NOTE: MODIFY THIS TO ADD EFFECTS TO YOUR ATTACK/TARGET ----- #
extra_effects = {
    'hit_mod': +1,              # from wraithseer
    'lethal_hits': True,        # from wraithseer
    'reroll_1_hit': True,       # eldar detachment rule
    'reroll_1_wound': True,     # eldar detachment rule
}
# ------------------------------------------------------------------ #



# repeat scenario some large amount of times, get distribution of outcomes
# NOTE: lower this number if it gets too slow when doing something with many different attacks
n_trials = 10000

damage_done = np.zeros(n_trials)
models_killed = np.zeros(n_trials)
max_wounds = 0
for i in range(len(target_profile['unit_wounds_profile'])):
    max_wounds += target_profile['unit_wounds_profile'][i]

# make attacks n_trials times
for i in range(n_trials):
    target_profile = deepcopy(target)
    statistics = {'total_damage': 0}

    # ----- NOTE: ADD YOUR ATTACKS HERE ----- #
    target_profile['unit_wounds_profile'] = make_attacks(
        num_weapons=10, **{**eldar_wraithcannon, **target_profile, **extra_effects}, statistics_dict=statistics
    )
    # --------------------------------------- #

    # store results
    damage_done[i] = statistics['total_damage']
    models_killed[i] = target_profile['unit_wounds_profile'].count(0)





# plot histograms, print probability of killing unit
n_kills = (models_killed==len(target_profile['unit_wounds_profile'])).sum()
print(f'Probability of killing unit:  {n_kills/n_trials}')

counts, edges, bars = plt.hist(damage_done, bins=np.arange(max_wounds+2)-0.5, density=True, cumulative=False)
plt.bar_label(bars, rotation='vertical')
plt.xticks(np.arange(0, max_wounds+1))
plt.xlabel('Total Damage')
plt.ylabel('Probability')
plt.show()

counts, edges, bars = plt.hist(models_killed, bins=np.arange(len(target_profile['unit_wounds_profile'])+2)-0.5, density=True, cumulative=False)
plt.bar_label(bars, rotation='vertical')
plt.xticks(np.arange(0, len(target_profile['unit_wounds_profile']) + 1 ))
plt.xlabel('Models Slain')
plt.ylabel('Probability')
plt.show()


