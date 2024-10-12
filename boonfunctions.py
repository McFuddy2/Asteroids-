


def double_score_multiplier(player, game):
    game.score_multiplier += 1
    message = "Score Multiply Bonus"
    return message, undo_double_score_multiplier
def undo_double_score_multiplier(player, game):
    game.score_multiplier -= 1   


def speed_boost(player, game):
    game.player_movement_speed += 1.5
    message = "Speed Increase"
    return message, undo_speed_boost
def undo_speed_boost(player, game):
    game.player_movement_speed -= 100
    

def shoot_faster(player, game):
    game.player_shoot_cooldown /= 2
    message = "Fast Shot"
    return message, undo_shoot_faster
def undo_shoot_faster(player, game):
        game.player_shoot_cooldown *= 2
    

def extra_life(player, game):
    player.lives += 1
    message = "Extra Life"
    return message, undo_extra_life
def undo_extra_life(player, game):
    game.player_radius += 0
    

def bigger_bullets(player, game):
    game.shot_radius += 10
    message = "BIG SHOT"
    return message, undo_bigger_bullets
def undo_bigger_bullets(player, game):
    game.shot_radius -= 10
    

def increased_pos_item_drop(player, game):
    game.pos_item_drop_chance += 0.2
    message = "Increased Green Drops"
    return message, undo_increased_pos_item_drop
def undo_increased_pos_item_drop(player, game):
    game.pos_item_drop_chance -= 0.1
    