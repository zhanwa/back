"""分页模块"""

from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination
# 1.看第n页,每页看多少条数据
class MyPage(PageNumberPagination):
    # 每页默认显示多少条
    page_size = 2
    # 每页最多显示多少条
    max_page_size =10
    # 可以带size参数来确定每页看多少条 size=10
    page_size_query_param = "size"
    # 通过page看多少也
    page_query_param="page"

# 2 从第几条数据开始向后看多少条
class LimitPage(LimitOffsetPagination):
    default_limit = 2
    # limit = n 从索引处向后显示n条
    limit_query_param = 'limit'
    # offset索引,从0开始 表示当前你的位置
    offset_query_param = 'offset'
    # 最多显示5条
    max_limit = 5
# 加密分页,只用上一页,下一页
class CursorPage(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 2
    # 使用id排序 正序  -id表示反序
    ordering = 'id'
    page_size_query_param =5