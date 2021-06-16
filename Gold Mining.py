import pygame
import os

pygame.init()

def setup_level():
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

def display_level():
    txt_level = game_font.render(f"Level {level}", True, BLACK)
    screen.blit(txt_level, (30, 10))

def setup_time_over(time):
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

    setup_level()

    display_level()

    # 시간 처리
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    setup_time_over(total_time - int(elapsed_time))

    pygame.display.update() # 화면 업데이트

''' 4. 종료 '''
pygame.time.delay(1000)
pygame.quit()