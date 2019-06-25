# from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from django.conf.urls import include, url


urlpatterns = [
    url(r'list/$', TemplateView.as_view(template='FiveG-NL_Archives-Home.html')),
    url(r'april-08/$', TemplateView.as_view(template='FiveG-NL_April08.html')),
    url(r'july-08/$', TemplateView.as_view(template='FiveG-NL_July08.html')),
    url(r'march-09/$', TemplateView.as_view(template='FiveG-NL_March09.html')),
    url(r'june-09/$', TemplateView.as_view(template='June09.html')),
    url(r'april-08/warm-up-from-the-editor/$', TemplateView.as_view(template='Warm up from the Editor-April08.html')),
    url(r'april-08/from-the-ceos-desk/$', TemplateView.as_view(template='From the CEOs Desk-April08.html')),
    url(r'april-08/gift-of-the-gurus/$', TemplateView.as_view(template='Gift of the Gurus-April08.html')),
    url(r'april-08/product-development/$', TemplateView.as_view(template='Product Development-April08.html')),
    url(r'april-08/between-the-cubicles/$', TemplateView.as_view(template='Between the cubicles-April08.html')),
    url(r'april-08/sports/$', TemplateView.as_view(template='Sports-April08.html')),
    url(r'april-08/survey-of-the-month/$', TemplateView.as_view(template='Survey of the month-April08.html')),
    url(r'april-08/mystifier/$', TemplateView.as_view(template='Mystifier-April08.html')),
    url(r'april-08/jocularity/$', TemplateView.as_view(template='Jocularity-April08.html')),
    url(r'april-08/logo-race/$', TemplateView.as_view(template='Logo Race-April08.html')),

    url(r'july-08/warm-up-from-the-editor/$', TemplateView.as_view(template='Warmup from the Editor-july08.html')),
    url(r'july-08/the-focus-on-completing-things/$', TemplateView.as_view(template='The focus on completing things-july08.html')),
    url(r'july-08/the-sub-prime-crisis/$', TemplateView.as_view(template='The Sub Prime Crisis-july08.html')),
    url(r'july-08/ipl-frenzy/$', TemplateView.as_view(template='IPL Frenzy-july08.html')),
    url(r'july-08/mystifier/$', TemplateView.as_view(template='Mystifier-july08.html')),
    url(r'july-08/valparai-2013the-tea-trail/$', TemplateView.as_view(template='Valparai The tea trail-july08.html')),
    url(r'july-08/the-first-step-2/$', TemplateView.as_view(template='The First step-july08.html')),

    url(r'march-09/from-the-editors-desk/$', TemplateView.as_view(template='From the Editors Desk-March-09.html')),
    url(r'march-09/pride-rigour-and-discipline-in-software-development/$', TemplateView.as_view(template='Pride, Rigour and Discipline in Software Development-March-09.html')),
    url(r'march-09/in-the-lighter-vein/$', TemplateView.as_view(template='Jest for you-March-09.html')),
    url(r'march-09/the-financial-201cmaya201d/$', TemplateView.as_view(template='The Financial Maya-March-09.html')),
    url(r'march-09/trip-to-a-place-of-solace-and-comfort/$', TemplateView.as_view(template='Trip to a place of solace and comfort-March-09.html')),
    url(r'march-09/happenings-of-5g-family-since-the-july-2008-issue/$', TemplateView.as_view(template='Happenings of 5G family-March-09.html')),
    url(r'march-09/puzzle/$', TemplateView.as_view(template='Puzzle-March-09.html')),
    url(r'march-09/answer-to-the-5g-nl-puzzle/$', TemplateView.as_view(template='Answer to the 5G-NL Puzzle-March-09.html')),
    url(r'march-09/puzzleGoforit/$', TemplateView.as_view(template='Go for it-March-09.html')),
    url(r'march-09/the-speed-breaker/$', TemplateView.as_view(template='Reasoning and Discovering-March-09.html')),
]
