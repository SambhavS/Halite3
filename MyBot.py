# Imports
import hlt
from hlt import constants
from hlt import positionals as ps
import random
import logging

# Helpers

def log(string):
    logging.info(string)
    
# Main    
def main():
    # Ship Movements
    def max_halite(positions):
        return max(positions, key = lambda pos: game_map[pos].halite_amount)

    def min_halite(positions):
        return min(positions, key = lambda pos: game_map[pos].halite_amount)
    
    def expected_val(pos):
        on_sq = game_map[pos].halite_amount
        halite, moves = 0, game_map.calculate_distance(ship.position, pos) ** 1.5
        if on_sq <= 50:
            return 0
        while on_sq > 50:
            moves += 1
            halite += on_sq/4
            on_sq *= 0.75
        return halite/float(moves)
        
    def to_target(ship):
        val = 33
        positions = [norm(ps.Position(ship.position.x+i, ship.position.y+j))
                     for i in range(-val, val) for j in range(-val, val)] 
        positions = sorted(positions, key=lambda pos: -1 * expected_val(pos))
        for pos in positions:
            if pos != ship.position:
                move = goto(ship, pos)
                if move != ship.stay_still():
                    return move
        return safe_rand(ship)

    def goto(ship, pos):
        dx, dy = pos.x - ship.position.x, pos.y - ship.position.y
        if not dy:
            posX = ps.Position(ship.position.x + int(dx/abs(dx)), ship.position.y)
            return ship.move(naive_navigate(ship, norm(posX)))
        if not dx:
            posY = ps.Position(ship.position.x, ship.position.y + int(dy/abs(dy)))
            return ship.move(naive_navigate(ship, norm(posY)))
        posX = norm(ps.Position(ship.position.x + int(dx/abs(dx)), ship.position.y))
        posY = norm(ps.Position(ship.position.x, ship.position.y + int(dy/abs(dy))))
        better, worse = max_halite([posX, posY]), min_halite([posX, posY])
        if game_map[better].is_empty:
            return ship.move(naive_navigate(ship, better))
        return ship.move(naive_navigate(ship, worse))


    def to_yard(ship):
        move = goto(ship, me.shipyard.position)
        if move != ship.stay_still():
            return move
        return safe_rand(ship)

    def away_yard(ship):
        dx, dy = ship.position.x - me.shipyard.position.x, ship.position.y - me.shipyard.position.y
        goal = norm(ps.Position(ship.position.x + dx, ship.position.y + dy))
        move = goto(ship, goal)
        if move != ship.stay_still():
            return move
        return safe_rand(ship)


    def safe_rand(ship):
        positions = ship.position.get_surrounding_cardinals()
        random.shuffle(positions)
        for pos in positions:
            if game_map[pos].is_empty:
                return ship.move(naive_navigate(ship,pos))
        return ship.stay_still()

    def move_choice(ship, stat):
        if game_map[ship.position].halite_amount > 50 and ship.halite_amount < 985:
            return ship.stay_still()
                
        if stat == "explore":
            if ship.halite_amount > 985:
                ship_status[ship.id] = "return"
                return to_yard(ship)
            return to_target(ship)

        if stat == "return":
            return to_yard(ship)

        if stat == "leave":
            if game_map.calculate_distance(ship.position, me.shipyard.position) > 5:
                ship_status[ship.id] = "explore"
                return to_target(ship)
            return away_yard(ship)

    def end_move_choice(ship, stat):
        if ship.position == me.shipyard.position:
            return ship.stay_still()
        if game_map.calculate_distance(ship.position, me.shipyard.position) == 1:
            return ship.move(game_map.get_unsafe_moves(ship.position, me.shipyard.position)[0])
        return to_yard(ship)


    # Main Loop
    while True:
        game.update_frame()
        me = game.me
        game_map = game.game_map
        naive_navigate = game_map.naive_navigate
        norm = game_map.normalize
        commands = []

        # Ship Movement
        for ship in me.get_ships():
            # Initialize ship
            if ship.id not in ship_status:
                ship_status[ship.id] = "explore"
            # Move Choice
            if ship.halite_amount*10 < game_map[ship.position].halite_amount:
                command = ship.stay_still()
            elif turns - game.turn_number < 30:
                command = end_move_choice(ship, ship_status[ship.id])
            elif ship.position == me.shipyard.position:
                ship_status[ship.id] = "leave"
                command = safe_rand(ship)
            else:
                command = move_choice(ship, ship_status[ship.id])
            commands.append(command)
        
        # Spawning
        if me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
            start = game.turn_number <= 1
            make_more =  len(me.get_ships()) < 20 and turns - game.turn_number > 100
            if start or make_more:
                commands.append(me.shipyard.spawn())  

        game.end_turn(commands)


#Initialize
game = hlt.Game()
game.ready("BattleBot")
ship_status = {}
turns = {32: 400, 40: 425, 48: 450, 56: 475, 64: 500}[game.game_map.width]
DIRS = ps.Direction.get_all_cardinals()
main()
