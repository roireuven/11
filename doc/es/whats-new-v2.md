# Novedades de v2.3/v2.4

Esta guía resume las principales características agregadas en **stable v2.3** y **stable v2.4** de HotelRestaurantMini-MartManagement.

**Sitios estables en vivo:**

| Versión | URL |
|---------|-----|
| **v2.3** | [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) |
| **v2.4** | [hotel-restaurant-minimart2-4.web.app](https://hotel-restaurant-minimart2-4.web.app/) |
| **Desarrollo** | [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) |

---

## Interfaz completa en 21 idiomas

La interfaz de usuario de la aplicación web está disponible en **21 idiomas**: inglés, español, francés, alemán, japonés, coreano, árabe, hindi, tailandés, vietnamita, indonesio, turco, ruso, italiano, holandés, polaco, hebreo, laosiano, portugués (Brasil), chino (simplificado) y chino (tradicional).

### Dónde cambiar el idioma

| Pantalla | Cómo |
|--------|-----|
| **Iniciar sesión/configurar** | Menú desplegable de idioma en el encabezado (antes de iniciar sesión) |
| **Después de iniciar sesión** | Selector de configuración regional de la barra superior o **Localización** en el menú |
| **Configuración** | Sección de idioma de la aplicación |

La preferencia se guarda en el almacenamiento del navegador (`hotel_mgr_uiLocale`).

### RTL (de derecha a izquierda)

**Árabe** y **hebreo** habilitan el diseño RTL para toda la aplicación. Los formularios modales utilizan una alineación mejorada para que las etiquetas y las entradas se lean correctamente tanto en lenguajes LTR como RTL.

---

## Configuración por primera vez (traducido)

El asistente de configuración está completamente localizado:

- Nombre del negocio/hotel
- Texto del encabezado del sistema
- Campos de nombre de usuario, correo electrónico y contraseña de administrador
- Todos los botones y mensajes de validación.

Después de la configuración, el nombre del hotel se almacena y se muestra en el encabezado de la aplicación donde se configuró.

---

## Acciones rápidas del panel (cuadrícula PMS)

El **Panel** muestra una cuadrícula de botones **+** azules para tareas comunes:

| Botón | Abre |
|--------|--------|
| Añadir habitación | Nueva forma de habitación |
| Añadir Reserva | Nuevo formulario de reserva |
| Agregar invitado | Nuevo formulario de invitado |
| Agregar tarea | Nuevo ticket de mantenimiento |
| Agregar servicio | Nueva solicitud de servicio |
| Agregar factura | Nuevo formulario de factura |
| Agregar existencias | Nuevo artículo de inventario |
| Agregar menú | Nuevo elemento de menú |
| Agregar artículo de la tienda | Nueva tienda / artículo mini-mart |
| Agregar usuario | Nueva cuenta de personal |

**Nota:** *Agregar limpieza* y *Agregar transacción* se eliminaron de esta cuadrícula (v2.4). Utilice la barra lateral para **Limpieza** y **Transacciones** cuando sea necesario.

---

## Formas modales traducidas

Los cuadros de diálogo para agregar y editar están traducidos a los 21 idiomas, incluidos:

- **Mantenimiento** — ticket nuevo (habitación, prioridad, problema, notas)
- **Factura** — agregar/editar (huésped, habitación, fechas, montos, estado de pago)
- **Inventario**: agregar/editar artículo (nombre, código de barras, categoría, cantidad, disponibilidad de POS)
- **Elemento del menú**: agregar/editar (nombre, icono, precio, categoría, imagen, enlace de stock)
- **Artículo de la tienda**: agregar/editar (nombre, precio, categoría, ícono de estante, código de barras, stock)- **Cuenta de usuario** — agregar/editar (nombre, correo electrónico, contraseña, función)

Las etiquetas de carga de imágenes (“desde el dispositivo”, “o URL de la imagen”) siguen el idioma activo.

---

## Reserva → Nuevo huésped

Al crear una **reserva**, si el huésped aún no está en el directorio:

1. Toca **+ Nuevo huésped** (o equivalente) en el formulario de reserva.
2. Complete el modal **Nuevo Huésped** (nombre, pasaporte, nacionalidad, fecha de nacimiento, forma de pago, contacto, notas).
3. Toca **Agregar huésped y regresar**: regresarás a la reserva con el nuevo huésped seleccionado.

El selector de nacionalidad (lista de búsqueda) también está traducido.

---

## Documentación

- Esta guía de **Novedades** está disponible en los 21 idiomas de la documentación.
- Abra documentos desde la aplicación: **barra superior → Documentación**, **☰ Ayuda → Documentación** o **navegación inferior → Documentos**.
- URL independiente: `/doc/?lang={code}#/whats-new-v2`

---

## Para administradores

| Tarea | Dónde |
|------|--------|
| Capacitar al personal sobre el cambio de idioma | [Localization](localization.md) |
| Configurar propiedad después de la actualización | [Settings & configuration](settings-and-configuration.md) |
| Implementar actualizaciones | [Deployment](deployment.md) — `npm run deploy:stable` publica en v2.3 y v2.4 |

---

## Guías relacionadas

- [Localization](localization.md) — idiomas, RTL, archivos locales
- [First-time setup](first-time-setup.md) — configuración inicial
- [Navigation & UI](navigation-and-ui.md): tablero, barra lateral, navegación móvil
- [Hotel operations](hotel-operations.md) — reservas e invitados
- [Deployment](deployment.md) — desarrollo versus estable v2.3 / v2.4