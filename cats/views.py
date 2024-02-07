from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.throttling import AnonRateThrottle,ScopedRateThrottle

from .models import Achievement, Cat, User
from .pagination import CatsPagination
from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .throttling import WorkingHoursRateThrottle



class CatViewSet(viewsets.ModelViewSet):

    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (WorkingHoursRateThrottle,ScopedRateThrottle)
    # throttle_classes = (AnonRateThrottle,)  # Подключили класс AnonRateThrottle 
    # throttle_scope = 'low_request'
    # Вот он наш собственный класс пагинации с page_size=20
     # Временно отключим пагинацию на уровне вьюсета, 
    # так будет удобнее настраивать фильтрацию
    # pagination_class = CatsPagination

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filterset_fields = ('color', 'birth_year')
    # search_fields = ('name',)
    #  Доступные для поиска поля связанной модели указываются через нотацию с двойным подчёркиванием: ForeignKey текущей модели__имя поля в связанной модели.
    search_fields = ('achievements__name', 'owner__username') 
    # при GET-запросе вида /cats/?ordering=name — применится сортировка выдачи по именам котиков в алфавитном порядке.
    ordering_fields = ('name', 'birth_year') 
    # в результатах выдачи будет применяться сортировка по умолчанию, дополнительные параметры при запросе не нужны:
    ordering = ('name',) 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

    def get_permissions(self):
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
        # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer