import os
import pygame
import random
import csv


class GUI:

    def __init__(self) -> None:
        """
        Sets up the window and creates everything such as the bird, the pipes, and the background.
        """
        self.width, self.height = 550, 500
        self.window = pygame.display.set_mode((self.width, self.height))

        self.fps = 40

        self.running = True
        self.active = False
        self.vel_bird = 0
        self.vel_pipe = 4
        self.vel_min = -8
        self.vel_max = 10

        self.bird_width = 55
        self.bird_height = 35
        self.bird_image = pygame.image.load(os.path.join("images", "bird.png"))
        self.bird_right = pygame.transform.scale(self.bird_image, (self.bird_width, self.bird_height))
        self.bird_hit_right = pygame.Rect(60, self.height / 2, self.bird_width, self.bird_height)
        self.bird_image_left = pygame.image.load(os.path.join("images", "bird_left.png"))
        self.bird_left = pygame.transform.scale(self.bird_image_left, (self.bird_width, self.bird_height))
        self.bird_hit_left = pygame.Rect(self.width - 150, self.height / 2, self.bird_width, self.bird_height)

        self.back_image = pygame.image.load(os.path.join("images", "background.jpg"))
        self.back = pygame.transform.scale(self.back_image, (self.width, self.height))

        self.title_image = pygame.image.load(os.path.join("images", "title.png"))
        self.title = pygame.transform.scale(self.title_image, (self.width, self.height))
        self.distance_y = 150
        self.distance_x = 225
        self.pipe_width = 50

        self.pipe_image = pygame.image.load(os.path.join("images", "pipe.png"))
        self.pipe_up = pygame.transform.rotate(
            pygame.transform.scale(self.pipe_image, (self.pipe_width, self.height - 150)), 0)
        self.pipe_down = pygame.transform.rotate(
            pygame.transform.scale(self.pipe_image, (self.pipe_width, self.height - 150)), 180)

        up_y, down_y = self.random_y()
        pipe_up_hit1 = pygame.Rect(self.width + self.distance_x * 0, up_y, self.pipe_width, self.height - 170)
        pipe_down_hit1 = pygame.Rect(self.width + self.distance_x * 0, down_y, self.pipe_width, self.height - 170)
        up_y, down_y = self.random_y()
        pipe_up_hit2 = pygame.Rect(self.width + self.distance_x * 1, up_y, self.pipe_width, self.height - 170)
        pipe_down_hit2 = pygame.Rect(self.width + self.distance_x * 1, down_y, self.pipe_width, self.height - 170)
        up_y, down_y = self.random_y()
        pipe_up_hit3 = pygame.Rect(self.width + self.distance_x * 2, up_y, self.pipe_width, self.height - 170)
        pipe_down_hit3 = pygame.Rect(self.width + self.distance_x * 2, down_y, self.pipe_width, self.height - 170)

        self.pipe_up_list = [pipe_up_hit1, pipe_up_hit2, pipe_up_hit3]
        self.pipe_down_list = [pipe_down_hit1, pipe_down_hit2, pipe_down_hit3]

        self.clock = pygame.time.Clock()

        card_height = 15
        card_width = 15
        card_0 = pygame.transform.scale(pygame.image.load(os.path.join("images", "0.png")), (card_height, card_width))
        card_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "1.png")), (card_height, card_width))
        card_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "2.png")), (card_height, card_width))
        card_3 = pygame.transform.scale(pygame.image.load(os.path.join("images", "3.png")), (card_height, card_width))
        card_4 = pygame.transform.scale(pygame.image.load(os.path.join("images", "4.png")), (card_height, card_width))
        card_5 = pygame.transform.scale(pygame.image.load(os.path.join("images", "5.png")), (card_height, card_width))
        card_6 = pygame.transform.scale(pygame.image.load(os.path.join("images", "6.png")), (card_height, card_width))
        card_7 = pygame.transform.scale(pygame.image.load(os.path.join("images", "7.png")), (card_height, card_width))
        card_8 = pygame.transform.scale(pygame.image.load(os.path.join("images", "8.png")), (card_height, card_width))
        card_9 = pygame.transform.scale(pygame.image.load(os.path.join("images", "9.png")), (card_height, card_width))

        self.score_x = 15
        self.score_y = 15
        self.count = 0

        self.scorecards = [card_0, card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9]
        self.current_score = []

        self.running_bird = False
        self.running_combat = False
        self.active_combat = False

        self.bullet_width = 6
        self.bullet_height = 18
        self.bullet_right = pygame.transform.rotate(
            pygame.transform.scale(self.pipe_image, (self.bullet_width, self.bullet_height)), 90)
        self.bullet_left = pygame.transform.rotate(
            pygame.transform.scale(self.pipe_image, (self.bullet_width, self.bullet_height)), 270)
        self.bullet_left_list = []
        self.bullet_right_list = []

        self.middle = pygame.Rect(self.width / 2 - 2, 0, 4, self.height)

        self.count_left = 0
        self.count_right = 0
        self.current_score_left = []
        self.current_score_right = []

        self.running_leader = False
        self.leaderboard = []
        self.read_highscores()

        pygame.init()

        self.base_font = pygame.font.Font(os.path.join("text", "flappy_text.ttf"), 50)

        self.main()

    def delete_highscores(self,randomize=False) -> None:
        """
        Deletes 'data.csv' and clears leaderboard list

        :param randomize: is passed through for create_highscores()
        """
        os.remove("data.csv")
        self.leaderboard.clear()
        self.read_highscores(randomize)

    def create_highscores(self,randomize=False) -> None:
        """
        Creates new 'data.csv'

        :param randomize: adds random scores to leaderboard if True
        """
        list_scores = []
        if randomize:
            rand = random
            for num in range(0, 6):
                list_scores.append(rand.randint(0, 10))
            list_scores.sort(reverse=True)
        with open("data.csv","w") as new_file:
            con = csv.writer(new_file,delimiter=",")
            for num in range(0,6):
                if randomize:
                    con.writerow(["CPU",list_scores[num]])
                else:
                    con.writerow(["CPU","0"])
            
    def read_highscores(self,randomize=False) -> None:
        """
        Reads 'data.csv' for highscores

        :param randomize: is passed through for create_highscores()
        """
        if not os.path.isfile("data.csv"):
            self.create_highscores(randomize)
        with open("data.csv","r") as input_file:
            con = csv.reader(input_file,delimiter=",")
            for row in con:
                self.leaderboard.append(row)

    def check_highscores(self) -> None:
        """
        Checks if count is higher than the lowest score on leaderboard
        """
        for x, num in enumerate(self.leaderboard):
            if self.count > int(num[1]):
                self.leaderboard.insert(x,["___",self.count])
                self.get_name(x)
                self.leaderboard.pop()
                self.save_highscores()
                break

    def get_name(self, index) -> None:
        """
        Gets user input for leaderboard name if user gets new high score

        :param index: where user is on in leaderboard
        """
        name_leader = "___"
        count_name = 0
        loop_name = True
        while loop_name:
            self.draw_leaderboard(True)
            text1 = self.base_font.render("New High Score",True,"black")
            text2 = self.base_font.render("Enter your name",True,"black")
            self.window.blit(text1, (200, 140))
            self.window.blit(text2, (200, 200))
            pygame.display.update()
            if count_name == 3:
                pygame.time.wait(1000)
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    name_leader = "CPU"
                    loop_name = False
                    self.running = False
                    self.running_bird = False
                if event.type == pygame.KEYDOWN:
                    key_pressed = pygame.key.name(event.key)
                    if key_pressed.isalpha() and len(key_pressed) <= 1:
                        name_leader = name_leader.replace("_",key_pressed,1)
                        count_name += 1
                    if event.key == pygame.K_ESCAPE:
                        name_leader = "CPU"
                        loop_name = False
            self.leaderboard[index][0] = name_leader

    def save_highscores(self) -> None:
        """
        Saves leaderboard onto 'data.csv'
        """
        with open("data.csv","w") as output_file:
            con = csv.writer(output_file,delimiter=",")
            for num in self.leaderboard:
                con.writerow(num)

    def draw_bird(self) -> None:
        """
        Updates screen to the original flappy bird game.
        """
        text_control = self.base_font.render("Press SPACE to start", True, "black")
        self.window.blit(self.back, (0, 0))
        self.window.blit(self.bird_right, (self.bird_hit_right.x, self.bird_hit_right.y))
        if not self.active:
            self.window.blit(text_control,(self.width/3,self.height/2))
        for num in range(0, len(self.pipe_up_list)):
            self.window.blit(self.pipe_up, (self.pipe_up_list[num].x, self.pipe_up_list[num].y - 10))
        for num in range(0, len(self.pipe_down_list)):
            self.window.blit(self.pipe_down, (self.pipe_down_list[num].x, self.pipe_down_list[num].y - 10))
        for x, num in enumerate(self.current_score):
            self.window.blit(self.scorecards[num], (self.score_x * (x + 1), self.score_y))
        pygame.display.update()

    def draw_title(self) -> None:
        """
        Draws the title screen
        """
        text_controls1 = self.base_font.render("F to start Flappy Bird", True, "black")
        text_controls2 = self.base_font.render("C to start Combat Game", True, "black")
        text_controls3 = self.base_font.render("L to start Leaderboard", True, "black")
        text_controls4 = self.base_font.render("ESCAPE to get back to Title Screen", True, "black")
        pygame.draw.rect(self.window,(78,192,202),pygame.Rect(0,0,self.width,self.height))
        self.window.blit(self.title, (0, 60))
        self.window.blit(text_controls1,(20,20))
        self.window.blit(text_controls2,(20,60))
        self.window.blit(text_controls3,(20,100))
        self.window.blit(text_controls4,(20,140))
        pygame.display.update()

    def draw_combat(self) -> None:
        """
        Draws the combat game screen
        """
        text_controls_right1 = self.base_font.render("WASD to move",True,"black")
        text_controls_right2 = self.base_font.render("Left Shift to shoot", True, "black")
        text_controls_left1 = self.base_font.render("Arrow Keys to move", True, "black")
        text_controls_left2 = self.base_font.render("Right Shift to shoot", True, "black")
        temp_x = self.width - 50
        self.window.blit(self.back, (0, 0))
        if not self.active_combat:
            self.window.blit(text_controls_right1,(15,60))
            self.window.blit(text_controls_right2,(15,100))
            self.window.blit(text_controls_left1,(self.middle.x+5,60))
            self.window.blit(text_controls_left2,(self.middle.x+5,100))
        pygame.draw.rect(self.window, "black", self.middle)
        self.window.blit(self.bird_right, (self.bird_hit_right.x, self.bird_hit_right.y))
        self.window.blit(self.bird_left, (self.bird_hit_left.x, self.bird_hit_left.y))
        for hit in self.bullet_right_list:
            self.window.blit(self.bullet_right, (hit.x, hit.y))
        for hit in self.bullet_left_list:
            self.window.blit(self.bullet_left, (hit.x, hit.y))
        for x, num in enumerate(self.current_score_left):
            self.window.blit(self.scorecards[num], (self.score_x * (x + 1), self.score_y))
        for x, num in enumerate(self.current_score_right):
            self.window.blit(self.scorecards[num], (temp_x + (self.score_x * x), self.score_y))
        pygame.display.update()

    def draw_leaderboard(self, new=False) -> None:
        """
        Draws leaderboard

        :param new: if count is a new high score
        """
        text_top = self.base_font.render("Leaderboard",True,"black")
        text_delete1 = self.base_font.render("Press BACKSPACE to", True, "black")
        text_delete2 = self.base_font.render("refresh Leaderboard", True,"Black")
        text_randomize1 = self.base_font.render("Press R to", True, "black")
        text_randomize2 = self.base_font.render("randomize Leaderboard", True, "black")
        self.window.blit(self.back,(0,0))
        self.window.blit(text_top,(30,40))
        for y, num in enumerate(self.leaderboard):
            text_temp = self.base_font.render(f"{num[0]}",True,"black")
            for x, score in enumerate(str(num[1])):
                self.window.blit(self.scorecards[int(score)],(120+(x*15),110+(y*60)))
            self.window.blit(text_temp,(30,100+(y*60)))
        if not new:
            self.window.blit(text_delete1, (240, self.height - 200))
            self.window.blit(text_delete2, (240, self.height - 160))
            self.window.blit(text_randomize1, (240, self.height - 100))
            self.window.blit(text_randomize2, (240, self.height - 60))
            pygame.display.update()

    def main_leader(self) -> None:
        """
        Checks for key presses BACKSPACE, ESCAPE, R
        """
        while self.running_leader:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_leader = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running_leader = False
                    if event.key == pygame.K_BACKSPACE:
                        self.delete_highscores()
                    if event.key == pygame.K_r:
                        self.delete_highscores(True)
            self.draw_leaderboard()

    def main(self) -> None:
        """
        Continuously checks for either key F or C or L during title screen to start game.
        """
        self.bird_hit_right.x = 60
        self.bird_hit_right.y = self.height / 2
        while self.running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.running_bird = True
                        self.main_bird()
                    if event.key == pygame.K_c:
                        self.running_combat = True
                        self.main_combat()
                    if event.key == pygame.K_l:
                        self.running_leader = True
                        self.main_leader()
            self.draw_title()

        pygame.quit()

    def reset_bird(self) -> None:
        """
        Resets birds in combat game when one is hit.
        """
        self.bird_hit_right.x = 60
        self.bird_hit_right.y = self.height / 2
        self.bird_hit_left.x = self.width - 150
        self.bird_hit_left.y = self.height / 2
        self.bullet_left_list.clear()
        self.bullet_right_list.clear()
        self.active_combat = False

    def main_combat(self) -> None:
        """
        The main window for the combat game.
        """
        while self.running_combat:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_combat = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running_combat = False
                        self.count_right = 0
                        self.count_left = 0
                        self.reset_bird()
                    if event.key == pygame.K_LSHIFT:
                        self.combat_shoot_right()
                    if event.key == pygame.K_RSHIFT:
                        self.combat_shoot_left()
            self.key_press_combat()
            self.bullet_move()
            self.combat_collision()
            self.combat_score()
            self.draw_combat()

    def combat_shoot_right(self) -> None:
        """
        The right bird shoots
        """
        self.active_combat = True
        if len(self.bullet_right_list) < 4:
            self.bullet_right_list.append(
                pygame.Rect(self.bird_hit_right.x + self.bird_width, self.bird_hit_right.y + self.bird_height / 2,
                            self.bullet_width, self.bullet_height))

    def combat_shoot_left(self) -> None:
        """
        The left bird shoots
        """
        self.active_combat = True
        if len(self.bullet_left_list) < 4:
            self.bullet_left_list.append(
                pygame.Rect(self.bird_hit_left.x, self.bird_hit_left.y + self.bird_height / 2, self.bullet_width,
                            self.bullet_height))

    def bullet_move(self) -> None:
        """
        Moves the bullets
        """
        vel_bullet = 5
        for hit in self.bullet_right_list:
            hit.x += vel_bullet
        for hit in self.bullet_left_list:
            hit.x -= vel_bullet

    def combat_collision(self) -> None:
        """
        Checks if the bullets collided with either bird
        """
        for hit in self.bullet_left_list:
            if hit.x < -self.bullet_width:
                self.bullet_left_list.remove(hit)
            if hit.colliderect(self.bird_hit_right):
                self.count_right += 1
                self.reset_bird()
        for hit in self.bullet_right_list:
            if hit.x > self.width:
                self.bullet_right_list.remove(hit)
            if hit.colliderect(self.bird_hit_left):
                self.count_left += 1
                self.reset_bird()

    def key_press_combat(self) -> None:
        """
        Reads all key presses for Combat Game
        """
        move_speed = 3
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.bird_hit_right.x > 0:
            self.active_combat = True
            self.bird_hit_right.x -= move_speed
        if keys[pygame.K_w] and self.bird_hit_right.y > 0:
            self.active_combat = True
            self.bird_hit_right.y -= move_speed
        if keys[pygame.K_d] and self.bird_hit_right.x < self.width / 2 - self.bird_width:
            self.active_combat = True
            self.bird_hit_right.x += move_speed
        if keys[pygame.K_s] and self.bird_hit_right.y < self.height - self.bird_height:
            self.active_combat = True
            self.bird_hit_right.y += move_speed

        if keys[pygame.K_LEFT] and self.bird_hit_left.x > self.width / 2:
            self.active_combat = True
            self.bird_hit_left.x -= move_speed
        if keys[pygame.K_UP] and self.bird_hit_left.y > 0:
            self.active_combat = True
            self.bird_hit_left.y -= move_speed
        if keys[pygame.K_RIGHT] and self.bird_hit_left.x < self.width - self.bird_width:
            self.active_combat = True
            self.bird_hit_left.x += move_speed
        if keys[pygame.K_DOWN] and self.bird_hit_left.y < self.height - self.bird_height:
            self.active_combat = True
            self.bird_hit_left.y += move_speed

    def combat_score(self) -> None:
        """
        Updates combat games score.
        """
        self.current_score_left.clear()
        self.current_score_right.clear()
        temp_score_left = str(self.count_left)
        temp_score_right = str(self.count_right)
        for num in temp_score_left:
            self.current_score_left.append(int(num))
        for num in temp_score_right:
            self.current_score_right.append(int(num))

    def main_bird(self) -> None:
        """
        The main area for the original flappy bird game
        """
        while self.running_bird:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_bird = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.key_press_bird()
                    if event.key == pygame.K_ESCAPE:
                        self.running_bird = False
                        self.game_over_bird(True)
                        self.count = 0

            self.move_bird()
            self.move_pipe()
            self.score_bird()
            self.game_over_bird()
            self.draw_bird()

    def move_bird(self) -> None:
        """
        Moves the bird down 1 every tick when game is active
        """
        if self.active:
            if self.vel_bird > self.vel_min:
                self.vel_bird -= 1
            self.bird_hit_right.y -= self.vel_bird

    def move_pipe(self) -> None:
        """
        Moves the pipes every tick when game is active
        """
        if self.active:
            separation = 100
            for num in range(0, len(self.pipe_up_list)):
                up_y, down_y = self.random_y()
                if self.pipe_up_list[num].x < -self.pipe_width:
                    self.pipe_up_list[num].x = self.width + separation
                    self.pipe_up_list[num].y = up_y
                self.pipe_up_list[num].x -= self.vel_pipe
                if self.pipe_down_list[num].x < -self.pipe_width:
                    self.pipe_down_list[num].x = self.width + separation
                    self.pipe_down_list[num].y = down_y
                self.pipe_down_list[num].x -= self.vel_pipe

    def score_bird(self) -> None:
        """
        Updates score for flappy bird game
        """
        if self.active:
            for num in range(0, len(self.pipe_up_list)):
                if self.bird_hit_right.x >= self.pipe_up_list[num].x > self.bird_hit_right.x - self.vel_pipe:
                    self.count += 1
        temp_count = str(self.count)
        self.current_score.clear()
        for num in temp_count:
            self.current_score.append(int(num))

    def game_over_bird(self, reset=False) -> None:
        """
        Checks if the bird has collided with the ground, roof,  or a pipe
        Resets the Flappy Bird game

        :param reset: tells game to reset
        """
        for num in range(0, len(self.pipe_up_list)):
            if self.bird_hit_right.colliderect(self.pipe_up_list[num]) \
                    or self.bird_hit_right.colliderect(self.pipe_down_list[num]) \
                    or self.bird_hit_right.y + self.bird_hit_right.height > self.height \
                    or self.bird_hit_right.y < 0 \
                    or reset:
                self.active = False
                if not reset:
                    self.check_highscores()
                for number in range(0, len(self.pipe_up_list)):
                    self.pipe_up_list[number].x = self.width + self.distance_x * number
                    self.pipe_down_list[number].x = self.width + self.distance_x * number
                    self.bird_hit_right.y = self.height / 2

    def random_y(self) -> tuple:
        """
        Creates two random ints used to place the pipes y-cord

        :return: Tuple of two ints used to place the pipes y-cord
        """
        rand = random
        down_y = rand.randint(50, 320) - self.pipe_down.get_height()
        up_y = down_y + self.distance_y + self.pipe_down.get_height()
        return up_y, down_y

    def key_press_bird(self) -> None:
        """
        Starts movement in Flappy Bird game
        """
        if not self.active:
            self.active = True
            self.count = 0
        self.vel_bird = self.vel_max


if __name__ == "__main__":
    GUI()