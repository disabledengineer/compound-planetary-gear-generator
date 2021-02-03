### Author: Nico Schinacher
### This Script figures out possible compound planetary gear combinations using given boundaries

import math

# desired ratio
desired = 20

# gear ratio tolerance
tolerance = 1

# sun gear first stage (min/max)
sun_gear_min_1 = 15
sun_gear_max_1 = 30
# planet gear first stage (min/max)
planet_gear_min_1 = 15
planet_gear_max_1 = 20
# sun gear second stage (min/max)
sun_gear_min_2 = 15
sun_gear_max_2 = 30
# planet gear second stage (min/max)
planet_gear_min_2 = 15
planet_gear_max_2 = 20

# teeth difference between first and second sun gear
sun_gear_difference = 5

# teeth difference between first and second planet gear
planet_gear_difference = 10

# min planets
min_planets = 4
# max planets
max_planets = 20

# max module difference
module_difference = 1

# ignore irrational module ratios
# recommended: True
ignore_irrational_module_ratios = True

# ignore irrational gear ratios
# i don't care :)
ignore_irrational_gear_ratios = False

# list of possible combinations
combinations = []

# main function for doing stuff
def main():
    # total number of iterations
    total = (sun_gear_max_1 - sun_gear_min_1 + 1) * (planet_gear_max_1 - planet_gear_min_1 + 1) * (sun_gear_max_2 - sun_gear_min_2 + 1) * (planet_gear_max_2 - planet_gear_min_2 + 1)
    # current iteration
    iteration = 0
    # sun gear teeth - first stage
    for sun_gear_1 in range(sun_gear_min_1, sun_gear_max_1 + 1):
        # planet gears teeth - first stage
        for planet_gear_1 in range(planet_gear_min_1, planet_gear_max_1 + 1):
            # sun gear teeth - second stage
            for sun_gear_2 in range(sun_gear_min_2, sun_gear_max_2 + 1):
                # planet gears teeth - second stage
                for planet_gear_2 in range(planet_gear_min_2, planet_gear_max_2 + 1):
                    # update iteration
                    iteration += 1
                    print(iteration/total * 100, end="\r")
                    ring_gear_1 = sun_gear_1 + planet_gear_1 * 2
                    ring_gear_2 = sun_gear_2 + planet_gear_2 * 2
                    try:
                        # do even more math
                        gear_ratio = 1 / (((ring_gear_2 - ((ring_gear_1 / planet_gear_1) * planet_gear_2)) / ring_gear_2) * (sun_gear_1 / (ring_gear_1 + sun_gear_1)))
                        module_ratio = (sun_gear_2 + planet_gear_2) / (sun_gear_1 + planet_gear_1)
                        planet_gear_1_tip_diameter = planet_gear_1 + 2 # calculate using module 1
                        planet_gear_2_tip_diameter = planet_gear_2 + 2 # calculate using module 2
                        # find possible numbers of planets
                        num_planet = []
                        for num in range(min_planets, max_planets + 1):
                            # check whole number
                            if float((sun_gear_1 + ring_gear_1) / num).is_integer() and float((sun_gear_2 + ring_gear_2) / num).is_integer():
                                # check if planets fit inside ring gear (outer circle of sun gear)
                                # basic maffs to figue this out
                                # pi/sin^-1(r/(r+R))
                                # might use ' >= ' however there still should be clearence between the planet gears, thus ' > '
                                if math.pi / math.asin((planet_gear_1_tip_diameter / 2) / (planet_gear_1_tip_diameter / 2 + sun_gear_1 / 2)) > num and math.pi / math.asin((planet_gear_2_tip_diameter / 2) / (planet_gear_2_tip_diameter / 2 + sun_gear_1 / 2)) > num:
                                    num_planet.append(num)
                        # check if there even is a possible number of planets
                        if len(num_planet) == 0:
                            continue
                        # check if within tolerance
                        # don't have much abs in real life, so might aswell show off here
                        if(abs(abs(gear_ratio) - abs(desired)) > tolerance):
                            continue
                        # check desired tooth difference
                        if abs(sun_gear_2 - sun_gear_1) <= sun_gear_difference and abs(planet_gear_1 - planet_gear_2) > planet_gear_difference:
                            continue
                        # check module difference
                        if module_ratio < 1:
                            module_ratio = 1 / module_ratio
                        if module_ratio > module_difference:
                            continue
                        # also check if module ratio is irrational
                        if (ignore_irrational_module_ratios and len(str(module_ratio).split(".")[1]) > 6):
                            continue
                        if (ignore_irrational_gear_ratios and len(str(gear_ratio).split(".")[1]) > 6):
                            continue
                        gear = Gear(sun_gear_1, planet_gear_1, ring_gear_1, sun_gear_2, planet_gear_2, ring_gear_2, module_ratio, gear_ratio, num_planet)
                        combinations.append(gear)
                    except ZeroDivisionError:
                        # good code doesn't need exception handling
                        # wait...
                        continue
    for combination in combinations:
        print("SG1: " + str(combination.sun_gear_1) + ", PG1: " + str(combination.planet_gear_1) + ", RG1: " + str(combination.ring_gear_1))
        print("SG2: " + str(combination.sun_gear_2) + ", PG2: " + str(combination.planet_gear_2) + ", RG2: " + str(combination.ring_gear_2))
        print("Module Ratio: " + str(combination.module_ratio))
        print("Ratio: " + str(combination.gear_ratio))
        print("Number of Planets: " + str(combination.num_planet))
        print()
# class representing single compound planetary gear
class Gear:
    def __init__(self, sg1, pg1, rg1, sg2, pg2, rg2, m, r, n):
        self.sun_gear_1 = sg1
        self.planet_gear_1 = pg1
        self.ring_gear_1 = rg1
        self.sun_gear_2 = sg2
        self.planet_gear_2 = pg2
        self.ring_gear_2 = rg2
        self.module_ratio = m
        self.gear_ratio = r
        self.num_planet = n
main()