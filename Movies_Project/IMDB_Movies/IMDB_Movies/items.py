# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbMoviesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_name = scrapy.Field()
    movie_release_year = scrapy.Field()
    movie_url = scrapy.Field()
    movie_imdb_rating = scrapy.Field()
    movie_genre = scrapy.Field()
    movie_duration_minute = scrapy.Field()
    movie_directors = scrapy.Field()
    movie_stars = scrapy.Field()
    movie_directors_link = scrapy.Field()
    movie_stars_link = scrapy.Field()
    movie_votes = scrapy.Field()
    movie_gross_millions_of_dollars = scrapy.Field()
    movie_production_status = scrapy.Field()
    