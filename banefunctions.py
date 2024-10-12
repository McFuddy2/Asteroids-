def more_asteroids(player, game):
    game.asteroid_spawn_rate /= 2  # Increase spawn rate
    message = "More Asteroids"
    return message, undo_more_asteroids
def undo_more_asteroids(player, game):
    game.asteroid_spawn_rate *= 2


def reduce_speed(player, game):
    game.player_movement_speed -= 100  # Decrease speed by 25%
    message = "Speed Decrease"
    return message, undo_reduce_speed
def undo_reduce_speed(player, game):
    game.player_movement_speed += 100


def shoot_slower(player, game):
    game.player_shoot_cooldown *= 2  # Double the cooldown time
    message = "Slow Shot"
    return message, undo_shoot_slower
def undo_shoot_slower(player, game):
    game.player_shoot_cooldown /= 2


def slow_turning(player, game):
    game.player_turn_speed -= 100  # Slow down turning
    message = "Slow Turning"
    return message, undo_slow_turning
def undo_slow_turning(player, game):
    game.player_turn_speed += 100


def increased_neg_item_drop(player, game):
    game.neg_item_drop_chance += 0.2  # Increase the chance by 5%
    message = "Increased Red Drops"
    return message, undo_increased_neg_item_drop
def undo_increased_neg_item_drop(player, game):
    game.neg_item_drop_chance -= 0.2