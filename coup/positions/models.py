import datetime
import math

from django.db import models
from django.conf import settings
from django.urls import reverse

from coup.core.models import TimeStampedModel
from coup.users.models import User


class PositionManager(models.Manager):
    """
    Custom model manager extending over django's
    default model manager.
    """
    use_for_related_fields = True
    
    DEFAULT_INPUT = ''

    def query_on_params(self,\
                        **kwargs):
        """
        Method called by search view to filter on:
            - title
            - company
            - start/end year/month
        """
        # check for empty query
        if self.check_empty_query(**kwargs):
            return []

        return self.filter_positions(**kwargs)

    def quick_query(self,\
                    value):
        """
        Handles quick queries based on
        a single value.
        """
        # first filter on required fields
        return self.all().filter(\
            company__icontains = value)


    def filter_positions(self,\
                         **kwargs):
        """
        Handles direct queries on:
            - company
            - title
            - start/end year
            - start/end month
            - location within km radius 
        """
        # search filters
        company_s = kwargs['company'][0]
        title_s = kwargs['title'][0]
        start_year = kwargs['start_year'][0]
        start_month = kwargs['start_month'][0]
        end_year = kwargs['end_year'][0]
        end_month = kwargs['end_month'][0]
        location_lat = kwargs['location_lat'][0]
        location_lng = kwargs['location_lng'][0]

        # start with all objects
        query_set = self.all()
        # first filter on required fields
        if company_s == '' and title_s == '':
            pass
        elif title_s == '':
            query_set = query_set.filter(\
                company__icontains = company_s)
        elif company_s == '':
            query_set = query_set.filter(\
                title__icontains = title_s)
        else:
            query_set = query_set.filter(\
                company__icontains = company_s,\
                title__icontains = title_s)

        # second filter on date fields
        if start_year != self.DEFAULT_INPUT:
            query_set = query_set.filter(\
                start_year__gte = start_year)
        if end_year != self.DEFAULT_INPUT:
            query_set = query_set.filter(\
                end_year__lte = end_year)
        if start_month != self.DEFAULT_INPUT:
            query_set = query_set.filter(\
                start_month__gte = start_month)
        if end_month != self.DEFAULT_INPUT:
            query_set = query_set.filter(\
                end_month__lte = end_month)

        # filter on location 
        if location_lat != self.DEFAULT_INPUT and\
           location_lng != self.DEFAULT_INPUT:
            query_set = self.get_nearby_positions(\
                query_set,\
                float(location_lat),\
                float(location_lng))
  
        return query_set

    def get_nearby_positions(self,\
                             query_set,\
                             curr_lat,\
                             curr_lng):
        """
        Returns all positions in the query set
        within a 10km box of the given 
        latitude/longitude coordinate.
        """
        distance = 10.0
        earth_radius = 6371.0;

        delta_lat = math.degrees(distance/earth_radius)
        max_lat = curr_lat + delta_lat
        min_lat = curr_lat - delta_lat

        radius_at_lng = earth_radius*math.cos(math.radians(curr_lat))
        delta_lng = math.degrees(distance/radius_at_lng)
        max_lng = curr_lng + delta_lat
        min_lng = curr_lng - delta_lat

        return query_set.filter(location_lat__gte = min_lat,\
            location_lat__lte = max_lat,\
            location_lng__gte = min_lng,\
            location_lng__lte = max_lng)
         
        
    def check_empty_query(self,\
                          **kwargs):
        """
        Returns True if passed query parameters
        are empty, False otherwise.
        """
        for value in kwargs.values():
            if value[0] != self.DEFAULT_INPUT:
                return False
        return True


class Position(models.Model):
    """
    Stores details about a specific co-op position.
    Shares a many-to-many relationship with the User model.
    TODO: GLASSDOOR API INTEGRATION FOR INTERVIEW QUESTIONS
    """
    # add custom manager
    objects = PositionManager()

    # choices for year
    YEAR_CHOICES = []
    for r in range(2000, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((str(r),str(r)))

    # choices for month
    MONTH_CHOICES = []
    for i in range(1,13):
        month_s = datetime.date(i,i,i).strftime('%B')
        MONTH_CHOICES.append((month_s, month_s))

    # company name and job title
    company = models.CharField(max_length = 30)
    title = models.CharField(max_length = 30)

    # start year/month
    start_year = models.CharField(choices = YEAR_CHOICES,\
        max_length = 4,\
        default = YEAR_CHOICES[0][0])
    start_month = models.CharField(max_length = 9,\
        choices = MONTH_CHOICES,\
        default = MONTH_CHOICES[0][0])

    # end year/month
    end_year = models.CharField(choices = YEAR_CHOICES,\
        max_length = 4,\
        null = True,\
        blank = True)
    end_month = models.CharField(max_length = 9,\
        choices = MONTH_CHOICES,\
        null = True,\
        blank = True) 

    # location in terms of lat/lng coordinates
    location_lat = models.FloatField(max_length = 20,\
        null = True,\
        blank = True)
    location_lng = models.FloatField(max_length = 20,\
        null = True,\
        blank = True)    

    # location in terms of human readable address
    location_addr = models.CharField(max_length = 100,\
        null = True,\
        blank = True)

    # user who owns the position
    user = models.ForeignKey(User,\
        on_delete = models.CASCADE,\
        null = True)

    # slug for readable urls
    slug = models.SlugField()

    def __str__(self):
        return "%s %s" % (self.company, self.title)

    # Returns the url to access a particular position
    def get_absolute_url(self):
        return reverse('positions:position-detail', \
            kwargs={\
                'pk' : self.id, \
                'slug' : str(self.slug)
            }
        )

    def generate_slug(self):
        """
        Sets slug for position url
        as username-title-company.
        """ 
        new_slug = '{}-{}'.format(\
            '-'.join(self.title.lower().split(' ')),\
            '-'.join(self.company.lower().split(' ')))

        self.slug = new_slug
        return new_slug


class CommentManager(models.Manager):
    """
    Custom manager for Comment extending
    over django's default manager.
    """
    use_for_related_fields = True
    
    def query_on_position(self,\
                          positions_l):
        """
        Queries for users related to positions
        in positions_l.
        """
        users_l = []
        for _p in positions_l:
            related_l = self.filter(position = _p)
            for _r in related_l:
                users_l.append(_r.user)
        return users_l
    
    def query_on_user(self,\
                      users_l):
        """
        Queries for positions related to users
        in users_l.
        """
        positions_l = []
        for _u in users_l:
            related_l = self.filter(user = _u)
            for _r in related_l:
                positions_l.append(_r.position)
        return positions_l
    

class Comment(TimeStampedModel):
    """
    Model to store specific user comments about
    specific positions.
    Shares a foreign key relationship with:
        - User
    """
    # custom manager
    objects = CommentManager()

    comment = models.TextField(max_length=200,\
        null = True,\
        blank = True)
    position = models.ForeignKey(Position,\
        on_delete = models.CASCADE, \
        null = True)
    user = models.ForeignKey(User,\
        on_delete = models.CASCADE, \
        null = True)

    def __str__(self):
        return ' '.join([
            'comment',
            str(self.id),
        ])
