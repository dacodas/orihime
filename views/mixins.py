import collections

class UseCurrentUserMixin():

    # Or restrict by this... Or can that just be handled with permissions_clases?
    # def get_queryset(self):
    #     return self.request.user.accounts.all()
    def create(self, request, *args, **kwargs):

        newQueryDict = request.data.copy()
        newQueryDict['user'] = request.user.email
        fauxRequest = collections.namedtuple('Request', 'data')(newQueryDict)

        return super(UseCurrentUserMixin, self).create(fauxRequest, *args, **kwargs)
