# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from musicdb.utils.http import render_playlist
from musicdb.classical.models import Artist, Work, Recording, Ensemble, \
    Category

def categories(request):
    return render(request, 'classical/categories.html', {
        'categories': Category.get_root_nodes(),
    })

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    return render(request, 'classical/category.html', {
        'category': category,
    })

def composers(request):
    return render(request, 'classical/composers.html', {
        'composers': Artist.objects.composers(),
    })

def ensembles(request):
    return render(request, 'classical/ensembles.html', {
        'ensembles': Ensemble.objects.all(),
    })

def artists(request):
    return render(request, 'classical/artists.html', {
        'artists': Artist.objects.artists(),
    })

def artist(request, slug):
    artist = get_object_or_404(Artist, slug=slug)

    works = artist.works.select_related('key').prefetch_related(
        'catalogues__catalogue',
    )

    return render(request, 'classical/artist.html', {
        'works': works,
        'artist': artist,
    })

def ensemble(request, slug):
    return render(request, 'classical/ensemble.html', {
        'ensemble': get_object_or_404(Ensemble, slug=slug),
    })

def work(request, artist_slug, slug):
    work = get_object_or_404(Work, slug=slug, composer__slug=artist_slug)

    recordings = work.recordings.select_related('work').prefetch_related(
        'movements__music_file',
        'performances__artistperformance',
        'performances__ensembleperformance',
    )

    return render(request, 'classical/work.html', {
        'work': work,
        'recordings': recordings,
    })

def play_recording(request, recording_id):
    recording = get_object_or_404(Recording, pk=recording_id)

    return render_playlist(request, recording.get_tracks())

##

def recent(request):
    recent = Recording.objects.recent().select_related(
        'work__key',
        'work__composer',
    ).prefetch_related(
        'performances',
        'performances__artistperformance__artist',
        'performances__ensembleperformance__ensemble',
        'work__catalogues__catalogue',
    )[:20]

    return render(request, 'classical/recent.html', {
        'recent': recent,
    })
