import pygame
import os
import math
from random import*

pygame.init()

class Gemstone(pygame.sprite.Sprite): # 보석 생성 클래스
    def __init__(self, image, position, price, speed):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center = position)
        self.price = price
        self.speed = speed
    
    def set_position(self, position, angle): # 집게로 잡은 물체 위치 조정 함수
        r = self.rect.size[0] // 2
        rad_angle = math.radians(angle)
        to_x = r * math.cos(rad_angle)
        to_y = r * math.sin(rad_angle)
        self.rect.center = (position[0] + to_x, position[1] + to_y)


def setup_gemstones(): # 보석 배치 및 인자(가격, 속도) 설정 함수
    global level, gemstone_images, center_of_small_golds, center_of_big_golds, center_of_stones, center_of_diamonds

    small_gold_price, small_gold_speed = 100, 5
    big_gold_price, big_gold_speed = 300, 2
    stone_price, stone_speed = 10, 2
    diamond_price, diamond_speed = 600, 7

    num_of_small_golds = level + 1
    width_of_small_gold = gemstone_images[0].get_rect()[2]
    height_of_small_gold = gemstone_images[0].get_rect()[3]
    for i in range(0, num_of_small_golds):
        # center_of_small_golds.append((randrange(width_of_small_gold, screen_width - width_of_small_gold), randrange(200, screen_height - height_of_small_gold)))
        gemstone_group.add(Gemstone(gemstone_images[0], (randint(int(width_of_small_gold + i*(screen_width / num_of_small_golds)), int((i + 1)*(screen_width / num_of_small_golds) - width_of_small_gold)), randint(200, screen_height - height_of_small_gold)), small_gold_price, small_gold_speed))
        
    num_of_big_golds = level + 1
    width_of_big_gold = gemstone_images[1].get_rect()[2]
    height_of_big_gold = gemstone_images[1].get_rect()[3]
    for i in range(0, num_of_big_golds):
        # center_of_big_golds.append((randrange(width_of_big_gold, screen_width - width_of_big_gold), randrange(200, screen_height - height_of_big_gold)))
        gemstone_group.add(Gemstone(gemstone_images[1], (randint(int(width_of_big_gold + i*(screen_width / num_of_big_golds)), int((i + 1)*(screen_width / num_of_big_golds) - width_of_big_gold)), randint(200, screen_height - height_of_big_gold)), big_gold_price, big_gold_speed))

    num_of_stones = level + 1
    width_of_stone = gemstone_images[2].get_rect()[2]
    height_of_stone = gemstone_images[2].get_rect()[3]
    for i in range(0, num_of_stones):
        # center_of_stones.append((randrange(width_of_stone, screen_width - width_of_stone), randrange(200, screen_height - height_of_stone)))    
        gemstone_group.add(Gemstone(gemstone_images[2], (randint(int(width_of_stone + i*(screen_width / num_of_stones)), int((i + 1)*(screen_width / num_of_stones) - width_of_stone)), randint(200, screen_height - height_of_stone)), stone_price, stone_speed))

    num_of_diamonds = (level // 2) + 1
    width_of_diamond = gemstone_images[3].get_rect()[2]
    height_of_diamond = gemstone_images[3].get_rect()[3]
    for i in range(0, num_of_diamonds):
        # center_of_diamonds.append((randrange(width_of_diamond, screen_width - width_of_diamond), randrange(200, screen_height - height_of_diamond)))
        gemstone_group.add(Gemstone(gemstone_images[3], (randint(int(width_of_diamond + i*(screen_width / num_of_diamonds)), int((i + 1)*(screen_width / num_of_diamonds) - width_of_diamond)), randint(200, screen_height - height_of_diamond)), diamond_price, diamond_speed))
    
def check_setup_gemstone(): # 겹치는 보석 재생성 함수 일단 스킵
    for gemstone in gemstone_group:
            pygame.sprite.spritecollide(gemstone, gemstone_group, False)

class Claw(pygame.sprite.Sprite): # 집게 클래스
    def __init__(self, image, position):
        super().__init__()
        self.image = image # 집게 회전 시 이미지 업데이트
        self.original_image = image # 초기의 이미지 보관
        self.rect = image.get_rect(center = position)

        self.offset = pygame.math.Vector2(default_offset_x_claw, 0) # 해당 좌표만큼 이미지 이동 변수, Vector2는 rotate 함수 지원(각도 넣으면 좌표 자동 계산)
        self.position = position

        self.direction = LEFT # 집게 이동 방향
        self.angle_speed = 2.5 # 집게 각속도(프레임당)
        self.angle = 10 # 최초 각동 정의
    
    def update(self, to_x):
        if self.direction == LEFT: # 방향별 집게 이동 처리
            self.angle += self.angle_speed
        elif self.direction == RIGHT:
            self.angle -= self.angle_speed
        if self.angle > 170:
            self.angle = 170
            self.direction = RIGHT
        elif self.angle < 10:
            self.angle = 10
            self.direction = LEFT
        
        self.offset.x += to_x # offset의 x좌표를 이동시킬 to_x만큼 업데이트

        self.rotate()
    
    def rotate(self): # 집게 이미지 회전 함수
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1) # 회전할 원본 이미지, 회전 각도와 방향, 이미지 크기
        offset_rotated = self.offset.rotate(self.angle) # offset 회전된 값을 받는 변수, rect값에 적용 위함
        self.rect = self.image.get_rect(center = self.position + offset_rotated) # self.image가 회전 된 이미지를 가져왔으니, claw rect정보를 새롭게 만들어진 이미지로부터 중심점 업뎃   
        # 이미지 회전 시 rect의 left, top은 고정, height, width 변경됨, 이 변경 된 height, width의 rect정보를 업데이트 해줘야 중심이 맞음
    
    def set_init_state(self): # 집게 원위치 후 재회전 처리 함수
        self.offset.x = default_offset_x_claw
        self.angle = 10
        self.direction = LEFT
    
    def draw(self, screen): # 
        screen.blit(self.image, self.rect)
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5) # position ~ rect 중심까지 잇는 선


def update_score(score):
    global current_score
    current_score += score

def setup_level(): # 레벨 및 레벨 당 타겟 점수 설정 함수
    global level, current_score, target_score, game_result, total_time, elapsed_time
    if current_score >= target_score:
        screen.fill(BLACK)
        game_result = "Mission Complete"
        txt_game_result = game_result_font.render(game_result, True, WHITE)
        rect_game_result = txt_game_result.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
        screen.blit(txt_game_result, rect_game_result)
        level += 1
        target_score = target_score + (level - 1) * 500
        current_score = 0
        plus_time = 60 - (total_time - elapsed_time)
        total_time = int(total_time + plus_time)
        setup_gemstones()

def display_level(): # 레벨 표시 함수
    txt_level = game_font.render(f"Level {level}", True, BLACK)
    screen.blit(txt_level, (30, 10))
    txt_curr_score = game_font.render(f"Current Score: {current_score}", True, BLACK)
    screen.blit(txt_curr_score, (30, 40))
    txt_target_score = game_font.render(f"Target Score: {target_score:,}", True, BLACK)
    screen.blit(txt_target_score, (30, 70))

def setup_time_over(time): # 타임오버 처리 함수
    global game_result, running
    txt_timer = game_font.render(f"{time}s left", True, BLACK)
    screen.blit(txt_timer, (1100, 10))
    time_over_font = pygame.font.SysFont("arialrounded", 60)
    if time < 0:
        screen.fill(BLACK)
        game_result = "Time Over"
        txt_game_result = game_result_font.render(game_result, True, WHITE)
        rect_game_result = txt_game_result.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
        screen.blit(txt_game_result, rect_game_result)
        running = False

''' 1. 기본 설정 '''
''' 1-1. 화면'''
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height)) # (x, y) 해당 크기 디스플레이 생성
pygame.display.set_caption("GOLD MINER") # 제목 표시

''' 1-2. font '''
game_font = pygame.font.SysFont("arialrounded", 30)
game_result_font = pygame.font.SysFont("arialrounded", 60)
''' 1-3. FPS '''
''' 1-4. 음악 '''

''' 2. 게임 내 요소 '''
center_of_small_golds = []
center_of_big_golds = []
center_of_stones = []
center_of_diamonds = []

level = 1
current_score = 0
target_score = 1000

total_time = 60
start_ticks = pygame.time.get_ticks()

game_result = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

default_offset_x_claw = 40
to_x = 0
move_speed = 12
return_speed = 20
caught_gemstone = None
LEFT = -1
RIGHT = +1
STOP = 0

''' 2-1. 배경 '''
current_path = os.path.dirname(__file__) # 현재 파일 위치 반환 변수
background = pygame.image.load(os.path.join(current_path, "background.png"))

''' 2-2. 스프라이트 '''
gemstone_images = [ # 이미지 불러오기
    pygame.image.load(os.path.join(current_path, "small_gold.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "big_gold.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "stone.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "diamond.png")).convert_alpha()]

gemstone_group = pygame.sprite.Group() # Group 정의: sprite 관리 편하게 하기 위함
setup_gemstones()
check_setup_gemstone()

claw_image = pygame.image.load(os.path.join(current_path, "claw.png")).convert_alpha() # 집게 이미지 불러오기, 투명한 부분 무시하는 함수 alpha
claw = Claw(claw_image, (screen_width // 2, 110))


''' 3. 메인루프(메인 이벤트 처리) '''
running = True
while running:
    ''' 3-1. FPS '''
    pygame.time.Clock().tick(30) # FPS 처리
    # print(pygame.time.Clock().tick(30))
    ''' 3-2. 이벤트 처리(키, 마우스, 종료 등) '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            claw.direction = STOP
            to_x = move_speed
    
    ''' 3-3. 게임 내 요소 위치 정의 '''
    if claw.rect.left < 0 or claw.rect.right > screen_width or claw.rect.bottom > screen_height:
        to_x = -return_speed # 집게 벽에 닿았을 때 귀환 처리
    if claw.offset.x < default_offset_x_claw:
        to_x = 0
        claw.set_init_state() # 원위치 귀환 시 초기화 처리
        if caught_gemstone: # 잡은 보석이 있다면 점수화 처리
            update_score(caught_gemstone.price)
            gemstone_group.remove(caught_gemstone)
            caught_gemstone = None
    ''' 3-4. 충돌처리 '''
    if not caught_gemstone: # 빈 집게 충돌 처리
        for gemstone in gemstone_group:
            if pygame.sprite.collide_mask(claw, gemstone): # 여백을 제외한 실제 이미지 출돌처리 함수
                caught_gemstone = gemstone
                to_x = -gemstone.speed
                break
    if caught_gemstone:
        caught_gemstone.set_position(claw.rect.center, claw.angle)
    ''' 3-5. 화면에 그리기 '''
    screen.blit(background, (0, 0)) # 배경화면 스크린 내 표시
    
    gemstone_group.draw(screen) # 스크린 내 보석 표시
    
    claw.update(to_x)
    claw.draw(screen)

    setup_level()

    display_level()

    # 시간 처리
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    setup_time_over(total_time - int(elapsed_time))

    pygame.display.update() # 화면 업데이트

''' 4. 종료 '''
pygame.time.delay(1000)
pygame.quit()