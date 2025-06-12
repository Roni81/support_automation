import cv2
import numpy as np
from typing import Tuple, List

class MorphologicalProcessor:
    # DLP 프린터용 형태학적 영상 처리 기반 서포트 제너레이터

    def __init__(self, kernel_size: int = 3):
        self.kernel_size = kernel_size
        self.kernel = np.ones((kernel_size, kernel_size), np.uint8)


    def generate_external_support_area(
            self, 
            lower_layer: np.ndarray,
            upper_layer: np.ndarray
        ) -> np.ndarray:
       
        
        # 위층과 아래층 단면 영상 간의 형태학적 연산을 통한 외부 서포터 영역 생성
        # 상위 레이어에서 하위 레이어를 뺀 차이 계산
        diff = cv2.subtract(upper_layer, lower_layer)
        
        # 형태학적 열림 연산 (노이즈 제거)
        opened = cv2.morphologyEx(diff, cv2.MORPH_OPEN, self.kernel)
        
        # 팽창 연산으로 서포터 영역 확장
        dilated = cv2.dilate(opened, self.kernel, iterations=1)
        
        return dilated
    
    
    def generate_internal_support_area(
            self,
            layer_image: np.ndarray,
            min_wall_thickness: int = 2
        ) -> np.ndarray:

        # 벽 두께를 고려한 커널 생성
        wall_kernel = np.ones((min_wall_thickness, min_wall_thickness), np.uint8)
        
        # 침식 연산 (벽 두께만큼 안쪽으로)
        eroded = cv2.erode(layer_image, wall_kernel, iterations=1)
        
        # 열림 연산 (침식 후 팽창)
        opened = cv2.morphologyEx(eroded, cv2.MORPH_OPEN, self.kernel)
        
        # 원본에서 열림 결과를 빼서 내부 공간 탐지
        internal_area = cv2.subtract(layer_image, opened)
        
        return internal_area