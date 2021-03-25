from django.http import Http404


class OwnerOnlyMixin(object):

    def has_permissions(self):
        return self.get_object().owner == self.request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404('You do not have permission.')
        return super(OwnerOnlyMixin, self).dispatch(
            request, *args, **kwargs)


class MembersOnlyMixin(object):

    def has_permissions(self):
        if not self.get_object() in self.request.user.user_rooms.all():
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404('You do not have permission.')
        return super(MembersOnlyMixin, self).dispatch(
            request, *args, **kwargs)
