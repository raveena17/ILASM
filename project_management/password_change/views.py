from __future__ import unicode_literals

from django.shortcuts import render
from .forms import Password_reset_form
import ldap 
import sys
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


from project_management.settings import *

# Create your views here.


def ldap_password_management(request, id=None):
	message = None
	password_reset_form = Password_reset_form()
	if request.method == 'POST':
		try:
			con = ldap.initialize("ldap://" + LDAP_SERVER)
			con.simple_bind_s('cn=admin,dc=fifthgentech,dc=local', LDAP_PASSWORD)
			if request.POST['new_password'] == request.POST['confirm_password']:
				con.passwd_s("cn=" + str(request.user.username) +",ou=users,dc=fifthgentech,dc=local", str(request.POST["old_password"]), str(request.POST["new_password"]))
				message = messages.success(request, _('Password Changed Sucessfully'))
			else:
				message = messages.error(request, _('Invalid Password'))
		except Exception as e:
			message = messages.error(request, _('Failed Operation'))

	return render(
		request, 'password_change_form.html', {
		'password_reset_form': password_reset_form,
		'message': message
		}
	)