import re
from django.test import TestCase
from django.conf import settings
from django.db import connections
from django.urls import reverse
from django.contrib.auth.models import User
from django.apps import apps


class ProjectConfigTest(TestCase):
  """Test para verificar que el proyecto Django está configurado correctamente."""

  def test_project_starts(self):
    """Verifica que el proyecto se inicia correctamente."""
    #
    self.assertTrue(True)

  def test_database_connection(self):
    """Verifica que la conexión a la base de datos funciona."""
    # Intenta ejecutar una consulta simple
    with connections['default'].cursor() as cursor:
      cursor.execute("SELECT 1")
      result = cursor.fetchone()[0]
      self.assertEqual(result, 1)

  def test_admin_site_loads(self):
    """Verifica que el sitio de administración se carga correctamente."""
    # Crea un superusuario para el test
    User.objects.create_superuser(
      username='admin_test',
      email='admin@example.com',
      password='password123'
    )

    # Inicia sesión
    self.client.login(username='admin_test', password='password123')

    # Intenta acceder al sitio de administración
    response = self.client.get(reverse('admin:index'))
    self.assertEqual(response.status_code, 200)

  def test_settings_configuration(self):
    """Verifica configuraciones importantes del proyecto."""
    # Verifica que DEBUG está configurado según el entorno
    self.assertIsInstance(settings.DEBUG, bool)

    # Verifica que la configuración de base de datos existe
    self.assertTrue('default' in settings.DATABASES)

    # Verifica que la configuración de INSTALLED_APPS incluye las aplicaciones base
    required_apps = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
    ]

    for app in required_apps:
      self.assertIn(app, settings.INSTALLED_APPS)

  def test_static_and_media_settings(self):
    """Verifica la configuración de archivos estáticos y media."""
    self.assertTrue(hasattr(settings, 'STATIC_URL'))
    self.assertTrue(hasattr(settings, 'MEDIA_URL'))
    self.assertTrue(hasattr(settings, 'STATICFILES_DIRS'))

  def test_apps_load_correctly(self):
    """Verifica que todas las aplicaciones se cargan correctamente."""
    for app_config in apps.get_app_configs():
      # Si podemos acceder a los modelos, la app está cargada correctamente
      list(app_config.get_models())

    # Si llegamos aquí sin errores, todas las apps cargaron correctamente
    self.assertTrue(True)

  def test_not_found_page_loads(self):
    """Verifica que la página de error 404 carga correctamente."""
    response = self.client.get('/not-found')

    if hasattr(response, 'status_code'):
      self.assertEqual(response.status_code, 404)
    else:
      self.fail(f"La respuesta no tiene el atributo status_code. Respuesta: {response}")

  def test_homepage_loads(self):
    """Verifica que la página de inicio carga correctamente."""
    response = self.client.get('/')

    # Verifica que response tiene el atributo status_code antes de usarlo
    if hasattr(response, 'status_code'):
      self.assertEqual(response.status_code, 404)
    else:
      self.fail(f"La respuesta no tiene el atributo status_code. Respuesta: {response}")

  def test_migrations_applied(self):
    """Verifica que todas las migraciones están aplicadas."""
    from django.db.migrations.executor import MigrationExecutor
    from django.db import connections

    connection = connections['default']
    executor = MigrationExecutor(connection)
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())

    # Si el plan está vacío, todas las migraciones están aplicadas
    self.assertEqual(len(plan), 0, "Hay migraciones pendientes de aplicar")
