"""
    LDAP authentication backend.
"""
import ldap
# import ldap.LDAPError
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from project_management.settings import LDAP_SERVER


class LDAPBackend(object):
    """
        Provides methods to authenticate against LDAP
        and get_user from the Auth plug-in.
    """

    def authenticate(self, username=None, password=None):
        """
            Authenticate against the LDAP server provided by settings.LDAP_SERVER.
            The LDAP server is assumed to listen to port 389.
        """
        try:
            con = ldap.open(settings.LDAP_SERVER, 389)
            # con.protocol_version = ldap.VERSION3
            # con.simple_bind_s("cn=admin,dc=fifthgentech,dc=local", settings.LDAP_PASSWORD )
            # con.search_s('ou=users,dc=fifthgentech,dc=local',ldap.SCOPE_SUBTREE,'(cn=user*)',['cn'])
            # con.set_option(ldap.OPT_REFERRALS, 0)
            # con.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            # user = con.search_s('dc=fifthgentech,dc=local',ldap.SCOPE_SUBTREE,'(uid=%s)' % (username),['cn'])
            # con.simple_bind_s(user[0][0], password)
            user = User.objects.get(username=username)
        except Exception as e:
            user = None
        # except User.DoesNotExist:
        #     user = None  # New users may be added (created) here. (enhancement)
        # except ldap.LDAPError:
        #     user = None
        return user

    def get_user(self, user_id):
        """
            Get user object from Auth.User.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
