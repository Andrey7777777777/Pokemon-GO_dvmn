# Generated by Django 3.1.14 on 2023-02-28 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0008_auto_20230226_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='evaluation_from',
        ),
        migrations.AddField(
            model_name='pokemon',
            name='previous_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_evolution', to='pokemon_entities.pokemon', verbose_name='Эвалюция'),
        ),
    ]
