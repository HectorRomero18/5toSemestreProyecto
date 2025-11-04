from pathlib import Path
from typing import Dict , Optional
from domain.entities.letra import LetraEntity
from infrastructure.opencv.trazo_extractor import generar_trazo_desde_imagen
from domain.entities.trazo import Trazo
import logging

logger = logging.getLogger(__name__)

""" Carga las letras desde la carpeta 'media/' """
class LetraStorage:
    def __init__(self, carpeta_media: str = "media"):
        self.carpeta_media = Path(carpeta_media)
        self._cache:Dict[str,LetraEntity]= {}
        
    
    def cargar_letras(self, generate_trazos:bool = True, n_points:int =64) -> Dict[str , LetraEntity]:
        if not self.carpeta_media.exists():
            raise FileNotFoundError(f"No se encontro la carpeta : {self.carpeta_media}") 
        
        letras : Dict[str, LetraEntity]= {}
        
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
                letra = LetraEntity(caracter=caracter, imagen=imagen_ruta)
                
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
        """ Intentar cargar la letra directamente (sin generar trazo)"""
        folder = self.carpeta_media
        for sub in folder.iterdir():
            posible= sub/ f"{c}.png"
            if posible.exists():
                letra = LetraEntity(caracter=c , imagen =str(posible.resolve()))
                self._cache[c]= letra
                return letra
        return None
        raise FileNotFoundError(f"No se encontro la imagen para el caracter '{caracter}'")
    
    def listar_letras_disponibles(self):
        return list(self._cache.keys())