import scrapy
import requests
from ..items import ImdbMoviesItem

class MoviespiderSpider(scrapy.Spider):
    name = 'MovieSpider'
    allowed_domains = ['www.imdb.com']
    start_urls = [
        'https://www.imdb.com/search/title/?genres=action&title_type=movie',
        'https://www.imdb.com/search/title/?genres=adventure&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Drama&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Comedy&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Fantasy&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Family&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Romance&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Sci-Fi&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Thriller&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Animation&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Crime&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Mystery&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Horror&title_type=movie',
        'https://www.imdb.com/search/title/?genres=History&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Western&title_type=movie',
        'https://www.imdb.com/search/title/?genres=War&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Musical&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Music&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Biography&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Sport&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Film-Noir&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Reality-TV&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Game-Show&title_type=movie',
        'https://www.imdb.com/search/title/?genres=News&title_type=movie',
        'https://www.imdb.com/search/title/?genres=Talk-Show&title_type=movie'
    ]
    
    def __init__(self):
        self.items = ImdbMoviesItem()

    def parse(self, response):
        records = response.css('.mode-advanced')
        movie_names = []
        movie_release_year = []
        movie_urls = []
        movie_imdb_rating = []
        movie_genre = []
        movie_duration = []
        movie_directors = []
        movie_stars = []
        movie_directors_link = []
        movie_stars_link = []
        movie_votes = []
        movie_gross = []
        movie_production_status = []
        for record in records:
            movie_names.append(record.css('.lister-item-header a::text').get())
            movie_release_year.append(record.css('.text-muted.unbold::text').get())
            movie_urls.append(record.css('.lister-item-header a::attr(href)').get())
            movie_imdb_rating.append(record.css('strong::text').get())
            movie_genre.append(record.css('.genre::text').get())
            movie_duration.append(record.css('.runtime::text').get())
            
            director_and_stars = record.css('.text-muted~ .text-muted+ p ::text').getall()
            director_and_stars = [d.strip() for d in director_and_stars if d.strip() != '']
            director_and_stars = [d for d in director_and_stars if d != ',']
            director_and_stars = [d for d in director_and_stars if d != '|']
            print("LIST : ", end="\t")
            print(director_and_stars)
            
            try:
                index_of_stars = director_and_stars.index('Stars:')
            except Exception:
                try:
                    index_of_stars = director_and_stars.index('Star:')
                except Exception:
                    index_of_stars = -1
            
            if index_of_stars == 0:
                movie_directors.append([])
                movie_stars.append(director_and_stars[index_of_stars+1:])
            elif index_of_stars == -1:
                movie_directors.append(director_and_stars[1:])
                movie_stars.append([])
            else:
                movie_directors.append(director_and_stars[1:index_of_stars])
                movie_stars.append(director_and_stars[index_of_stars+1:])
            
            all_links = record.css('.text-muted~ .text-muted+ p a ::attr(href)').getall()
            all_links = ["http://www.imdb.com" + link for link in all_links]
            movie_directors_link.append(all_links[0:len(movie_directors[len(movie_directors)-1])])
            movie_stars_link.append(all_links[len(movie_directors[len(movie_directors)-1]):])
            
            movie_votes.append(record.css('.sort-num_votes-visible span:nth-child(2)::text').get())
            movie_gross.append(record.css('.ghost~ .text-muted+ span::text').get())
            movie_production_status.append(record.css('b::text').get())
            # movie_director.append(record.css('.text-muted~ .text-muted+ p ::text').getall())
            # movie_stars.append(record.css('.lister-item-content .ghost~ a ::attr(href)').get())
        # print("Movie Names :" + str(len(movie_names)))
        # print("Movie Release Year :" + str(len(movie_release_year)))
        # print("Movie URLs :" + str(len(movie_urls)))
        # print("Movie IMDB Rating :" + str(len(movie_imdb_rating)))
        # print("Movie Genre : " + str(len(movie_genre)))
        # print("Movie Duration : " + str(len(movie_genre)))
        # print("Movie Directors : " + str(len(movie_directors)))
        # print("Movie Stars : " + str(len(movie_stars)))
        # print("Movie Directors Link : " + str(len(movie_directors_link)))
        # print("Movie Stars Link : " + str(len(movie_stars_link)))
        # print("Movie Votes : " + str(len(movie_votes)))
        # print("Movie Gross : " + str(len(movie_gross)))
        # print("Movie Production Status : " + str(len(movie_production_status)))
        for i in range(len(movie_urls)):
            movie_urls[i] = 'http://www.imdb.com' + movie_urls[i]
            movie_genre[i] = movie_genre[i].split(',')
            for j in range(len(movie_genre[i])):
                movie_genre[i][j] = movie_genre[i][j].strip()
            self.items['movie_name'] = movie_names[i]
            self.items['movie_release_year'] = movie_release_year[i]
            self.items['movie_url'] = movie_urls[i]
            self.items['movie_imdb_rating'] = movie_imdb_rating[i]
            self.items['movie_genre'] = movie_genre[i]
            self.items['movie_duration_minute'] = movie_duration[i]
            self.items['movie_directors'] = movie_directors[i]
            self.items['movie_stars'] = movie_stars[i]
            self.items['movie_directors_link'] = movie_directors_link[i]
            self.items['movie_stars_link'] = movie_stars_link[i]
            self.items['movie_votes'] = movie_votes[i]
            self.items['movie_gross_millions_of_dollars'] = movie_gross[i]
            self.items['movie_production_status'] = movie_production_status[i]
            yield self.items
            
        next_page_link = response.css('.nav .next-page::attr(href)').get()
        next_page_link = 'http://www.imdb.com' + next_page_link
        if scrapy.Request(next_page_link) is not None:
            yield scrapy.Request(next_page_link, callback=self.parse)