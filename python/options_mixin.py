from django.http.request import QueryDict
from django.shortcuts import redirect
from users.models import UserListingOptions
from django.http import JsonResponse


class FiltersMixin:

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['filter_cookie'] = self.filter_cookie or None
        context['expand_filters'] = self.request.COOKIES.get(
            self.filter_cookie) != None
        return context

    def save_user_options(self, request):
        filters_form = request.POST.get('filters_form')
        user_options = UserListingOptions.objects.update_or_create(
            key=self.key_for_options,
            user=request.user,
            defaults={'key': self.key_for_options,
                      'user': request.user, 'options': filters_form}
        )

    def get_user_options(self, request):

        user_options = UserListingOptions.objects.filter(
            key=self.key_for_options, user=request.user).first()
        if user_options:
            options_dict = QueryDict(user_options.options)
        else:
            options_dict = request.GET
        return options_dict

    def get_filterset(self, queryset, request):

        def get_filters_dict(request):
            if 'reset' in request.GET:
                filters_dict = None
                return filters_dict
            if 'filters' in request.GET:
                filters_dict = request.GET
                return filters_dict
            if 'filters' or 'reset' not in request.GET:
                filters_dict = self.get_user_options(request)
                return filters_dict

        self.filterset = self.filterset_class(
            get_filters_dict(request), queryset=queryset, request=request)
        return self.filterset

    def post(self, request, *args, **kwargs):
        if 'filters_form' in request.POST:
            self.save_user_options(request)
        return JsonResponse({"answer": 'Filters have been saved'}, status=200)