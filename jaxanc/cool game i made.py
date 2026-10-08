import math
import random
import pygame

# Window settings
WIDTH = 1024
HEIGHT = 768
TITLE = "Infinite Archery 2D"

# Game states
game_over = False
score = 0

# Player (Bow) position
player_x = 100
player_y = HEIGHT // 2

# Bow charging mechanics
charging = False
charge_power = 0.0
MAX_CHARGE = 30.0

# Store current mouse position for aiming
current_mouse_pos = (WIDTH // 2, HEIGHT // 2)

# Projectiles (Arrows currently in flight)
arrows = []

# Targets list
targets = []
target_spawn_timer = 0


class Target:

  def __init__(self):
    self.x = WIDTH - 80
    self.y = random.randint(100, HEIGHT - 100)
    self.radius = 36  # Made slightly bigger so they are easier to hit!
    self.speed = random.randint(2, 4)
    self.direction = random.choice([-1, 1])

  def update(self):
    self.y += self.speed * self.direction
    if self.y < 80 or self.y > HEIGHT - 80:
      self.direction *= -1


def reset_game():
  global score, arrows, targets, game_over, charging, charge_power
  score = 0
  arrows = []
  targets = [Target(), Target()]
  game_over = False
  charging = False
  charge_power = 0.0
  # Hide system mouse cursor for custom crosshair
  pygame.mouse.set_visible(False)
  # Confine mouse inside the window
  pygame.event.set_grab(True)


reset_game()


def update():
  global charge_power, target_spawn_timer

  if game_over:
    return

  # Handle charging the bow (Holding Left Mouse Button)
  if charging:
    if charge_power < MAX_CHARGE:
      charge_power += 0.5

  # Update targets
  for t in targets:
    t.update()

  # Infinitely spawn new targets slower
  target_spawn_timer += 1
  if target_spawn_timer > 220:
    targets.append(Target())
    target_spawn_timer = 0

  # Update flying arrows
  for arrow in arrows[:]:
    arrow["x"] += arrow["vx"]
    arrow["y"] += arrow["vy"]

    if (
        arrow["x"] > WIDTH
        or arrow["x"] < 0
        or arrow["y"] > HEIGHT
        or arrow["y"] < 0
    ):
      arrows.remove(arrow)
      continue

    # Check collisions with targets
    hit_target = None
    for t in targets:
      distance = math.hypot(arrow["x"] - t.x, arrow["y"] - t.y)
      if distance < t.radius:
        hit_target = t
        break

    if hit_target:
      targets.remove(hit_target)
      arrows.remove(arrow)
      global score
      score += 1


def on_key_down(key):
  # Press ESC to unlock the mouse and show the cursor so you can move the window
  if key == keys.ESCAPE:
    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)


def on_mouse_move(pos):
  global current_mouse_pos
  current_mouse_pos = pos


def on_mouse_down(pos, button):
  global charging, charge_power
  if button == mouse.LEFT:
    charging = True
    charge_power = 0.0


def on_mouse_up(pos, button):
  global charging, arrows, charge_power

  if button == mouse.LEFT and charging:
    charging = False

    # Calculate angle from bow to mouse release position
    angle = math.atan2(pos[1] - player_y, pos[0] - player_x)

    base_speed = 10.0
    speed = base_speed + charge_power

    vx = math.cos(angle) * speed
    vy = math.sin(angle) * speed

    arrows.append({"x": player_x, "y": player_y, "vx": vx, "vy": vy})
    charge_power = 0.0


def draw():
  screen.fill((30, 30, 40))

  # Draw boundary line
  screen.draw.line((WIDTH - 100, 0), (WIDTH - 100, HEIGHT), (70, 70, 90))

  # Calculate aiming angle based on current mouse position
  mx, my = current_mouse_pos
  aim_angle = math.atan2(my - player_y, mx - player_x)

  # --- DRAW ROTATED / AIMED BOW ---
  bow_radius = 35
  pull_back_offset = int(charge_power * 1.5)

  tip_angle_offset = math.pi / 2
  tip1_x = player_x + math.cos(aim_angle - tip_angle_offset) * bow_radius
  tip1_y = player_y + math.sin(aim_angle - tip_angle_offset) * bow_radius
  tip2_x = player_x + math.cos(aim_angle + tip_angle_offset) * bow_radius
  tip2_y = player_y + math.sin(aim_angle + tip_angle_offset) * bow_radius

  # Draw bow handle/body line
  screen.draw.line((tip1_x, tip1_y), (tip2_x, tip2_y), (139, 69, 19))

  # Bowstring notch
  notch_x = player_x - math.cos(aim_angle) * (15 + pull_back_offset)
  notch_y = player_y - math.sin(aim_angle) * (15 + pull_back_offset)

  # Draw bowstring segments connecting tips to the notch
  screen.draw.line((tip1_x, tip1_y), (notch_x, notch_y), (200, 200, 200))
  screen.draw.line((tip2_x, tip2_y), (notch_x, notch_y), (200, 200, 200))

  # If charging, draw the yellow arrow rod nocked on the string
  if charging:
    arrow_tip_x = player_x + math.cos(aim_angle) * (20 + charge_power)
    arrow_tip_y = player_y + math.sin(aim_angle) * (20 + charge_power)
    screen.draw.line(
        (notch_x, notch_y), (arrow_tip_x, arrow_tip_y), (255, 255, 0)
    )

    # Charging indicator bar above bow
    bar_width = int((charge_power / MAX_CHARGE) * 60)
    screen.draw.filled_rect(
        Rect(player_x - 30, player_y - 70, 60, 8), (50, 50, 50)
    )
    screen.draw.filled_rect(
        Rect(player_x - 30, player_y - 70, bar_width, 8), (255, 165, 0)
    )

  # Draw Targets
  for t in targets:
    screen.draw.filled_circle((t.x, t.y), t.radius, (220, 50, 50))
    screen.draw.filled_circle((t.x, t.y), int(t.radius * 0.6), (240, 240, 240))
    screen.draw.filled_circle((t.x, t.y), int(t.radius * 0.2), (200, 30, 30))

  # Draw Flying Arrows as rods pointing in the direction of flight
  for arrow in arrows:
    ax, ay = arrow["x"], arrow["y"]
    flight_angle = math.atan2(arrow["vy"], arrow["vx"])
    tail_x = ax - math.cos(flight_angle) * 16
    tail_y = ay - math.sin(flight_angle) * 16
    front_x = ax + math.cos(flight_angle) * 6
    front_y = ay + math.sin(flight_angle) * 6
    screen.draw.line(
        (int(tail_x), int(tail_y)), (int(front_x), int(front_y)), (255, 255, 0)
    )

  # Draw Custom In-Game Crosshair
  screen.draw.line((mx - 8, my), (mx + 8, my), (0, 255, 255))
  screen.draw.line((mx, my - 8), (mx, my + 8), (0, 255, 255))
  screen.draw.circle((mx, my), 6, (0, 255, 255))

  # Draw UI
  screen.draw.text(f"Score: {score}", (20, 20), color="white", fontsize=32)
  screen.draw.text(
      "ESC: Release Mouse | Hold LEFT CLICK to charge & shoot",
      (20, HEIGHT - 30),
      color="lightgray",
      fontsize=20,
  )