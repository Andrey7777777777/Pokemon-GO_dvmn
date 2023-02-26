from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    title_en = models.CharField(max_length=50, blank=True, verbose_name='Название на английском')
    title_jp = models.CharField(max_length=50, blank=True, verbose_name='Название на японском')
    evaluation_from = models.ForeignKey('self', null=True,
                                        on_delete=models.SET_NULL,
                                        blank=True,
                                        related_name='evolutions', verbose_name='Эвалюция')
    image = models.ImageField(null=True, blank=True, verbose_name='Картинка')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(null=True, verbose_name='Время появления')
    disappeared_at = models.DateTimeField(null=True, verbose_name='Время исчезновения')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень покемона')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье покемона')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила покемона')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита покемона')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость покемона')



