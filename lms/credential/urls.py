from django.urls import path
from .views import certificate, certificates, badges, badge, nft_mint, nft_verify

urlpatterns = [
    path('certificates/', certificates, name='certificates'),
    path('certificate/<str:uid>/', certificate, name='certificate'),
    path('badges/', badges, name='badges'),
    path('badge/<str:uid>/', badge, name='badge'),
    # NFT Blockchain Certificate Routes
    path('nft/mint/', nft_mint, name='nft_mint'),
    path('nft/verify/', nft_verify, name='nft_verify'),
]           

