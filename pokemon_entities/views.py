import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    local_time = localtime()
    pokemon_entity = PokemonEntity.objects.filter(appeared_at__lte=local_time,
                                                  disappeared_at__gte=local_time)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity in pokemon_entity:
        add_pokemon(folium_map,
                    entity.lat,
                    entity.lon,
                    request.build_absolute_uri(entity.pokemon.image.url)
                    )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        if pokemon.image:
            img_url = request.build_absolute_uri(pokemon.image.url)
        else:
            img_url = DEFAULT_IMAGE_URL
        pokemons_on_page.append({
            'pokemon_id': pokemon.pk,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    pokemons_evolution_from = {}
    pokemons_evolution_to = {}

    if pokemon.previous_evolution:
        pokemons_evolution_from = {
            'pokemon_id': pokemon.previous_evolution.pk,
            'img_url': request.build_absolute_uri(pokemon.previous_evolution.image.url),
            'title_ru': pokemon.previous_evolution.title,
        }

    if pokemon.next_evolutions.all():
        pokemon_evolution = pokemon.next_evolutions.first()
        pokemons_evolution_to = {
            'pokemon_id': pokemon_evolution.pk,
            'img_url': pokemon_evolution.image.url,
            'title_ru': pokemon_evolution.title,
        }

    img_url = request.build_absolute_uri(pokemon.image.url)
    pokemons_info = {
        'pokemon_id': pokemon.pk,
        'img_url': img_url,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': pokemons_evolution_from,
        'next_evolution': pokemons_evolution_to
    }

    requested_pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
         )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons_info
    })
