# main.py
import cv2
import numpy as np
from core.support_generator import DLPSupportGenerator

def main():
    # 서포트 생성기 초기화
    generator = DLPSupportGenerator(layer_height=0.05)
    
    # STL 파일 경로 (테스트용 파일 경로로 변경하세요)
    stl_file_path = "test_model.stl"
    
    try:
        # 서포트 생성
        print("서포트 생성 시작...")
        supported_layers = generator.generate_supports_for_stl(stl_file_path)
        
        # 결과 시각화 (처음 몇 레이어만)
        for i in range(min(5, len(supported_layers))):
            cv2.imshow(f'Layer {i}', supported_layers[i])
            cv2.waitKey(1000)  # 1초 대기
        
        cv2.destroyAllWindows()
        print(f"서포트 생성 완료! 총 {len(supported_layers)} 레이어")
        
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
