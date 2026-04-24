from django.core.management.base import BaseCommand
from course.models import Skill, DifficultyLevel, Language, OfferedBy, Industry, Tier, Course
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    
    help = 'Set up initial data for the Course app'

    def handle(self, *args, **kwargs):
        # Create initial Skills
        skills = ['Python', 'Data Analysis', 'Machine Learning', 'Web Development']
        for skill in skills:
            Skill.objects.get_or_create(name=skill)

        # Create initial Difficulty Levels
        levels = ['Beginner', 'Intermediate', 'Advanced']
        for level in levels:
            DifficultyLevel.objects.get_or_create(level=level)

        # Create initial Languages
        languages = [('English', 'en'), ('Spanish', 'es'), ('French', 'fr'), ('Hindi', 'hi')]
        for name, code in languages:
            Language.objects.get_or_create(name=name, code=code)

        # Create initial Offered By entries
        organizations = [
            ('CertiChain', 'https://certichain.io')
        ]
        
        for org_name, website in organizations:
            OfferedBy.objects.get_or_create(organization_name=org_name, website=website,description=fake.paragraph(nb_sentences=100))

        # Create initial Industries
        industries = ['Information Technology', 'Finance', 'Healthcare', 'Education']
        for industry in industries:
            Industry.objects.get_or_create(name=industry)

        # Create initial Tiers
        tiers = ['Free', 'Basic', 'Premium']
        for tier in tiers:
            Tier.objects.get_or_create(name=tier)

        self.stdout.write(self.style.SUCCESS('Successfully set up initial data for the Course app'))
