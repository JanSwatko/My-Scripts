import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.data import race_townhalls
from sc2.constants import *
from sc2.ids.upgrade_id import ZERGLINGMOVEMENTSPEED
import enum
import random

class MacroZerg(sc2.BotAI):
    def __init__(self):
        self.ITERATIONS_PER_MINUTE = 165
        self.MAX_WORKERS = 72
        self.MAX_QUEENS = 5
        self.MAX_ZERGLING = 60

    async def on_step(self, iteration):
        self.iteration = iteration
        await self.distribute_workers()
        await self.build_workers()
        await self.build_overlords()
        await self.build_queens()
        await self.build_extractors()
        await self.expand()
        await self.offensive_force_buildings()
        await self.build_offensive_force()
        await self.upgrade()
        await self.attack()

    async def build_workers(self):
        if len(self.units(HATCHERY)) * 22 > len(self.units(DRONE)):
            if len(self.units(DRONE)) < self.MAX_WORKERS:
                larvae = self.units(LARVA)
                if self.can_afford(DRONE) and larvae.exists:
                    await self.do(larvae.random.train(DRONE))

    async def build_queens(self):
        if len(self.units(HATCHERY)) * 2 > len(self.units(QUEEN)):
            if len(self.units(QUEEN)) < self.MAX_QUEENS:
                for hy in self.units(HATCHERY).ready.noqueue:
                    if self.can_afford(QUEEN) and self.supply_left > 0:
                        await self.do(hy.train(QUEEN))

    async def build_overlords(self):
        larvae = self.units(LARVA)
        if self.supply_left < 4 and not self.already_pending(OVERLORD):
            if self.can_afford(OVERLORD) and larvae.exists:
                await self.do(larvae.random.train(OVERLORD))

    async def build_extractors(self):
        if self.units(EXTRACTOR).amount < 3 and self.can_afford(EXTRACTOR):
            drone = self.workers.random
            target = self.state.vespene_geyser.closest_to(drone.position)
            err = await self.do(drone.build(EXTRACTOR, target))

    async def expand(self):
        if self.units(HATCHERY).amount < 4 and self.can_afford(HATCHERY):
            await self.expand_now()

    async def offensive_force_buildings(self):
        hq = self.townhalls.first
        sp = self.units(SPAWNINGPOOL)

        if not (self.units(SPAWNINGPOOL).ready.exists or self.already_pending(SPAWNINGPOOL)):
            if self.can_afford(SPAWNINGPOOL):
                await self.build(SPAWNINGPOOL, near=hq)

        if self.units(SPAWNINGPOOL).ready.exists and not self.units(ROACHWARREN):
            if self.can_afford(ROACHWARREN) and not self.already_pending(ROACHWARREN):
                await self.build(ROACHWARREN, near=hq)

        if self.units(SPAWNINGPOOL).ready.exists and not self.units(BANELINGNEST):
            if self.can_afford(BANELINGNEST) and not self.already_pending(BANELINGNEST):
                await self.build(BANELINGNEST, near=hq)

        if self.units(SPAWNINGPOOL).exists or self.already_pending(SPAWNINGPOOL):
            if not self.units(LAIR).exists and hq.noqueue:
                if self.can_afford(LAIR):
                    await self.do(hq.build(LAIR))

    async def build_offensive_force(self):
        larvae = self.units(LARVA)
        hq = self.townhalls.first

        for queen in self.units(QUEEN).idle:
            abilities = await self.get_available_abilities(queen)
            if AbilityId.EFFECT_INJECTLARVA in abilities:
                await self.do(queen(EFFECT_INJECTLARVA, hq))

        if self.can_afford(ZERGLING) and larvae.exists:
            await self.do(larvae.random.train(ZERGLING))

        if self.can_afford(ROACH) and larvae.exists:
            await self.do(larvae.random.train(ROACH))

        if self.units(BANELINGNEST).ready.exists:
            zerglings = self.units(ZERGLING)
            if zerglings.exists and zerglings.amount >= self.units(BANELING).amount:
                if self.can_afford(BANELING):
                    await self.do(zerglings.random.train(BANELING))
                elif self.can_afford(ZERGLING) and larvae.exists:
                    await self.do(larvae.random.train(ZERGLING))
                    return

    def find_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units)
        elif len(self.known_enemy_structures) > 0:
            return random.choice(self.known_enemy_structures)
        else:
            return self.enemy_start_locations[0]

    async def attack(self):
        if self.units(QUEEN).amount > 1:
            if len(self.known_enemy_units) > 0:
                for q in self.units(QUEEN).idle:
                    await self.do(q.attack(random.choice(self.known_enemy_units)))

        aggressive_units = {ZERGLING: [40, 6], ROACH: [12, 2], BANELING: [20, 3]}

        for UNIT in aggressive_units:
            if self.units(UNIT).amount > aggressive_units[UNIT][0] and self.units(UNIT).amount > aggressive_units[UNIT][1]:
                for s in self.units(UNIT).idle:
                    await self.do(s.attack(self.find_target(self.state)))

            elif self.units(UNIT).amount > aggressive_units[UNIT][1]:
                if len(self.known_enemy_units) > 0:
                    for s in self.units(UNIT).idle:
                        await self.do(s.attack(random.choice(self.known_enemy_units)))

run_game(maps.get("AutomatonLE"), [
    Bot(Race.Zerg, MacroZerg()),
    Computer(Race.Terran, Difficulty.Medium)
], realtime=False)
