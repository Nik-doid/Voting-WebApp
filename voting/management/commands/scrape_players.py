import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from voting.models import Player

class Command(BaseCommand):
    help = 'Scrape player data and save it to the database'

    def handle(self, *args, **kwargs):
        url = 'https://www.vlr.gg/player/26171/demon1'
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            
            player_name = soup.find('h1', class_='wf-title').text.strip()
            real_name = soup.find('h2', class_='player-real-name ge-text-light').text.strip()
            photo_tag = soup.find('img', alt=player_name)
            photo_url = 'https:' + photo_tag['src'] if photo_tag else None

          
            player, created = Player.objects.get_or_create(
                name=player_name,
                defaults={
                    'real_name': real_name,
                    'photo_url': photo_url
                }
            )
            if created:
                self.stdout.write(f"Added player: {player_name}")
            else:
                self.stdout.write(f"Player already exists: {player_name}")
        else:
            self.stdout.write(f"Failed to fetch data. Status code: {response.status_code}")
