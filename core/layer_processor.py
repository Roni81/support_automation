# core/layer_processor.py
import trimesh
import numpy as np
from typing import List
from .morphological_processor import MorphologicalProcessor

class LayerProcessor:
    """STL 파일을 레이어별로 처리하는 클래스"""
    
    def __init__(self, layer_height: float = 0.05, resolution: float = 0.1):
        self.layer_height = layer_height
        self.resolution = resolution
        self.morph_processor = MorphologicalProcessor()
    
    def slice_mesh_to_layers(self, mesh: trimesh.Trimesh) -> List[np.ndarray]:
        """STL 메시를 레이어별 이미지로 슬라이싱"""
        layers = []
        z_min, z_max = mesh.bounds[0][2], mesh.bounds[1][2]
        
        # 각 레이어 높이에서 슬라이싱
        for z in np.arange(z_min, z_max, self.layer_height):
            # 특정 높이에서 메시 슬라이싱
            slice_2d = mesh.section(plane_origin=[0, 0, z], 
                                   plane_normal=[0, 0, 1])
            
            if slice_2d is not None:
                # 2D 슬라이스를 이미지로 변환
                layer_image = self._slice_to_image(slice_2d, mesh.bounds)
                layers.append(layer_image)
            else:
                # 빈 레이어 추가
                layers.append(np.zeros((512, 512), dtype=np.uint8))
        
        return layers
    
    def _slice_to_image(self, slice_2d, bounds) -> np.ndarray:
        """2D 슬라이스를 이미지로 변환"""
        # 이미지 크기 설정 (512x512 픽셀)
        img_size = 512
        image = np.zeros((img_size, img_size), dtype=np.uint8)
        
        if slice_2d.entities:
            # 바운딩 박스 계산
            x_min, x_max = bounds[0][0], bounds[1][0]
            y_min, y_max = bounds[0][1], bounds[1][1]
            
            # 스케일링 팩터 계산
            scale_x = img_size / (x_max - x_min)
            scale_y = img_size / (y_max - y_min)
            scale = min(scale_x, scale_y) * 0.9  # 여백 추가
            
            # 중심점 계산
            center_x = img_size // 2
            center_y = img_size // 2
            
            # 각 엔티티를 이미지에 그리기
            for entity in slice_2d.entities:
                if hasattr(entity, 'points'):
                    points = entity.points(slice_2d.vertices)
                    # 좌표 변환
                    scaled_points = []
                    for point in points:
                        x = int(center_x + (point[0] - (x_min + x_max)/2) * scale)
                        y = int(center_y + (point[1] - (y_min + y_max)/2) * scale)
                        scaled_points.append([x, y])
                    
                    # 폴리곤 채우기
                    if len(scaled_points) > 2:
                        pts = np.array(scaled_points, np.int32)
                        cv2.fillPoly(image, [pts], 255)
        
        return image
