import pygame
import os
from random import*

pygame.init()

class Gemstone(pygame.sprite.Sprite): # 보석 생성 클래스
    def __init__(self, image, position, price, speed):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center = position)
        self.price = price
        self.speed = speed

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
        gemstone_group.add(Gemstone(gemstone_images[0], (randrange(width_of_small_gold, screen_width - width_of_small_gold), randrange(200, screen_height - height_of_small_gold)), small_gold_price, small_gold_speed))
        
    num_of_big_golds = level + 1
    width_of_big_gold = gemstone_images[1].get_rect()[2]
    height_of_big_gold = gemstone_images[1].get_rect()[3]
    for i in range(0, num_of_big_golds):
        # center_of_big_golds.append((randrange(width_of_big_gold, screen_width - width_of_big_gold), randrange(200, screen_height - height_of_big_gold)))
        gemstone_group.add(Gemstone(gemstone_images[1], (randrange(width_of_big_gold, screen_width - width_of_big_gold), randrange(200, screen_height - height_of_big_gold)), big_gold_price, big_gold_speed))

    num_of_stones = level + 1
    width_of_stone = gemstone_images[2].get_rect()[2]
    height_of_stone = gemstone_images[2].get_rect()[3]
    for i in range(0, num_of_stones):
        # center_of_stones.append((randrange(width_of_stone, screen_width - width_of_stone), randrange(200, screen_height - height_of_stone)))    
        gemstone_group.add(Gemstone(gemstone_images[2], (randrange(width_of_stone, screen_width - width_of_stone), randrange(200, screen_height - height_of_stone)), stone_price, stone_speed))

    num_of_diamonds = (level // 2) + 1
    width_of_diamond = gemstone_images[3].get_rect()[2]
    height_of_diamond = gemstone_images[3].get_rect()[3]
    for i in range(0, num_of_diamonds):
        # center_of_diamonds.append((randrange(width_of_diamond, screen_width - width_of_diamond), randrange(200, screen_height - height_of_diamond)))
        gemstone_group.add(Gemstone(gemstone_images[3], (randrange(width_of_diamond, screen_width - width_of_diamond), randrange(200, screen_height - height_of_diamond)), diamond_price, diamond_speed))
    
def check_setup_gemstone(): # 겹치는 보석 재생성 함수
    for gemstone in gemstone_group:
        if pygame.sprite.collide_mask(gemstone, gemstone):
            gemstone_group.remove(gemstone)
            gemstone_group.add(gemstone)

def setup_level(): # 레벨 및 레벨 당 타겟 점수 설정 함수
    global level, current_score, target_score, game_result, total_time
    if current_score >= target_score:
        screen.fill(BLACK)
        game_result = "Mission Complete"
        txt_game_result = game_result_font.render(game_result, True, WHITE)
        rect_game_result = txt_game_result.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
        screen.blit(txt_game_result, rect_game_result)
        level += 1
        target_score = target_score + (level - 1) * 500
        total_time = 60

def display_level(): # 레벨 표시 함수
    txt_level = game_font.render(f"Level {level}", True, BLACK)
    screen.blit(txt_level, (30, 10))

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

total_time = 3
start_ticks = pygame.time.get_ticks()

game_result = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
    ''' 3-3. 게임 내 요소 위치 정의 '''
    ''' 3-4. 충돌처리 '''
    ''' 3-5. 화면에 그리기 '''
    screen.blit(background, (0, 0)) # 배경화면 스크린 내 표시
    
    gemstone_group.draw(screen) # 스크린 내 보석 표시
    
    setup_level()

    display_level()

    # 시간 처리
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    setup_time_over(total_time - int(elapsed_time))

    pygame.display.update() # 화면 업데이트

''' 4. 종료 '''
pygame.time.delay(1000)
pygame.quit()