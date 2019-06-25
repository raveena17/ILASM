"""
    Context processor. May be invoked from any view.
"""

def menu_and_privilege(request, user_name = ''):
    """
        Gets the menu list, also privileges and the user.
    """
    login_data = request.session.get('LoginData', '')
    if login_data and login_data.has_key('loginUserName'):
        user_name = login_data['loginUserName']
    return { 'userName' : user_name  }
