from django.utils.deprecation import MiddlewareMixin
# from .models import UserOperationRecordModel


# class UserOperationRecordMiddleware(MiddlewareMixin):
#
#     def process_request(self, request):
#         ip_addr = request.META.get("REMOTE_ADDR")
#         method = request.META.get("REQUEST_METHOD")
#         api_path = request.META.get("PATH_INFO")
#         username = request.user
#         if method == "GET":
#             parameters = request.GET.dict()
#         else:
#             # print(request.body)
#             try:
#                 parameters = eval(request.body.decode("utf-8"))
#             except Exception as e:
#                 parameters = ""
#         record_data = {
#             "ip_addr": ip_addr,
#             "methodtype": method,
#             "api_path": api_path,
#             "username": username,
#             "parameters": parameters
#         }
#         UserOperationRecordModel.objects.create(**record_data)


class NotUseCsrfTokenMiddlewareMixin(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
