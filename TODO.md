# TODO: Optimización del Sistema de Trazos en AirWrite

## Análisis de Rendimiento
- [x] Identificar causas de lentitud: Procesamiento CV en cada frame (absdiff, threshold, dilate, Canny), streaming de video a alta resolución, falta de caching de modelos de texto, operaciones innecesarias en loop.
- [x] Comparar con código original: Script Python simple corre localmente sin web streaming, más rápido.

## Optimizaciones de Código
- [ ] Optimizar `drawing_loop.py`:
  - Reducir resolución de frames (target_size más pequeño o escalado).
  - Aumentar `min_dist` para reducir frecuencia de dibujado.
  - Simplificar detección de marcador (eliminar GaussianBlur si no es necesario).
  - Reducir operaciones CV innecesarias.
- [x] Optimizar `evaluar_trazo.py`:
  - Cachear modelos de texto generados.
  - Reducir valores de BAND_DILATE y STROKE_DILATE.
  - Usar operaciones CV más eficientes (e.g., bitwise en lugar de múltiples dilates).
- [x] Optimizar `trazos.py`:
  - Agregar caching para modelos de texto.
  - Optimizar streaming de video (reducir fps si necesario).
  - Evitar regenerar modelos en cada request.
- [x] Optimizar `trazo_extractor.py`:
  - Reducir valores de BAND_DILATE y STROKE_DILATE para mejor rendimiento.

## Mejoras de UI
- [ ] Agregar alerta de switch en `index.js`:
  - Mostrar alerta con colores: rojo (<45%), amarillo (45-70%), verde (>70%).
  - Incluir mensaje motivacional y porcentaje de similitud.
  - Reemplazar alert() con notificación personalizada.
- [ ] Actualizar `index.html` si es necesario para la alerta.

## Pruebas y Validación
- [ ] Probar rendimiento después de cambios.
- [ ] Verificar que el trazado funcione correctamente y sea fluido.
- [ ] Asegurar compatibilidad con código original.

## Notas Adicionales
- El sistema actual usa Django con OpenCV para web, mientras que el original es un script local.
- Enfocarse en reducir carga computacional para lograr fluidez similar al original.
