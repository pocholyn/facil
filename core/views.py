
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages


def permission_denied(request, exception=None):
	"""Handler para errores 403: guarda un mensaje en sesión y redirige al dashboard.

	Esto permite mostrar un modal elegante en la página principal en lugar de la
	página 403 por defecto.
	"""
	msg = 'No tienes permisos para realizar esta acción.'
	# Guardar mensaje en sesión para que la plantilla lo muestre como modal
	request.session['permission_message'] = msg
	# También agregar un mensaje normal (opcional)
	messages.error(request, msg, extra_tags='permission')
	return redirect('dashboard')


def clear_permission_message(request):
	"""Endpoint para limpiar el mensaje de permiso almacenado en sesión.

	Espera un POST desde JavaScript (CSRF token incluido) y elimina la clave de sesión.
	"""
	if request.method == 'POST':
		request.session.pop('permission_message', None)
		return JsonResponse({'ok': True})
	return JsonResponse({'ok': False}, status=405)

# Create your views here.
