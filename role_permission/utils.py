from functools import reduce
from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'size'
    page_query_param = 'page'


def get_object(obj, id):
    try:
        obj_1 = obj.objects.get(id=id)
        return obj_1
    # ObjectDoesNotExist时表示get没有获取内容
    except Exception as e:
        print(str(e))
        return ""


def dict_make(dict2, item):
    k,v = item
    if k == "page" or k == "size":
        pass
    else:
        if v:
            dict2[k + "__icontains"] = v
        else:
            pass
    return dict2
# parms_query_dict1 = reduce(dict_make, list(parms_query_dict.keys()), {})
