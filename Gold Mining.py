import pygame
import os

pygame.init()


''' 1. 기본 설정 '''
''' 1-1. 화면'''
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height)) # (x, y) 해당 크기 디스플레이 생성
pygame.display.set_caption("GOLD MINER") # 제목 표시
''' 1-2. font '''
''' 1-3. FPS '''
''' 1-4. 음악 '''

''' 2. 게임 내 요소 '''
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

    pygame.display.update() # 화면 업데이트

''' 4. 종료 '''
pygame.quit()