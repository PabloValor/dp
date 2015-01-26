# -*- encoding: utf-8 -*-
import csv
import datetime
from django.core.management.base import BaseCommand, CommandError
from tournaments.models import Tournament, Match, Fixture, Team

class Command(BaseCommand):
    # ./manage.py load_tournament 'Torneo Primera Division 2015' 15 ../scrapers/torneo/2015_argentina_primera_division.csv 
    args = '<tournamentName numberMatchesPerFixture csvPath>'
    help = 'Loads a new Tournamnet'

    def handle(self, *args, **options):
        tournament_name = args[0]
        number_match_per_fixture = args[1]
        csv_path = args[2]

        tournament = Tournament.objects.create(name = tournament_name)

        fixture_number = 0        
        match_counter = 0

        with open(csv_path, 'r') as csvfile:
            match_reader = csv.reader(csvfile, delimiter=',')
            for match in match_reader:
                match_date = datetime.datetime.strptime(match[0], "%d-%m-%Y").date()
                
                if match_counter % int(number_match_per_fixture) == 0:
                    fixture_number += 1
                    match_counter = 0
                    fixture = Fixture.objects.create(number = fixture_number, tournament = tournament, open_until = match_date)
                    self.stdout.write("Fixture {0}\n".format(fixture_number))
                    
                    
                local_name = match[1].strip()
                visitor_name = match[2].strip()

                Match.objects.create(local_team = Team.objects.get(name = local_name),
                                     visitor_team = Team.objects.get(name = visitor_name),
                                     date = match_date,
                                     fixture = fixture)

                match_counter += 1

                
