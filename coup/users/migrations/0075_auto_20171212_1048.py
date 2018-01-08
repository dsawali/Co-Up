# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-12 18:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0074_auto_20171204_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='program',
            field=models.CharField(blank=True, choices=[('Anthropology', 'Anthropology'), ('Asia-Canada', 'Asia-Canada'), ('Cognitive Science', 'Cognitive Science'), ('Criminology', 'Criminology'), ('Economics', 'Economics'), ('English', 'English'), ('First Nations Studies', 'First Nations Studies'), ('French Cohort', 'French Cohort'), ('French', 'French'), ("Gender, Sexuality, and Women's Studies", "Gender, Sexuality, and Women's Studies"), ('Gerontology', 'Gerontology'), ('Graduate Liberal Studies', 'Graduate Liberal Studies'), ('Hellenic Studies', 'Hellenic Studies'), ('History', 'History'), ('Humanities', 'Humanities'), ('International Studies', 'International Studies'), ('Labour Studies', 'Labour Studies'), ('Language Training', 'Language Training'), ('Latin American Studies', 'Latin American Studies'), ('Linguistics', 'Linguistics'), ('Philosophy', 'Philosophy'), ('Political Science', 'Political Science'), ('Psychology', 'Psychology'), ('Public Policy', 'Public Policy'), ('Sociology', 'Sociology'), ('Urban Studies', 'Urban Studies'), ('World Literature', 'World Literature'), ('Communication', 'Communication'), ('Contemporary Arts', 'Contemporary Arts'), ('Interactive Arts and Technology', 'Interactive Arts and Technology'), ('Publishing', 'Publishing'), ('Archaeology', 'Archaeology'), ('Sustainable Community Development', 'Sustainable Community Development'), ('Environmental Science', 'Environmental Science'), ('Geography', 'Geography'), ('Resource and Environmental Management', 'Resource and Environmental Management'), ('Environment', 'Environment'), ('Heritage Resource Management', 'Heritage Resource Management'), ('Resource and Environmental Planning', 'Resource and Environmental Planning'), ('Computing Science', 'Computing Science'), ('Engineering Science', 'Engineering Science'), ('Mechatronic Systems Engineering', 'Mechatronic Systems Engineering'), ('Actuarial Science and Statistics', 'Actuarial Science and Statistics'), ('Biological Sciences', 'Biological Sciences'), ('Biomedical Physiology and Kinesiology', 'Biomedical Physiology and Kinesiology'), ('Chemistry', 'Chemistry'), ('Earth Sciences', 'Earth Sciences'), ('Mathematics', 'Mathematics'), ('Molecular Biology and Biochemistry', 'Molecular Biology and Biochemistry'), ('Physics', 'Physics'), ('Statistics and Actuarial Science', 'Statistics and Actuarial Science')], max_length=30),
        ),
    ]
