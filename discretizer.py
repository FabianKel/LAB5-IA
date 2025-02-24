#Task 1.1 Discretización de la imagen

import cv2
import numpy as np

class Discretizer:
    def __init__(self, cell_size):
        self.cell_size = cell_size
    
    def read_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("No se pudo leer la imagen.")
        return image
    
    def discretize(self, image):
        height = image.shape[0]  
        width = image.shape[1]   
        
        cell_height = height // self.cell_size
        cell_width = width // self.cell_size

        discrete_matrix = np.zeros((cell_height, cell_width), dtype=int)

        # Para cada celda de la matriz
        for i in range(cell_height):
            for j in range(cell_width):
                # Obtener región de la celda
                cell_region = image[i*self.cell_size:(i+1)*self.cell_size, j*self.cell_size:(j+1)*self.cell_size]
                
                avg_color = np.mean(cell_region, axis=(0,1))
                
                # Clasificar el color BGR
                blue = avg_color[0]
                green = avg_color[1]
                red = avg_color[2]

                # blanco (camino)
                if blue > 200 and green > 200 and red > 200:
                    discrete_matrix[i, j] = 0  
                
                # negro (pared)
                elif blue < 50 and green < 50 and red < 50:
                    discrete_matrix[i, j] = 1  
                
                # verde (meta)
                elif green > 150 and blue < 100 and red < 100:
                    discrete_matrix[i, j] = 2  
                
                # rojo (inicio)
                elif red > 150 and blue < 100 and green < 100:
                    discrete_matrix[i, j] = 3  

        return discrete_matrix

