# core/support_generator.py
import cv2
import numpy as np
from typing import List, Tuple
from .layer_processor import LayerProcessor
from .morphological_processor import MorphologicalProcessor

class DLPSupportGenerator:
    """DLP 프린터용 서포트 자동 생성기"""
    
    def __init__(self, layer_height: float = 0.05):
        self.layer_processor = LayerProcessor(layer_height)
        self.morph_processor = MorphologicalProcessor()
        self.support_structures = []
    
    def generate_supports_for_stl(self, stl_file_path: str) -> List[np.ndarray]:
        """STL 파일에 대한 서포트 생성"""
        # STL 파일 로드
        mesh = trimesh.load(stl_file_path)
        print(f"메시 로드 완료: {len(mesh.vertices)} 정점, {len(mesh.faces)} 면")
        
        # 레이어별로 슬라이싱
        layers = self.layer_processor.slice_mesh_to_layers(mesh)
        print(f"총 {len(layers)} 레이어 생성")
        
        # 서포트가 포함된 레이어 생성
        supported_layers = self._generate_supported_layers(layers)
        
        return supported_layers
    
    def _generate_supported_layers(self, layers: List[np.ndarray]) -> List[np.ndarray]:
        """각 레이어에 서포트 구조 추가"""
        supported_layers = []
        
        for i, layer in enumerate(layers):
            current_layer = layer.copy()
            
            # 첫 번째 레이어가 아닌 경우 외부 서포트 생성
            if i > 0:
                external_support = self.morph_processor.generate_external_support_area(
                    layers[i-1], layer)
                current_layer = cv2.bitwise_or(current_layer, external_support)
            
            # 내부 서포트 생성
            internal_support = self.morph_processor.generate_internal_support_area(layer)
            current_layer = cv2.bitwise_or(current_layer, internal_support)
            
            supported_layers.append(current_layer)
            
            # 진행 상황 출력
            if i % 10 == 0:
                print(f"레이어 {i}/{len(layers)} 처리 완료")
        
        return supported_layers
