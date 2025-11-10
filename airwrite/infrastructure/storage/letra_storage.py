from pathlib import Path
from typing import Dict , Optional
from airwrite.domain.entities.letra import LetraEntity
from airwrite.infrastructure.opencv.trazo_extractor import generar_trazo_desde_imagen
import logging

logger = logging.getLogger(__name__)
 
""" Carga las letras desde la carpeta 'media/' """
class LetraStorage:
    def __init__(self, carpeta_media: str = "media"):
        self.carpeta_media = Path(carpeta_media).resolve()
        self._cache:Dict[str,LetraEntity]= {}
        
    
    def cargar_letras(self, generate_trazos:bool = True, n_points:int =64) -> Dict[str , LetraEntity]:
        if not self.carpeta_media.exists():
            raise FileNotFoundError(f"No se encontro la carpeta : {self.carpeta_media}") 
        
        letras : Dict[str, LetraEntity]= {}
        letra_id = 1
        
        """ Recorre las subcarpetas de media (letra , numero) """
        for subcarpeta in sorted(self.carpeta_media.iterdir()):
            if not  subcarpeta.is_dir():
                continue
            for archivo in sorted(subcarpeta.iterdir()):
                if archivo.suffix.lower() != ".png":
                    continue
                nombre = archivo.stem.upper()
                
                """ Limpia de prefijos en las imagenes """
                if nombre.startswith("LETRA_"):
                    caracter = nombre.replace("LETRA_", "")
                elif nombre.startswith("NUMERO_"):
                    caracter = nombre.replace("NUMERO_", "")
                else:
                    caracter = nombre
                       
                imagen_ruta = str(archivo.resolve())
                letra = LetraEntity(id=letra_id, caracter=caracter, imagen=imagen_ruta)
                letra_id += 1 
                
                """ Generar trazo de referencia si se solicita """
                if generate_trazos:
                    try:
                        trazo_ref = generar_trazo_desde_imagen(imagen_ruta, n_points=n_points)
                        letra.trazos = [trazo_ref]
                        letra.contorno = trazo_ref.coordenadas[:]
                    except Exception as e:
                        logger.warning("No se pudo generar trazo para %s: %s", imagen_ruta,e)
                letras[caracter] = letra
                self._cache[caracter] = letra
        return letras
    
    """ Devuelve una letra desde caché o intenta buscarla en las subcarpetas """
    def obtener_letra(self, caracter:str) -> Optional[LetraEntity]:
        c = caracter.upper()
        if c in self._cache:
            return self._cache[c]
        letra_id = max([l.id for l in self._cache.values()], default=0) + 1
        """ Intentar cargar la letra directamente (sin generar trazo)"""
        for posible in self.carpeta_media.rglob(f"{c}.png"):
            imagen_ruta = str(posible.resolve())
            letra = LetraEntity(caracter=c, imagen=imagen_ruta)
            letra_id += 1

            try:
                trazo_ref = generar_trazo_desde_imagen(imagen_ruta, n_points=64)
                letra.trazos = [trazo_ref]
                letra.contorno = trazo_ref.coordenadas[:]
            except Exception as e:
                logger.warning("No se pudo generar trazo para %s: %s", imagen_ruta, e)

            self._cache[c] = letra
            return letra

        logger.error(f"No se encontró la imagen para el caracter '{caracter}' en {self.carpeta_media}")
        return None

    def listar_letras_disponibles(self):
        return list(self._cache.keys())