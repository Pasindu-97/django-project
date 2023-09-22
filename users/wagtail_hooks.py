from wagtail import hooks

from users.authentication import create_user, delete_user


@hooks.register("after_create_user")
def do_after_create_user(request, user):
    create_user(user.username)


@hooks.register("after_delete_user")
def do_after_delete_user(request, user):
    delete_user(user.username)
