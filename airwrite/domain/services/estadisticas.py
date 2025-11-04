from domain.entities.usuario import Usuario

class EstadisticasService:
    def __init__(self, usuario:Usuario):
        self.usuario = usuario
    
    """ Retorna un diccionario con el promedio de time por letra practicada"""    
    def promedio_tiempo_por_letra(self) -> dict:
        resultados = {}
        for letra in self.usuario.letras_practicadas:
            resultados[letra.caracter] = letra.tiempo_total()/ max(1, letra.numero_trazos())
        return resultados
      
    """ Calcula tiempo total practicado por usuario (todas las letras)"""
    def tiempo_total_usuario(self) -> float:
        return sum(letra.tiempo_total() for letra in self.usuario.letras_practicadas)
    
    def nivel_promedio(self) -> float:
        if not self.usuario.letras_practicadas:
            return 0.0
        return sum(letra.dificultad for letra in self.usuario.letras_practicadas) / len(self.usuario.letras_practicadas)
     
    """ Devuelve un resumen general del rendimiento del usuario """
    def resumen_general(self) -> dict:
        return{
            "usuario" : self.usuario.nombre,
            "nivel _actual":self.usuario.nivel,
            "letras_practicadas" : len(self.usuario.letras_practicadas),
            "tiempo_total": self.tiempo_total_usuario(),
            "nivel_promedio" : self.nivel_promedio(),
            "promedio_tiempo_por_letra": self.promedio_tiempo_por_letra(),
            
        }