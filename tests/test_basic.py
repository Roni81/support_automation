# tests/test_basic.py
import sys
import os

# 프로젝트 루트 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)


import numpy as np
import cv2
from core.morphological_processor import MorphologicalProcessor

def test_external_support():
    """외부 서포트 생성 테스트"""
    # 테스트용 이미지 생성
    lower_layer = np.zeros((100, 100), dtype=np.uint8)
    cv2.rectangle(lower_layer, (20, 20), (80, 80), 255, -1)
    
    upper_layer = np.zeros((100, 100), dtype=np.uint8)
    cv2.rectangle(upper_layer, (10, 10), (90, 90), 255, -1)
    
    # 서포트 생성
    processor = MorphologicalProcessor()
    support_area = processor.generate_external_support_area(lower_layer, upper_layer)
    
    # 결과 확인
    assert support_area is not None
    assert support_area.shape == (100, 100)
    print("외부 서포트 생성 테스트 통과!")

def test_internal_support():
    """내부 서포트 생성 테스트"""
    # 도넛 모양 테스트 이미지
    layer = np.zeros((100, 100), dtype=np.uint8)
    cv2.circle(layer, (50, 50), 40, 255, -1)  # 외부 원
    cv2.circle(layer, (50, 50), 20, 0, -1)   # 내부 원 (구멍)
    
    processor = MorphologicalProcessor()
    internal_support = processor.generate_internal_support_area(layer)
    
    assert internal_support is not None
    print("내부 서포트 생성 테스트 통과!")

if __name__ == "__main__":
    test_external_support()
    test_internal_support()
    print("모든 기본 테스트 통과!")
