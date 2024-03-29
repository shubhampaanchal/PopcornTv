#### Required ####
from builtins import Exception
import json
import pytz
import sys
import requests
from datetime import datetime,timedelta


#### Thread ####
from threading import *
from time import *


#### Django ####
from django.conf import settings
from django import template
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect


#### Rest Framework ####
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


#### Model ####
from .models import movieInformation


#### Error Code ####
from .APIStatus import *


#### AES ENCRYPTION ####
# from .AES256 import Cipher_AES


# #### CERTIFICATE ENCRYPTION ####
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_v1_5
# from base64 import b64decode
# from Cryptodome.Cipher import PKCS1_OAEP
# from Cryptodome.Hash import SHA256, SHA1
# from Cryptodome.Signature import pss


#### VALIDATIONS ####
from .ValidatorRex import ValidationClass


#### Loggers ####
import logging
logger=logging.getLogger('dashboardLogs')


#### ldap ####
from core.settings import API_KEY



#### LDAP CONNECTION ESTABLISHED SECTION START ####
# if LDAP_STATUS:

#     logger.info(ldapSuccess.get('message'))

# else:

#     logger.info(ldapError.get('message'))
#     logger.error(LDAP_ERR)
#### LDAP CONNECTION ESTABLISHED SECTION END ####



# #### SESSION KEY EXPIRE SECTION START ####
# class sessionKeyExpire(Thread):

#     def run(self):

#         try:
#             while True:

#                 sessionKeyDB = sessionKey.objects.filter(modifiedOn__lte = ((datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))- timedelta(days=1)))
#                 sessionKeyDB.delete()
#                 sleep(3600)

#         except Exception as err:
#             logger.error(err)
        
# """Uncomment Section if you want to Delete 24 hour old Session Key""" 
# if 'runserver' in sys.argv:
#     try:

#         threadObj = sessionKeyExpire()
#         threadObj.start()

#     except Exception as err:
#         pass
# #### SESSION KEY EXPIRE SECTION END ####



# #### AES ENCRYPTION DECRYPTION SECTION START ####
# def encryptionRex(sessionKey, encryptData):
#     return(Cipher_AES(sessionKey, "fedcba9876543210").encrypt(encryptData, "MODE_CBC", "PKCS5Padding", "base64"))

# def decryptionRex(sessionKey, decryptData):
#     return(Cipher_AES(sessionKey, "fedcba9876543210").decrypt(decryptData, "MODE_CBC", "PKCS5Padding", "base64"))
# #### AES ENCRYPTION DECRYPTION SECTION END ####



# #### CRT DECRYPTION SECTION START ####
# def decryptCrtRex(dataEncrypt):

#     privateKey= (open('certificates/apc_prvt_rsakey.pem', 'rb').read())
#     obj_private = RSA.importKey(privateKey)
#     decode_cipher = b64decode(dataEncrypt)

#     cipher = PKCS1_OAEP.new(key=obj_private, hashAlgo=SHA256, mgfunc=lambda x,y: pss.MGF1(x,y, SHA1))
#     ciphertext = cipher.decrypt(decode_cipher)

#     return(ciphertext.decode('utf-8'))
# #### CRT DECRYPTION SECTION END ####



# #### SERVER FIND SECTION START ####
# def serverFinder(macAddress):
#     roomConfigDB  = roomConfig.objects.values()

#     for item in roomConfigDB:

#         list_convert = json.loads(item.get('config').replace("'", '"'))
#         find_mac = (list(filter(lambda mc_addr: mc_addr['macAddress'] == macAddress, list_convert)))

#         if len(find_mac)!=0:

#             return item.get('macAddress')

#     return None
# #### SERVER FIND SECTION END ####




#### Dashboard setContent Section Start ####
def setContent(request, query):
    
    try:
        url = f"https://api.themoviedb.org/3/search/movie?query={query}&api_key={API_KEY}"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(response.text)
        
        movieName = response.get('results')[0].get('original_title')
        genreId = response.get('results')[0].get('genre_ids')
        movieType = ' | '.join(movieTypeDB[str(item)] for item in response.get('results')[0].get('genre_ids'))
        movieId = response.get('results')[0].get('id')
        overview = response.get('results')[0].get('overview')
        releaseDate = response.get('results')[0].get('release_date')
        language = response.get('results')[0].get('original_language')
        popularity = response.get('results')[0].get('popularity')
        voteAverage = response.get('results')[0].get('vote_average')
        voteCount = response.get('results')[0].get('vote_count')
        downloadPoster = "".join(["https://image.tmdb.org/t/p/w500", response.get('results')[0].get('poster_path')])
        downloadBackdrop = "".join(["https://image.tmdb.org/t/p/original", response.get('results')[0].get('backdrop_path')])
        
        r = requests.get(downloadPoster)
        with open(f"/home/guest/Desktop/server/popcorntv/apps/static/images/Poster/{response.get('results')[0].get('poster_path')}",'wb') as f:
            f.write(r.content)
        posterPath = f"/static/images/Poster/{response.get('results')[0].get('poster_path')}"
        
        r = requests.get(downloadBackdrop) 
        with open(f"/home/guest/Desktop/server/popcorntv/apps/static/images/Backdrop/{response.get('results')[0].get('backdrop_path')}",'wb') as f:
            f.write(r.content)
        backdropPath = f"/static/images/Backdrop/{response.get('results')[0].get('backdrop_path')}"
        
        try:
            if movieInformation.objects.filter(Q(movieId = movieId) | Q(movieName = movieName)).exists():
                
                try:
                    ### Update ###
                    movieInformationDB = movieInformation.objects.filter(Q(movieId = movieId) | Q(movieName = movieName))
                    modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                    movieInformationDB.update(
                                            movieName = movieName,
                                            genreId = genreId,
                                            movieType = movieType,
                                            movieId = movieId,
                                            overview = overview,
                                            releaseDate = releaseDate,
                                            language = language,
                                            popularity = popularity,
                                            voteAverage = voteAverage,
                                            voteCount = voteCount,
                                            posterPath = posterPath,
                                            backdropPath = backdropPath,
                                            watchCount = None,
                                            watchTime = None,
                                            teaser = None,
                                            movieURL = None,
                                            favourite = None,
                                            user = request.user,
                                            modifiedOn = modifiedOn,
                                        )
                    
                except Exception as err:
                    print(err)

            else:
                try:
                    ### Save ###
                    movieInformationDB = movieInformation()
                    movieInformationDB.movieName = movieName
                    movieInformationDB.genreId = genreId
                    movieInformationDB.movieType = movieType
                    movieInformationDB.movieId = movieId
                    movieInformationDB.overview = overview
                    movieInformationDB.releaseDate = releaseDate
                    movieInformationDB.language = language
                    movieInformationDB.popularity = popularity
                    movieInformationDB.voteAverage = voteAverage
                    movieInformationDB.voteCount = voteCount
                    movieInformationDB.posterPath = posterPath
                    movieInformationDB.backdropPath = backdropPath
                    movieInformationDB.watchCount = None,
                    movieInformationDB.watchTime = None,
                    movieInformationDB.teaser = None,
                    movieInformationDB.movieURL = None,
                    movieInformationDB.favourite = None,
                    movieInformationDB.user = request.user
                    movieInformationDB.uploadedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                    movieInformationDB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                    movieInformationDB.save()
                    print("save")

                except Exception as err:
                    print(err)

        except Exception as err:
            print(err)
        
    except Exception as err:
        print(err)
    
#### Dashboard setContent Section End ####


#### Dashboard Home Section Start ####
@login_required(login_url="/login/")
def inneyeHome(request):
    context = dict()
    movieData = dict()

    try:
        # l1 = ['20 Century Girl', 'The Godfather', 'The Shawshank Redemption', 'The Godfather Part II', '罗小黑战记', "Schindler's List", 'दिलवाले दुल्हनिया ले जायेंगे', 'Cosas imposibles', '千と千尋の神隠し', '12 Angry Men', '同級生', '君の名は。', '기생충', 'The Green Mile', 'The Dark Knight', "Gabriel's Inferno: Part II", "Gabriel's Inferno", '번 더 스테이지: 더 무비', 'Pulp Fiction', 'Il buono, il brutto, il cattivo', 'Forrest Gump', 'The Lord of the Rings: The Return of the King', 'GoodFellas', "Gabriel's Inferno: Part III", 'Nuovo Cinema Paradiso', 'La vita è bella', '七人の侍', '切腹', 'Psycho', 'Once Upon a Time in America', '火垂るの墓', "One Flew Over the Cuckoo's Nest", 'Fight Club', 'Primal: Tales of Savagery', 'O Auto da Compadecida', '소원', 'Cidade de Deus', 'Spider-Man: Into the Spider-Verse', '蛍火の杜へ', '映画 聲の形', 'ハウルの動く城', 'The Empire Strikes Back', '러브 유어셀프 인 서울', 'The Lord of the Rings: The Fellowship of the Ring', '新世紀エヴァンゲリオン劇場版 Air／まごころを、君に', 'ジョゼと虎と魚たち', 'Interstellar', 'The Pianist', 'Sunset Boulevard', 'シン・エヴァンゲリオン劇場版:||', 'Whiplash', 'The Lord of the Rings: The Two Towers', '白蛇 II: 青蛇劫起', 'American History X', 'Rear Window', 'The Shop Around the Corner', '生きる', 'Inception', 'Se7en', 'The Great Dictator', 'Dedicada A Mi Ex', 'もののけ姫', '映画 ギヴン', 'City Lights', '劇場版 ヴァイオレット・エヴァーガーデン', 'Top Gun: Maverick', 'Wolfwalkers', 'The Silence of the Lambs', '天国と地獄', 'Léon: The Professional', '劇場版「鬼滅の刃」無限列車編', 'Modern Times', 'Dead Poets Society', 'Clouds', 'Иди и смотри', 'Five Feet Apart', "C'era una volta il West", 'Life in a Year', 'Purple Hearts', 'Back to the Future', 'Hamilton', '劇場版 呪術廻戦 0', 'Paths of Glory', 'Le Trou', 'Justice League Dark: Apokolips War', 'PERFECT BLUE', 'Apocalypse Now', 'Avengers: Endgame', '7. Koğuştaki Mucize', '青春ブタ野郎はゆめみる少女の夢を見ない', "C'eravamo tanto amati", 'Steven Universe: The Movie', '砂の女', '牯嶺街少年殺人事件', '올드보이', 'Mommy', 'Intouchables', "La leggenda del pianista sull'oceano", 'Avengers: Infinity War', "It's a Wonderful Life", '아가씨', '신과함께-인과 연', 'The Lion King', 'The Art of Racing in the Rain', 'Klaus', '東京物語', 'Persona', 'さよならの朝に約束の花をかざろう', '映画 この素晴らしい世界に祝福を！紅伝説', 'Il sorpasso', '僕のヒーローアカデミア THE MOVIE ヒーローズ：ライジング', '少年的你', 'Green Book', 'Bo Burnham: Inside', "Zack Snyder's Justice League", 'Ladri di biciclette', 'おおかみこどもの雨と雪', 'Miraculous World : New York, les héros unis', 'Doctor Who: The Day of the Doctor', '君の膵臓をたべたい', 'The Apartment', 'Coco', 'Сталкер', 'ヴァイオレット・エヴァーガーデン 外伝 - 永遠と自動手記人形 -', 'Witness for the Prosecution', 'The Shining', 'A Clockwork Orange', '8½', 'Sátántangó', 'Det sjunde inseglet', "Mortal Kombat Legends: Scorpion's Revenge", 'The Kid', 'Inglourious Basterds', 'Vertigo', 'Star Wars', 'The Hate U Give', 'Indagine su un cittadino al di sopra di ogni sospetto', 'Les Enfants du Paradis', 'Gladiator', 'Saving Private Ryan', 'The Prestige', 'The Usual Suspects', 'The Help', 'Portrait de la jeune fille en feu', '新神榜：哪吒重生', 'Memento', 'The Matrix', 'Hacksaw Ridge', 'Shutter Island', 'Call Me by Your Name', 'Minha Mãe é uma Peça 3: O Filme', 'Piper', 'کفرناحوم', 'Abraham Lincoln Vampire Hunter: The Great Calamity', 'Soul', '山椒大夫', 'Joker', 'Taxi Driver', 'Metropolis', 'Black Beauty', 'Wonder', "Singin' in the Rain", 'Amici miei', 'Casablanca', 'Far from the Tree', 'Scener ur ett äktenskap', 'Scarface', 'The Departed', 'All About Eve', 'Como caído del cielo', 'La grande guerra', 'Me contro Te: Il film - La vendetta del Signor S', 'Django Unchained', 'La dolce vita', 'Togo', 'The Father', '用心棒', 'Lock, Stock and Two Smoking Barrels', 'Full Metal Jacket', '羅生門', 'Central do Brasil', 'Reservoir Dogs', 'Good Will Hunting', 'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb', 'My Policeman', 'Alien', 'Double Indemnity', 'Sherlock Jr.', 'Ayla', 'Smultronstället', 'Some Like It Hot', 'I soliti ignoti', 'Андрей Рублёв', 'Bo Burnham: Make Happy', 'Nobody', 'Scooby-Doo! and Kiss: Rock and Roll Mystery', 'The Truman Show', 'Everything Everywhere All at Once', 'Contratiempo', 'Anne of Green Gables', 'かぐや姫の物語', "Michael Jackson's Thriller", 'Harry Potter and the Deathly Hallows: Part 2', 'How to Train Your Dragon: Homecoming', 'Cruella', 'I corti', 'Paris, Texas', 'M - Eine Stadt sucht einen Mörder', 'Kağıttan Hayatlar', '花樣年華', 'En brazos de un asesino', 'Eternal Sunshine of the Spotless Mind', 'Hannah Gadsby: Nanette', '신과함께-죄와 벌', 'Totò, Peppino e la... malafemmina', '赤ひげ', 'Jagten', 'Voces inocentes', 'There Will Be Blood', 'Three Billboards Outside Ebbing, Missouri', 'Pride & Prejudice', 'Дерсу Узала', '도가니', 'পথের পাঁচালী', 'Lion', 'Incendies', 'Les Quatre Cents Coups', 'Una giornata particolare', 'Terminator 2: Judgment Day', "La passion de Jeanne d'Arc", 'La Haine', 'Das Boot', '2001: A Space Odyssey', 'Bound by Honor', 'Rocco e i suoi fratelli', 'The Elephant Man', '택시운전사', 'Jojo Rabbit', 'Love, Simon', 'となりのトトロ', 'WALL·E', 'Prisoners', 'Hidden Figures', 'La meglio gioventù', '乱', 'Prayers for Bobby', 'Palmer', 'Tropa de Elite', '살인의 추억', 'The Grand Budapest Hotel', 'Believe Me: The Abduction of Lisa McVey', 'Sulla mia pelle', 'Loving Vincent', 'Misfit #EresOTeHaces', 'El mesero', 'Kitbull', 'Gifted', 'The Red Shoes', 'Doctor Who: The Time of the Doctor', 'Room', 'Veinteañera, Divorciada y Fantástica', 'Achtste Groepers Huilen Niet', 'Judgment at Nuremberg', 'Le notti di Cabiria', 'Зеркало', 'Das Leben der Anderen', '天気の子', 'In a Heartbeat', 'My Name Is Khan', '重慶森林', 'The Circus', 'Per qualche dollaro in più', 'Requiem for a Dream', 'Miseria e nobiltà', 'Where Hands Touch', 'Que Horas Ela Volta?', 'To Kill a Mockingbird', 'American Beauty', "Ron's Gone Wrong", 'The Wolf of Wall Street', 'The Gold Rush', 'Bingo: O Rei das Manhãs', 'The Thing', 'Amadeus', 'Le Salaire de la peur', 'Song of the Sea', '晩春', 'The Sting', 'Spider-Man: No Way Home', 'Dial M for Murder', 'Citizen Kane', 'Straight Outta Nowhere: Scooby-Doo! Meets Courage the Cowardly Dog', 'Wish Dragon', 'Finch', 'バケモノの子', "A Dog's Journey", 'Harry Potter and the Prisoner of Azkaban', 'The Treasure of the Sierra Madre', 'The General', 'Los olvidados', 'No Manches Frida 2', 'Дурак', '雨月物語', '愛のむきだし', 'The Imitation Game', 'The Deer Hunter', 'Sing 2', 'Bohemian Rhapsody', 'CODA', 'Иван Васильевич меняет профессию', 'Höstsonaten', 'Casino', '기억의 밤', 'Scooby-Doo! Camp Scare', 'Roma città aperta', 'この世界の片隅に', 'Ford v Ferrari', 'Paperman', "Hachi: A Dog's Tale", 'Летят журавли', 'Gran Torino', 'Pink Floyd: The Wall', '隠し砦の三悪人', 'Barry Lyndon', 'Gone with the Wind', 'Thirteen Lives', 'On the Waterfront', 'North by Northwest', '태극기 휘날리며', 'तारे ज़मीन पर', 'El secreto de sus ojos', '마이웨이', 'One Week', 'Hoje Eu Quero Voltar Sozinho', '誰も知らない', 'El ángel exterminador', '김씨 표류기', 'Batman: The Dark Knight Returns, Part 2', 'The Mitchells vs. the Machines', 'Raging Bull', 'All My Life', 'दंगल', "Un condamné à mort s'est échappé", 'Lawrence of Arabia', '1917', '思い出のマーニー', '7번방의 선물', 'The Third Man', '泣きたい私は猫をかぶる', 'Rope', 'Viskningar och rop', '椿三十郎', 'Trainspotting', 'Kill Bill: Vol. 1', '3 Idiots', 'ドラゴンボール超 スーパーヒーロー', 'Rémi sans famille', '天空の城ラピュタ', 'Toy Story', 'La strada', 'Dem Horizont so nah', '大红灯笼高高挂', 'Das Cabinet des Dr. Caligari', 'Million Dollar Baby', 'Tre uomini e una gamba', '竜とそばかすの姫', 'アキラ', 'Before Sunrise', 'Girl in the Basement', 'Scooby-Doo! and the Curse of the 13th Ghost', 'Words on Bathroom Walls', 'Flipped', 'Raya and the Last Dragon', 'Catch Me If You Can', 'Trois couleurs : Rouge', '12 Years a Slave', 'Операция «Ы» и другие приключения Шурика', '蜘蛛巣城', 'Le Voyage dans la Lune', 'ฉลาดเกมส์โกง', 'つみきのいえ', 'Kill Bill: The Whole Bloody Affair', "Divorzio all'italiana", "L'Armée des ombres", 'La notte', "It's Such a Beautiful Day", 'Tel chi el telùn', 'Up', 'The Great Escape', 'Limelight', 'بچه\u200cهای آسمان', 'Il postino', 'La Grande Vadrouille', 'The Sixth Sense', 'What Ever Happened to Baby Jane?', 'Teen Titans Go! vs. Teen Titans', 'Un rescate de huevitos', 'Dallas Buyers Club', 'GHOST IN THE SHELL', 'Mr. Smith Goes to Washington']
        # l2 = ['No Country for Old Men', 'Unforgiven', 'Estômago', 'Blade Runner', 'Babamın Kemanı', 'The Greatest Showman', 'Inside Out', 'Braveheart', '風の谷のナウシカ', 'Captain Fantastic', 'Amarcord', 'Young Frankenstein', 'La Jetée', 'Luck', 'Freedom Writers', 'Jurassic Park', 'The Boy Who Harnessed the Wind', '活着', 'The Tomorrow War', 'Just Mercy', 'Mulan', 'La ciociara', 'La battaglia di Algeri', 'Raiders of the Lost Ark', 'Primos', '耳をすませば', 'The Iron Giant', 'Faust – Eine deutsche Volkssage', 'Rebecca', 'Charm City Kings', 'Chinatown', 'The Cameraman', 'The Cure', "Harry Potter and the Philosopher's Stone", 'The Breadwinner', '유열의 음악앨범', 'Luca', 'Little Women', 'Justice League: The Flashpoint Paradox', 'Aliens', 'In the Name of the Father', 'Vincent', 'To Be or Not to Be', 'Persepolis', '哪吒之魔童降世', 'A Vida Invisível', 'Guardians of the Galaxy', 'جدایی نادر از سیمین', 'About Time', 'Ace in the Hole', 'Novecento', '僕のヒーローアカデミア THE MOVIE ～2人の英雄～', 'خانه\u200cی دوست کجاست؟', 'The Night of the Hunter', 'Mamma Roma', 'The Pursuit of Happyness', "Le Fabuleux Destin d'Amélie Poulain", 'V for Vendetta', 'Sing Street', 'La classe operaia va in paradiso', 'Inner Workings', 'Me Before You', 'Return of the Jedi', 'Иваново детство', 'Roman Holiday', 'Heat', 'Hustle', 'Hors Normes', '오직 그대만', 'Gone Girl', 'Werckmeister harmóniák', 'Safety Last!', 'Miraculous World: Shanghai, la légende de Ladydragon', 'Dancer in the Dark', 'Sherlock: The Abominable Bride', 'Nattvardsgästerna', 'Sunrise: A Song of Two Humans', 'Cindy La Regia', 'La La Land', '東京ゴッドファーザーズ', 'A Street Cat Named Bob', 'Ностальгия', 'The Notebook', 'Per un pugno di dollari', 'Nosotros los nobles', 'Titanic', 'It Happened One Night', 'Kill Bill: Vol. 2', 'Us Again', 'Au revoir là-haut', 'Paper Moon', 'Les Diaboliques', 'Umberto D.', 'Perfetti sconosciuti', 'Fargo', 'Ahí te encargo', 'タンポポ', 'The Theory of Everything', 'Rio Bravo', 'ノーゲーム・ノーライフ ゼロ', 'Whiplash', '万引き家族', 'La Nuit américaine', 'Du rififi chez les hommes', 'Солярис', 'Stand by Me', 'Her', 'La luna', 'Le Samouraï', 'Prey', 'Isle of Dogs', 'Letter from an Unknown Woman', 'Scooby-Doo! and the Samurai Sword', 'Network', 'Le Sommet des dieux', 'ドラゴンボール超スーパー ブロリー', 'Un sac de billes', 'Ordet', 'Dances with Wolves', 'Minha Vida em Marte', 'बजरंगी भाईजान', 'Anatomy of a Murder', 'Knives Out', 'Бриллиантовая рука', 'Scooby-Doo! and the Goblin King', 'The Black Phone', 'Monsieur Verdoux', 'The Boy in the Striped Pyjamas', 'A Beautiful Mind', '霸王别姬', 'Z', 'Skyggen i mit øje', 'Il marchese del Grillo', 'We Bare Bears: The Movie', 'Polisse', '千年女優', 'ヱヴァンゲリヲン新劇場版：破', 'Feast', 'Mary and Max', 'The Grapes of Wrath', 'Dune', 'Mulholland Dr.', 'おくりびと', 'My Little Pony: A New Generation', 'Non essere cattivo', '魔女の宅急便', 'Ben-Hur', 'The Big Lebowski', 'Relatos salvajes', 'Death Note: デスノート', 'Louis C.K.: Hilarious', 'Warrior', 'Mr. Nobody', '一一', 'Papillon', 'Tropa de Elite 2', 'The Nightmare Before Christmas', '공동경비구역 JSA', 'The Last: Naruto the Movie', 'Im Westen nichts Neues', 'Mulholland Drive', 'La migliore offerta', 'Les Tontons flingueurs', 'La Grande Illusion', 'No Manches Frida', 'Love, Rosie', 'Der Untergang', 'The Greatest Beer Run Ever', 'Indiana Jones and the Last Crusade', 'El robo del siglo', 'Hiroshima mon amour', 'The Best Years of Our Lives', '봄 여름 가을 겨울 그리고 봄', 'The Normal Heart', 'कभी ख़ुशी कभी ग़म', 'Partly Cloudy', 'Finding Nemo', 'Monsters, Inc.', 'Regular Show: The Movie', 'World of Tomorrow', 'Såsom i en spegel', "Carlito's Way", 'Vivre sa vie: film en douze tableaux', 'Gone Mom: The Disappearance of Jennifer Dulos', 'Körkarlen', 'The Miracle Worker', '影武者', 'The Bridge on the River Kwai', 'Freaks', 'Before Sunset', 'El Infierno', 'Fantozzi', 'Under sandet', 'Harry Potter and the Goblet of Fire', "L'eclisse", 'Spotlight', 'Daft Punk & Leiji Matsumoto - Interstella 5555 - The 5tory of the 5ecret 5tar 5ystem', 'Dog Day Afternoon', "Rosemary's Baby", 'Logan', 'Der Himmel über Berlin', 'Into the Wild', 'Mortal Kombat Legends: Battle of the Realms', 'Gifted Hands: The Ben Carson Story', 'Coraline', '無間道', 'Ma vie de courgette', 'Brokeback Mountain', 'Ricos de Amor', 'Descendants 3', 'दृश्यम्', '秋刀魚の味', '내 머리 속의 지우개', 'Monty Python and the Holy Grail', 'Back to the Outback', '마녀', 'Midnight Sun', '빈집', 'Fail Safe', 'Constantine: City of Demons - The Movie', 'The Ox-Bow Incident', 'How to Train Your Dragon', 'War Room', 'A Woman Under the Influence', "Who's Afraid of Virginia Woolf?", 'るろうに剣心 最終章 The Final', 'Krótki film o miłości', 'Mishima: A Life in Four Chapters', 'Fanny och Alexander', 'Jungfrukällan', 'Snatch', 'King Richard', 'Toy Story 3', 'Dogville', 'The King of Comedy', '악마를 보았다', 'Der letzte Mann', 'Donnie Darko', 'Notorious', 'パプリカ', 'Werk ohne Autor', 'Batman: Under the Red Hood', 'Presto', 'Ratatouille', 'Elvis', '風立ちぬ', 'Ernest et Célestine', 'Manhattan', 'Anónima', 'I cento passi', 'Profondo rosso', 'Mustang', 'Straight Outta Compton', 'Lisbela e o Prisioneiro', '紅の豚', '추격자', 'The Man Who Shot Liberty Valance', 'Jeux interdits', 'L.A. Confidential', 'Holding the Man', '時をかける少女', 'Inherit the Wind', 'Touch of Evil', 'Pirates of the Caribbean: The Curse of the Black Pearl', 'Mauvaises herbes', 'A Bronx Tale', "Matrimonio all'italiana", 'Shelter', 'PlayTime', '劇場版 七つの大罪 光に呪われし者たち', "God's Own Country", 'Short Term 12', '獣兵衛忍風帖', 'Do the Right Thing', 'Annie Hall', 'Harry Potter and the Deathly Hallows: Part 1', 'Rocky', 'The Perks of Being a Wallflower', 'Non ci resta che piangere', 'Selena', 'All Quiet on the Western Front', 'The Dark Knight Rises', 'Fantastic Mr. Fox', 'Red Shoes and the Seven Dwarfs', 'Bacurau', 'How to Train Your Dragon: The Hidden World', 'Meshes of the Afternoon', 'The Color Purple', '범죄도시', 'Tod@s Caen', 'Big Fish', 'Guerra de Likes', 'రౌద్రం రణం రుధిరం', 'Tres metros sobre el cielo', 'The Untouchables', 'The Kissing Booth 2', 'Scooby-Doo! Abracadabra-Doo', 'Teen Titans: Trouble in Tokyo', 'The Breakfast Club', 'A Matter of Life and Death', 'Le Dîner de cons', 'The Maltese Falcon', 'Life of Brian', 'Divines', 'Amour', 'If Anything Happens I Love You', 'Onward', 'Marriage Story', 'Brief Encounter', '부산행', '傷物語〈Ⅰ鉄血篇〉', 'Doctor Who: Last Christmas', 'K-12', 'Batman: The Dark Knight Returns, Part 1', 'A torinói ló', 'Ya no estoy aquí', 'tick, tick... BOOM!', 'Awakenings', 'Rain Man', '조작된 도시', 'Temple Grandin', 'たそがれ清兵衛', 'Trollhunters: Rise of the Titans', '怪談', 'Nueve reinas', 'El espíritu de la colmena', 'Misery', 'Die Hard', 'The Blues Brothers', 'Cool Hand Luke', 'Minha Mãe é uma Peça: O Filme', 'The Searchers', 'El laberinto del fauno', 'Platoon', 'Sound of Metal', 'Barbie in the 12 Dancing Princesses', 'A Walk to Remember', 'Le Roi et l’oiseau', 'Pride', '天使のたまご', 'Back to the Future Part II', '白蛇：缘起', 'Big Hero 6', 'Mystic River', 'Enola Holmes 2', 'Zootopia', '葉問', 'Maudie', 'Scent of a Woman', 'I, Daniel Blake', 'The Trial of the Chicago 7', 'Demain tout commence', 'Giù la testa', 'Festen', '마더', 'The Hustler', "They Shoot Horses, Don't They?", 'Stalag 17', '劇場版 ソードアート・オンライン -オーディナル・スケール-', 'Fiddler on the Roof', '120 battements par minute', 'The Ten Commandments', 'Eu Não Quero Voltar Sozinho', "The King's Speech", 'The Straight Story', 'Persian Lessons', 'The Hateful Eight', 'Cléo de 5 à 7', 'Angst essen Seele auf', 'Beauty and the Beast', 'The Valet', 'Amici miei - Atto II°', 'Slumdog Millionaire', 'るろうに剣心 最終章 The Beginning', 'The Bad Guys', 'Accattone', 'Day & Night', 'Godzilla vs. Kong', 'Crush', 'Philadelphia', '악인전', '崖の上のポニョ', 'Nosferatu, eine Symphonie des Grauens', 'Padre no hay más que uno', 'Il traditore', 'Harry Potter and the Chamber of Secrets', 'Ma nuit chez Maud', 'The Exorcist', 'Magnolia', "Geri's Game", 'John Mulaney: The Comeback Kid', 'The Wrong Trousers', 'るろうに剣心\u3000伝説の最期編', "The Children's Hour", 'Ricky Gervais: Humanity', '墮落天使', 'Azur et Asmar', 'Edward Scissorhands', 'Le Grand Méchant Renard et autres contes...', 'The Batman']
        # l3 = ['The Broken Circle Breakdown', 'Dom za vešanje', 'Les Choristes', '歩いても 歩いても', 'Hotel Rwanda', 'The Avengers', 'The Sound of Music', 'A Charlie Brown Christmas', 'Le ballon rouge', 'Strangers on a Train', 'Rush', 'Shrek', 'Wrath of Man', '鬼婆', 'Druk', 'Подземље', 'Harvey', 'Le locataire', 'Charade', 'Harry Potter and the Half-Blood Prince', 'Overcomer', 'Dave Chappelle: The Age of Spin', 'Il gattopardo', 'Cat on a Hot Tin Roof', 'The Big Heat', 'Don Camillo', 'The Incredibles', 'Stagecoach', 'En corps', 'Una Película de Huevos', 'पीके', "Breakfast at Tiffany's", 'All the Bright Places', 'Hunt for the Wilderpeople', 'Les demoiselles de Rochefort', "All the President's Men", 'Out of the Past', 'Boże Ciało', 'Mildred Pierce', 'Batman Begins', '늑대소년', 'Spirit: Stallion of the Cimarron', 'Harry Potter and the Order of the Phoenix', 'Z-O-M-B-I-E-S 2', 'Moonrise Kingdom', 'High Noon', 'Nightcrawler', 'In the Heat of the Night', 'Systemsprenger', 'Jongens', '喋血雙雄', 'Il conformista', 'Hair Love', 'Sleuth', 'A Streetcar Named Desire', 'Brazil', 'Il Divo', 'Crna mačka, beli mačor', 'El abrazo de la serpiente', 'La Planète sauvage', 'Sweet Smell of Success', '아저씨', 'The Warriors', 'The Killing', 'Feel the Beat', 'カウボーイビバップ 天国の扉', 'The Bridges of Madison County', 'Scooby-Doo on Zombie Island', 'Fried Green Tomatoes', 'The Gentlemen', 'Kış Uykusu', 'Captain America: The Winter Soldier', "L'armata Brancaleone", 'Riget', 'Eddie Murphy: Delirious', 'Trois couleurs : Bleu', 'Freier Fall', 'Laurence Anyways', "What's Eating Gilbert Grape", 'I vitelloni', 'अंधाधुन', "To All the Boys I've Loved Before", 'Spies in Disguise', 'Steamboat Bill, Jr.', 'Victoria', 'Memoirs of a Geisha', 'La odisea de los giles', 'No se Aceptan Devoluciones', 'How to Train Your Dragon 2', '¿Qué culpa tiene el niño?', '夢', 'The Martian', '12 Angry Men', 'Todo sobre mi madre', 'Roma', 'Mandariinid', 'Jean de Florette', 'The Big Sleep', 'To All the Boys: Always and Forever', 'Offret', 'Mississippi Burning', 'Viridiana', 'The Princess Bride', 'Little Miss Sunshine', 'The Blind Side', 'Encanto', 'La gabbianella e il gatto', 'The Last Picture Show', 'The Philadelphia Story', 'Threads', 'カメラを止めるな！', 'Germania anno zero', 'Breakthrough', 'Chiedimi se sono felice', 'The Lost Weekend', 'ヱヴァンゲリヲン新劇場版：序', 'Le Clan des Siciliens', 'Where the Crawdads Sing', 'ストレンヂア -無皇刃譚-', 'Kind Hearts and Coronets', 'Kubo and the Two Strings', 'Black Swan', 'The Graduate', 'Scarlet Street', 'Cast Away', 'HANA-BI', 'Les Misérables', 'Atonement', 'Laura', 'Alice in den Städten', 'The Wild Bunch', 'Minha Mãe é uma Peça 2: O Filme', 'Synecdoche, New York', 'Shang-Chi and the Legend of the Ten Rings', 'Stand and Deliver', 'White Heat', 'Angels with Dirty Faces', 'कुछ कुछ होता है', 'Triangle of Sadness', 'Ricomincio da tre', 'Harold and Maude', 'Work It', '遊☆戯☆王 THE DARK SIDE OF DIMENSIONS', 'The Ultimate Gift', 'The Big Country', 'Jaws', 'Scooby-Doo! Pirates Ahoy!', 'Who Am I - Kein System ist sicher', 'Primal Fear', 'The Count of Monte Cristo', 'Fitzcarraldo', 'Planet of the Apes', 'Aladdin', 'I Still Believe', "Mickey's Christmas Carol", 'Jules et Jim', 'Sonic the Hedgehog 2', 'Amar te duele', 'Blue Velvet', 'Kingsman: The Secret Service', 'Dave Chappelle: Sticks & Stones', 'BORUTO -NARUTO THE MOVIE-', 'La Règle du jeu', 'È stata la mano di Dio', 'Балканский рубеж', "Ferris Bueller's Day Off", 'The Witcher: Nightmare of the Wolf', '心が叫びたがってるんだ。', 'Boogie Nights', "Ascenseur pour l'échafaud", "Guess Who's Coming to Dinner", 'Броненосец Потёмкин', 'Black Narcissus', 'Paisà', 'るろうに剣心 京都大火編', 'The Raid 2: Berandal', 'JFK', 'The Terminator', 'The Irishman', 'ベルセルク 黄金時代篇III 降臨', 'The Man from Earth', '聖闘士星矢 天界編 序奏 ~overture~', 'October Sky', 'Iron Man', 'Guardians of the Galaxy Vol. 2', 'Mediterraneo', 'King Kong', 'Free Guy', '僕のヒーローアカデミア THE MOVIE ワールド ヒーローズ ミッション', '뷰티 인사이드', 'Lilja 4-Ever', 'Night of the Living Dead', 'Le Loup et le Lion', 'Forever My Girl', 'Being There', 'Quo Vadis, Aida?', 'Papicha', 'Au hasard Balthazar', "Knockin' on Heaven's Door", '告白', 'Les Yeux sans visage', 'À bout de souffle', 'Z-O-M-B-I-E-S 3', 'The Danish Girl', "I Can't Think Straight", 'The Last Emperor', 'Butch Cassidy and the Sundance Kid', 'Ready Player One', 'The Others', 'Le Cercle rouge', 'Giant', 'Arsenic and Old Lace', 'Amores perros', 'The Suicide Squad', 'The Ghost and Mrs. Muir', '春光乍洩', 'Get a Horse!', 'そして父になる', "The World's Fastest Indian", 'La montaña sagrada', 'The Manchurian Candidate', 'Get Out', 'Baisers cachés', 'Searching', 'Plein soleil', 'Le Fantôme de la liberté', 'The Dirty Dozen', '借りぐらしのアリエッティ', 'A Little Princess', 'Anastasia', 'Maurice', 'The Little Prince', 'Ieri, oggi, domani', "Le conseguenze dell'amore", 'Changeling', 'The Sea Beast', 'The Fall', 'Tombstone', 'Seven Pounds', 'Thor: Ragnarok', 'The Fault in Our Stars', 'East of Eden', 'Children of Men', 'Turma da Mônica: Laços', 'Deadpool', 'The Longest Ride', 'Love and Death', 'Remember the Titans', "L'avventura", 'ゴジラ', 'Lost Highway', 'Volevo nascondermi', 'Twelve Monkeys', '修羅雪姫', 'Hable con ella', 'Edge of Tomorrow', '辣手神探', 'Groundhog Day', 'देवदास', 'Moulin Rouge!', 'Bao', "A Dog's Purpose", 'Sleepers', '劇場版 STEINS;GATE 負荷領域のデジャヴ', 'طعم گيلاس', 'Rebel Without a Cause', 'Verdens verste menneske', '喋血街頭', 'Lo chiamavano Trinità...', 'I Origins', 'Brutti, sporchi e cattivi', 'Manon des sources', 'Billy Elliot', 'Un prophète', 'Fatherhood', 'En man som heter Ove', '言の葉の庭', 'In a Lonely Place', 'Tři oříšky pro Popelku', 'La Rafle', 'The Longest Day', 'Tell It to the Bees', 'The Servant', 'Tangled', 'Bande à part', 'ドールズ', 'Boyz n the Hood', 'Little Big Man', 'Blue Miracle', 'Lou', 'Toy Story 2', 'The Wizard of Oz', 'Road to Ninja: Naruto the Movie', 'Krótki film o zabijaniu', 'One, Two, Three', 'The Bride of Frankenstein', 'American Gangster', "The Man Who Wasn't There", 'Bianca', 'My Fair Lady', 'Gilda', '2 Hearts', 'Le Chant du loup', 'What We Do in the Shadows', 'Moon', 'BURN·E', 'Le scaphandre et le papillon', 'Imagine Me & You', 'Dogman', 'The Call of the Wild', 'Arrival', 'Beasts of No Nation', 'Still Life', 'The Snowman', 'Secrets & Lies', 'Shottas', 'Halloween', 'The Banker', 'Cani arrabbiati', 'The Hobbit: The Desolation of Smaug', 'Running on Empty', 'The Curious Case of Benjamin Button', 'Bringing Up Baby', 'The Conjuring: The Devil Made Me Do It', 'Detachment', 'My Dinner with Andre', 'Kramer vs. Kramer', 'Moana', 'Ex Machina', 'Drive', 'Undisputed III: Redemption', 'My Man Godfrey', 'The Odd Couple', 'Mar adentro', 'Instant Family', 'Sin nombre', 'In Cold Blood', 'Ghostbusters: Afterlife', "Jusqu'à la garde", 'Hotel Mumbai', 'るろうに剣心', 'Mad Max: Fury Road', 'Splendor in the Grass', 'I Am Sam', 'Badlands', 'Mary Poppins', 'The SpongeBob Movie: Sponge on the Run', 'The Blue Umbrella', 'Fireproof', 'Edmond', 'Me and Earl and the Dying Girl', '菊次郎の夏', 'Campeones', '学園黙示録 HIGHSCHOOL OF THE DEAD ドリフターズ・オブ・ザ・デッド', 'Where Eagles Dare', 'A Quiet Place Part II', 'బాహుబలి:ద బిగినింగ్', 'Good Bye Lenin!', '콜', 'We Need to Talk About Kevin', 'The Last Samurai', 'Captain Phillips', 'Thelma & Louise', 'Evil Dead II', 'Injustice', '劇場版 七つの大罪 天空の囚われ人', 'El cuerpo', 'Sling Blade', 'The Conversation', 'Batman: The Long Halloween, Part One', 'Chill Out, Scooby-Doo!', 'バブル', 'The Game', 'きみと、波にのれたら', 'Spartacus', '친절한 금자씨', 'The Thin Man', 'Night on Earth', 'The Legend of Sleepy Hollow', 'Shadow of a Doubt', "The Emperor's New Groove", '10 Things I Hate About You', 'Girl, Interrupted', 'Novembre', 'PAW Patrol: Mighty Pups', 'Nous trois ou rien', 'Toy Story 4', 'Брат', 'Hannah and Her Sisters', 'Gattaca', 'Mysterious Skin', 'Midnight Express', 'Ninotchka', 'The Croods: A New Age', 'Veloce come il vento', 'The Favourite', '시', 'Justice Society: World War II', 'My Left Foot: The Story of Christy Brown', 'True Romance']
        # l4 = ['Hot Fuzz', 'Control', 'La Double Vie de Véronique', 'The French Connection', 'The Magnificent Seven', 'コクリコ坂から', 'Mr. Deeds Goes to Town', 'Escape from Alcatraz', 'Waking Life', 'Serpico', 'Beautiful Boy', 'Sabrina', 'Mein Blind Date mit dem Leben', 'サマーウォーズ', 'Aguirre, der Zorn Gottes', 'The Butterfly Effect', 'Seul contre tous', 'Hocus Pocus 2', 'Doctor Zhivago', 'BlacKkKlansman', 'The Book of Henry', 'Le Charme discret de la bourgeoisie', 'ドラゴンボールZ・絶望への反抗!!残された超戦士・悟飯とトランクス', 'Menace II Society', 'Treasure Planet', '4 luni, 3 săptămîni și 2 zile', 'Profumo di donna', 'Apocalypto', 'Gandhi', 'Key Largo', 'The Conjuring', 'Midnight in Paris', 'Shaun of the Dead', 'Un chien andalou', 'Cinderella Man', 'Dark Waters', 'Manchester by the Sea', 'Minions: The Rise of Gru', 'बर्फी!', 'Courageous', 'The Asphalt Jungle', '달콤한 인생', 'Abominable', 'Avatar', 'Возвращение', 'The Invisible Man', 'Donnie Brasco', 'Coach Carter', 'Batman: The Long Halloween, Part Two', 'Padre no hay más que uno 2: la llegada de la suegra', '감기', 'La piel que habito', 'Empire of the Sun', 'The Lighthouse', 'La grande bellezza', "L'Atalante", 'Una pura formalità', 'Låt den rätte komma in', "L'Homme de Rio", 'The Book of Life', 'ワンピース フィルム ゼット', 'X-Men: Days of Future Past', 'Suspiria', 'A Close Shave', '海街diary', 'Il secondo tragico Fantozzi', 'Tystnaden', 'Medianeras', 'Gladiator', 'Gaslight', 'Frankenstein', 'The Day the Earth Stood Still', 'The Two Popes', 'Лето', 'To Sir, with Love', 'Män som hatar kvinnor', 'Babam ve Oğlum', 'The Machinist', 'Malcolm X', "J'ai perdu mon corps", 'Blood Diamond', 'Le quai des brumes', 'Casino Royale', 'Midnight Cowboy', 'The Fifth Element', 'Blade Runner 2049', 'Somewhere in Time', 'The Birds', 'ज़िन्दगी ना मिलेगी दोबारा', 'The Goonies', '英雄', 'Turning Red', 'Black Panther: Wakanda Forever', 'The Dirt', "J'ai tué ma mère", 'Gun Crazy', 'ルパン三世 カリオストロの城', 'Batman: Mask of the Phantasm', 'The Wrestler', 'The Day of the Jackal', 'The Revenant', 'Der siebente Kontinent', 'Bullet Train', 'I, Tonya', 'Days of Heaven', "Sullivan's Travels", 'Kes', 'I Can Only Imagine', 'Stargirl', 'The Unforgivable', 'Калашников', 'भाग मिल्खा भाग', 'Le Corbeau', 'The Killing Fields', 'Paul, Apostle of Christ', 'A Star Is Born', 'Boyhood', 'Le avventure di Pinocchio', 'The Outlaw Josey Wales', 'The Lady Vanishes', 'Phantom of the Paradise', 'Le Procès', 'Who Framed Roger Rabbit', 'The Man Who Knew Too Much', '판도라', 'Crimes and Misdemeanors', 'Zodiac', 'Birdman of Alcatraz', 'The Death of Superman', "You Can't Take It with You", 'E.T. the Extra-Terrestrial', 'Ed Wood', 'The Rocky Horror Picture Show', 'Hercules', 'Corpse Bride', 'Big Time Adolescence', 'Then Came You', 'La Cité de la peur', 'The Boss Baby: Family Business', 'The Last Full Measure', 'Fury', 'Die Welle', "L'Année dernière à Marienbad", 'How to Steal a Million', 'The Man Who Would Be King', 'Facing the Giants', 'Αλέξης Ζορμπάς', 'A Few Good Men', 'Upgrade', 'La tortue rouge', 'Incredibles 2', 'Lilo & Stitch', 'The Sandlot', 'Rescued by Ruby', 'Das weiße Band - Eine deutsche Kindergeschichte', 'Play It Again, Sam', 'Patton', 'Happiness', 'Ciao Alberto', 'Imitation of Life', 'Barbie as The Princess & the Pauper', 'This Is England', 'Bonnie and Clyde', 'The Last Duel', 'Prison Break: The Final Break', 'Desert Flower', 'The Crow', 'A Grand Day Out', 'Vivir dos veces', 'Promising Young Woman', '감시자들', 'Invasion of the Body Snatchers', 'Repulsion', 'Still Alice', '吸血鬼ハンターD ブラッドラスト', 'Il grande silenzio', 'Dirty Harry', "L'Insulte", 'Zwartboek', 'Carandiru', 'Dawn of the Dead', 'Deadpool 2', 'La Folie des grandeurs', '엽기적인 그녀', 'After Hours', 'Before Midnight', "Travolti da un insolito destino nell'azzurro mare d'agosto", '花木兰', "Miller's Crossing", 'Walk the Line', 'Burrow', 'Mr & Mme Adelman', 'Hedwig and the Angry Inch', 'The Hating Game', 'The Train', 'Father Stu', 'Ballon', '警察故事', 'Jungle Cruise', 'The Royal Tenenbaums', 'Breaking the Waves', 'Aquarius', 'The Incredible Shrinking Man', "No Man's Land", 'The Long Goodbye', 'Au revoir les enfants', '霍元甲', 'Predator', 'La Belle et la Bête', 'Sauver ou périr', 'For the Birds', '少林三十六房', 'Almost Famous', 'Lucky Number Slevin', 'Zimna wojna', 'The Book Thief', 'La maschera del demonio', 'Les Chatouilles', 'A Perfect World', 'Trouble in Paradise', 'Carol', "Bir Zamanlar Anadolu'da", 'The Devils', 'Love & Basketball', 'Illusions perdues', 'Spider-Man: Far from Home', 'The Shack', 'Rogue One: A Star Wars Story', 'Il capitale umano', '3096 Tage', '金陵十三釵', 'Il vangelo secondo Matteo', 'Justice League: War', 'A Night at the Opera', 'Spoorloos', 'Willy Wonka & the Chocolate Factory', '让子弹飞', 'Marty', 'Glory', 'DC League of Super-Pets', 'Così è la vita', 'This Is Spinal Tap', 'mid90s', 'Paddington 2', 'The Best of Me', 'Le Premier Jour du reste de ta vie', 'Kung Fury', 'The Guernsey Literary & Potato Peel Pie Society', '복수는 나의 것', 'The Last Letter from Your Lover', "I'm Not Ashamed", 'Zelig', 'Eyes Wide Shut', 'The Name of the Rose', 'Cape Fear', 'Volver', 'Birdman or (The Unexpected Virtue of Ignorance)', 'Hamlet', 'Tutto quello che vuoi', 'Patients', 'レッドライン', 'The Adventures of Robin Hood', 'Cet obscur objet du désir', 'Irma la Douce', 'Peeping Tom', 'My Cousin Vinny', '18 regali', 'Star Trek II: The Wrath of Khan', 'ドラゴンボールZ たったひとりの最終決戦〜フリーザに挑んだZ戦士 孫悟空の父〜', 'Johnny Got His Gun', "It's the Great Pumpkin, Charlie Brown", '飲食男女', '¿Y cómo es él?', 'Pupille', 'To Have and Have Not', 'Ghostbusters', 'Barton Fink', 'South Park: Post COVID: The Return of COVID', 'Vargtimmen', 'Training Day', 'A través de mi ventana', 'The Mauritanian', 'Dunkirk', 'Ordinary People', '英雄本色', 'In Bruges', 'The Magdalene Sisters', 'Letters from Iwo Jima', 'Scarface', '精武英雄', 'The Insider', 'Durante la tormenta', 'Peaceful Warrior', 'How the Grinch Stole Christmas!', 'First Blood', 'Adams æbler', 'Le Grand Bleu', 'Miss Sloane', 'कल हो ना हो', 'Abre los ojos', 'Trois couleurs : Blanc', 'Baby Driver', 'Sonatine', 'La Môme', 'BAC Nord', 'Miss You Already', 'Mind Game', 'The Secret of NIMH', 'Spellbound', 'The Woman in the Window', '...continuavano a chiamarlo Trinità', 'C.R.A.Z.Y.', 'Back to the Future Part III', 'Scott Pilgrim vs. the World', 'Nocturnal Animals', 'The Age of Adaline', 'Shane', 'Lifted', 'My Darling Clementine', 'Richard Jewell', '野良犬', 'Pierrot le fou', '葉問2', 'Johnny Guitar', '新世紀エヴァンゲリオン 劇場版 DEATH & REBIRTH シト新生', 'The Secret Life of Bees', 'An Affair to Remember', 'Sense and Sensibility', "Boys Don't Cry", 'The One and Only Ivan', 'Vivo', 'ワンピース フィルム ストロングワールド', 'Chemical Hearts', 'No Time to Die', 'Celda 211', 'The Farewell', 'Lo chiamavano Jeeg Robot', '...altrimenti ci arrabbiamo!', 'The Fugitive', 'All That Jazz', '人狼 JIN-ROH', 'The Fallout', 'PAW Patrol: The Movie', 'The Thin Red Line', 'The Bourne Identity', 'Monster Pets: A Hotel Transylvania Short', 'Superman II: The Richard Donner Cut', 'Eraserhead', 'Lemonade Mouth', '哀しみのベラドンナ', 'The Taking of Pelham One Two Three', 'Doctor Strange in the Multiverse of Madness', 'Breathe', 'Unbroken', 'ベルセルク 黄金時代篇II ドルドレイ攻略', 'Il deserto rosso', 'The Lion in Winter', 'Frida', 'Uncle Frank', 'Fabrizio De André: Principe libero', 'Левиафан', 'Smetto quando voglio', 'True Grit', 'Man on Fire', 'Ray', "L'École buissonnière", 'Predestination', 'The Right Stuff', "Bram Stoker's Dracula", 'Tudo Bem no Natal Que Vem', 'Maggie Simpson in Playdate with Destiny', 'Nebraska', 'The Artist', "Scooby-Doo! in Where's My Mummy?", "The Devil's Advocate", 'Jeder für sich und Gott gegen alle', 'The Reader', 'Last Night in Soho', 'Once Upon a Time… in Hollywood', 'Teen Titans: The Judas Contract', 'Captain America: Civil War', '地獄でなぜ悪い', 'The Hurricane', '大鱼海棠', 'American Sniper', 'La pazza gioia', 'Glory Road', 'वीर-ज़ारा', 'Apollo 13', 'Sin City', 'Cherry', 'John Wick: Chapter 3 - Parabellum', 'Star Trek', 'Chaplin', 'The Last King of Scotland', 'Dolor y gloria', 'Miracles from Heaven', 'Sala samobójców', '鉄コン筋クリート', '少年黃飛鴻之鐵馬騮']
        # l5 = ['Donne-moi des ailes', "You're Not You", 'Něco z Alenky', 'ドラゴンボールZ 復活のフュージョン!! 悟空とベジータ', 'Rushmore', 'Doctor Strange', 'Barbie: Princess Charm School', 'درباره الی\u200e\u200e', 'The Innocents', '攻殻機動隊 2.0', 'A Boy Called Christmas', 'The Secret of Kells', 'Men of Honor', 'Mies vailla menneisyyttä', 'Smetto quando voglio - Ad honorem', 'Wind River', 'Tesis', 'あん', 'Lone Survivor', 'The Life of David Gale', 'Les Parapluies de Cherbourg', 'Clerks', "A Hard Day's Night", 'Gegen die Wand', '킹덤: 아신전', '100 metros', 'Honig im Kopf', 'On the Basis of Sex', 'Boîte noire', 'The Hunger Games: Catching Fire', 'Spirit Untamed', 'The Verdict', 'High Plains Drifter', 'Cabaret', 'Diarios de motocicleta', 'The Godfather Part III', 'Frantz', 'Scooby-Doo and the Ghoul School', 'La Belle Époque', "A Dog's Life", 'Enter the Dragon', 'The Passion of the Christ', 'Pretty Woman', 'El Dorado', 'The Station Agent', 'Greyhound', 'Selma', 'Serbuan maut', 'A Place in the Sun', 'Les Amants du Pont-Neuf', "Ocean's Eleven", 'Status Update', 'Being John Malkovich', 'The Good Lie', 'Blow-Up', 'Belle de jour', 'Waves', 'El Ángel', 'キュア', 'Русский ковчег', 'Y tu mamá también', 'When Harry Met Sally...', '버닝', 'The Florida Project', 'The Lego Movie', 'His Girl Friday', 'Das Experiment', 'Le Père Noël est une ordure', 'Oslo, 31. august', 'Caro Diario', 'Contact', 'Dog', 'The In Between', 'Ecce Bombo', 'Queen', 'District 9', 'The Bourne Ultimatum', 'Mudbound', 'McFarland, USA', 'Joyeux Noël', 'Erin Brockovich', 'Битва за Севастополь', 'The Man in the Moon', 'Vampyr - Der Traum des Allan Grey', 'ドライブ・マイ・カー', 'Minari', 'La noche de 12 años', 'Okja', 'Ostwind', 'Submarine', 'Naked', 'Les Héritiers', 'The Purple Rose of Cairo', 'As Good as It Gets', 'The Piano', 'Inside Man', 'American Satan', 'Dieses bescheuerte Herz', 'ハウス', '猛龍過江', 'Legends of the Fall', 'Red River', 'Scooby-Doo! WrestleMania Mystery', 'Non si sevizia un paperino', '醉拳二', 'Malèna', 'Duel', 'Braindead', 'Grease', 'Moonlight', 'Justice League: Doom', 'O Homem Que Copiava', 'Tarzan', 'Nos jours heureux', '살인자의 기억법', 'Smetto quando voglio - Masterclass', 'Mission: Impossible - Fallout', 'One Day', 'Once', 'Lazzaro felice', '신세계', 'Frances Ha', 'Une Femme est une femme', 'A Quiet Place', 'Pickup on South Street', 'Withnail & I', 'Glengarry Glen Ross', 'Black Widow', 'Le Corniaud', 'Mad Max 2', 'August Rush', 'First They Killed My Father', 'The Mission', 'The Peanut Butter Falcon', 'Palmeras en la nieve', 'Sedmikrásky', "Sophie's Choice", 'The Secret Garden', 'Black Panther', 'Adaptation.', 'La mala educación', 'The Best of Enemies', 'Creed', 'Sorcerer', 'Fantasia', 'Once Were Warriors', 'Moxie', 'Trolls World Tour', 'The Last of the Mohicans', 'Enemy at the Gates', 'Life of Pi', 'Eşkıya', "Kelly's Heroes", 'Star Wars: Episode III - Revenge of the Sith', '卧虎藏龍', 'Zulu', "Jacob's Ladder", 'The Hunt for Red October', 'Mon oncle', 'The 39 Steps', 'Été 85', 'Blindspotting', "La Promesse de l'aube", 'Enter the Void', 'La Gloire de mon Père', 'The Lady from Shanghai', 'Judas and the Black Messiah', 'Oscar', 'American Psycho', 'Saw', 'The Simpsons: The Good, the Bart, and the Loki', 'The Great Gatsby', 'The Basketball Diaries', 'Home Alone', 'Lost in Translation', 'Lifeboat', 'ルパン三世 THE FIRST', 'Descendants 2', 'Pelé: Birth of a Legend', 'Stuck in Love', "Sei donne per l'assassino", 'The Killers', 'Nosferatu - Phantom der Nacht', 'जोधा अकबर', '功夫', "Les 12 travaux d'Astérix", 'Beetlejuice', 'Duck Soup', 'Les Aventures de Rabbi Jacob', 'Serenity', 'Le Père Noël est une ordure', 'Barbie and the Diamond Castle', 'The Time Machine', 'The Remains of the Day', 'The Devil Wears Prada', 'Sicario', 'John Wick', 'Boy', 'Taken', 'Mujeres al borde de un ataque de nervios', 'An American Werewolf in London', 'The Woman King', 'Land and Freedom', 'Lolita', 'If I Stay', 'En kongelig affære', 'Shine', 'The Omen', 'Interview with the Vampire', 'Sissi', 'The Fighter', 'Little Lord Fauntleroy', "Scooby-Doo! and the Witch's Ghost", 'Office Space', 'Happiest Season', "The Zookeeper's Wife", "Futurama: Bender's Big Score", 'Love and Monsters', 'Run', 'ももへの手紙', 'Le violon rouge', 'Jeremiah Johnson', 'Fruitvale Station', 'Top Hat', 'Sonic the Hedgehog', "L'Instinct de mort", 'Scooby-Doo! and the Reluctant Werewolf', 'Seconds', 'Miracle on 34th Street', 'The Cook, the Thief, His Wife & Her Lover', 'Teen Titans Go! To the Movies', 'Philomena', 'Blow', 'Batman: Assault on Arkham', 'EverAfter', 'Road to Perdition', 'Now Is Good', 'The Fly', 'The Wind That Shakes the Barley', 'Close Encounters of the Third Kind', 'Sorry We Missed You', 'All That Heaven Allows', 'Secretariat', 'Scooby-Doo! and the Loch Ness Monster', 'Dazed and Confused', 'Eastern Promises', '25th Hour', 'Only the Brave', 'Les Triplettes de Belleville', 'Dead Man Walking', 'Scream', 'The Impossible', 'Bianco, rosso e Verdone', 'Scooby-Doo! and the Cyber Chase', 'Down by Law', 'Нелюбовь', 'Steamboat Willie', 'Mutiny on the Bounty', 'A Time to Kill', 'Black Hawk Down', 'Tengo ganas de ti', 'Les Bronzés font du ski', 'Play', 'Le Cerveau', 'Possession', 'Viaggio in Italia', 'ベルセルク 黄金時代篇I 覇王の卵', 'Cyrano de Bergerac', 'Spider-Man: Homecoming', "My Sister's Keeper", 'My Girl', 'Johnny Stecchino', 'Martyrs', 'Europa', 'Astérix & Obélix Mission Cléopâtre', 'I Kina spiser de hunde', 'Float', 'Southpaw', 'Saving Mr. Banks', '21 Grams', 'To Catch a Thief', 'On a retrouvé la 7ème compagnie', 'Rise of the Guardians', 'Rudy', 'Mr. Church', 'బాహుబలి 2: ది కన్ క్లూజన్', 'Giulietta degli spiriti', 'Masculin féminin', 'Freaks Out', 'The Girl with the Dragon Tattoo', 'Falling Down', 'Precious', '飛鷹計劃', 'Extraction', 'Rocketman', 'Ghostland', 'The Butler', 'Romeo and Juliet', 'Match Point', 'Darkest Hour', 'Perdona si te llamo amor', 'Tucker and Dale vs. Evil', 'MEMORIES', 'Wake in Fright', 'Jackie Brown', 'Fantastic Beasts and Where to Find Them', 'おもひでぽろぽろ', 'The Little Mermaid', 'Bloody Sunday', 'La Pianiste', 'Justice League vs. Teen Titans', 'Remember', 'Full Out', 'Now You See Me', 'The Muppet Christmas Carol', 'Goldfinger', 'The Big Sick', 'STAND BY ME ドラえもん', 'The Wicker Man', 'American Me', 'Scrooge', '醉拳', 'Christopher Robin', '곡성', 'サカサマのパテマ', 'Z-O-M-B-I-E-S', 'Les Misérables', 'Funny Games', 'Morte a Venezia', 'The African Queen', 'Dirty Dancing', 'Anima', 'Papillon', 'Deconstructing Harry', 'Maleficent: Mistress of Evil', 'The Social Network', 'Blood and Bone', 'Bad Day at Black Rock', 'Train de vie', 'Elisa y Marcela', "La mafia uccide solo d'estate", 'Scooby-Doo! and the Monster of Mexico', 'Wait Until Dark', 'Dark City', 'Twin Peaks: Fire Walk with Me', 'Perfume: The Story of a Murderer', 'A Man for All Seasons', 'Good Morning, Vietnam', 'Harriet', 'Febbre da cavallo', 'Boiling Point', 'Dear Basketball', 'From Here to Eternity', 'Giant Little Ones', 'Le fate ignoranti', 'Gentlemen Prefer Blondes', 'Phineas and Ferb: The Movie: Candace Against the Universe', 'A Christmas Carol', 'The Quiet Man', 'Ice Age', 'Woman in Gold', "L'ennemi public n°1", "Winchester '73", 'Persuasion', 'Nashville', 'A Shot in the Dark', 'Suite Française', 'Star Trek Into Darkness', 'Sommaren med Monika', 'Mine vaganti', 'La prima cosa bella', 'Suddenly, Last Summer', 'Minority Report', '20th Century Women', 'The Secret Scripture', 'Law Abiding Citizen', '攻殻機動隊: Stand Alone Complex - Solid State Society', 'La ley del deseo', 'Delicatessen', 'Enola Holmes', 'Un long dimanche de fiançailles', 'Split', 'The Big Short', 'Walkabout', "Pirates of the Caribbean: Dead Man's Chest", 'Le Nom des gens', '秒速5センチメートル', 'The Party', 'Mia et le lion blanc', 'Ophelia', 'Lava', 'ช็อคโกแลต', 'The Meaning of Life', 'The Abyss', 'Heathers', 'La Cité des Enfants Perdus', '헤어질 결심', 'Blow Out', 'Baisers volés', 'The Physician']

        #for item in l3:
        #    setContent(request,item)
        
        # for item in l3:
        #     setContent(request,item)
        
        
        
        context['segment'] = 'inneyeHome'
        
        context['types'] = ["actionCount","adventureCount","animationCount","comedyCount","crimeCount","documentaryCount","dramaCount","familyCount","fantasyCount","historyCount","horrorCount","mysteryCount","romanceCount","sifiCount","thrillerCount","warCount","westernCount"]
        
        context['actionCount'] = movieInformation.objects.filter(movieType__icontains='Action').count()
        context['adventureCount'] = movieInformation.objects.filter(movieType__icontains='Adventure').count()
        context['animationCount'] = movieInformation.objects.filter(movieType__icontains='Animation').count()
        context['comedyCount'] = movieInformation.objects.filter(movieType__icontains='Comedy').count()
        context['crimeCount'] = movieInformation.objects.filter(movieType__icontains='Crime').count()
        context['documentaryCount'] = movieInformation.objects.filter(movieType__icontains='Documentary').count()
        context['dramaCount'] = movieInformation.objects.filter(movieType__icontains='Drama').count()
        context['familyCount'] = movieInformation.objects.filter(movieType__icontains='Family').count()
        context['fantasyCount'] = movieInformation.objects.filter(movieType__icontains='Fantasy').count()
        context['historyCount'] = movieInformation.objects.filter(movieType__icontains='History').count()
        context['horrorCount'] = movieInformation.objects.filter(movieType__icontains='Horror').count()
        context['mysteryCount'] = movieInformation.objects.filter(movieType__icontains='Mystery').count()
        context['romanceCount'] = movieInformation.objects.filter(movieType__icontains='Romance').count()
        context['sifiCount'] = movieInformation.objects.filter(movieType__icontains='Science Fiction').count()
        context['thrillerCount'] = movieInformation.objects.filter(movieType__icontains='Thriller').count()
        context['warCount'] = movieInformation.objects.filter(movieType__icontains='War').count()
        context['westernCount'] = movieInformation.objects.filter(movieType__icontains='Western').count()
        
        context['action'] = movieInformation.objects.filter(movieType__icontains='Action').values()
        context['adventure'] = movieInformation.objects.filter(movieType__icontains='Adventure').values()
        context['animation'] = movieInformation.objects.filter(movieType__icontains='Animation').values()
        context['comedy'] = movieInformation.objects.filter(movieType__icontains='Comedy').values()
        context['crime'] = movieInformation.objects.filter(movieType__icontains='Crime').values()
        context['documentary'] = movieInformation.objects.filter(movieType__icontains='Documentary').values()
        context['drama'] = movieInformation.objects.filter(movieType__icontains='Drama').values()
        context['family'] = movieInformation.objects.filter(movieType__icontains='Family').values()
        context['fantasy'] = movieInformation.objects.filter(movieType__icontains='Fantasy').values()
        context['history'] = movieInformation.objects.filter(movieType__icontains='History').values()
        context['horror'] = movieInformation.objects.filter(movieType__icontains='Horror').values()
        context['mystery'] = movieInformation.objects.filter(movieType__icontains='Mystery').values()
        context['romance'] = movieInformation.objects.filter(movieType__icontains='Romance').values()
        context['sifi'] = movieInformation.objects.filter(movieType__icontains='Science Fiction').values()
        context['thriller'] = movieInformation.objects.filter(movieType__icontains='Thriller').values()
        context['war'] = movieInformation.objects.filter(movieType__icontains='War').values()
        context['western'] = movieInformation.objects.filter(movieType__icontains='Western').values()
        
        
        movieData['action'] = movieInformation.objects.filter(movieType__icontains='Action').values()
        movieData['adventure'] = movieInformation.objects.filter(movieType__icontains='Adventure').values()
        movieData['animation'] = movieInformation.objects.filter(movieType__icontains='Animation').values()
        movieData['comedy'] = movieInformation.objects.filter(movieType__icontains='Comedy').values()
        movieData['crime'] = movieInformation.objects.filter(movieType__icontains='Crime').values()
        movieData['documentary'] = movieInformation.objects.filter(movieType__icontains='Documentary').values()
        movieData['drama'] = movieInformation.objects.filter(movieType__icontains='Drama').values()
        movieData['family'] = movieInformation.objects.filter(movieType__icontains='Family').values()
        movieData['fantasy'] = movieInformation.objects.filter(movieType__icontains='Fantasy').values()
        movieData['history'] = movieInformation.objects.filter(movieType__icontains='History').values()
        movieData['horror'] = movieInformation.objects.filter(movieType__icontains='Horror').values()
        movieData['mystery'] = movieInformation.objects.filter(movieType__icontains='Mystery').values()
        movieData['romance'] = movieInformation.objects.filter(movieType__icontains='Romance').values()
        movieData['sifi'] = movieInformation.objects.filter(movieType__icontains='Science Fiction').values()
        movieData['thriller'] = movieInformation.objects.filter(movieType__icontains='Thriller').values()
        movieData['war'] = movieInformation.objects.filter(movieType__icontains='War').values()
        movieData['western'] = movieInformation.objects.filter(movieType__icontains='Western').values()
        
        context['movieData'] = movieData
        
        context['movieInformationDB'] = movieInformation.objects.filter(movieType__icontains='Action').values()

        html_template = loader.get_template('home/inneye-home.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard home Section End ####



#### Dashboard Movies Section Start ####
@login_required(login_url="/login/")
def inneyeMovies(request):
    context = dict()

    try:

        context['segment'] = 'inneyeMovies'

        html_template = loader.get_template('home/inneye-home.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard Movies Section End ####



#### Dashboard Series Section Start ####
@login_required(login_url="/login/")
def inneyeSeries(request):
    context = dict()

    try:

        context['segment'] = 'inneyeSeries'

        html_template = loader.get_template('home/inneye-home.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard Series Section End ####



#### Dashboard Categories Section Start ####
@login_required(login_url="/login/")
def inneyeCategories(request, movieType):
    context = dict()

    try:
        movieInformationDB = movieInformation.objects.filter(movieType__icontains=movieType).values()
        context['segment'] = movieType
        context['movieInformationDB'] = movieInformationDB

        html_template = loader.get_template('home/inneye-categories.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard Categories Section End ####



#### Dashboard Watch Section Start ####
@login_required(login_url="/login/")
def inneyeWatch(request, movieId):
    context = dict()

    try:

        movieInformationDB = movieInformation.objects.filter(movieId = movieId).values()
        
        context['segment'] = 'inneyeWatch'
        context['movieInformationDB'] = movieInformationDB

        html_template = loader.get_template('home/inneye-watch.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard Watch Section End ####



#### Dashboard Watch Section Start ####
@login_required(login_url="/login/")
def inneyeWatchSeries(request):
    context = dict()

    try:
        context['segment'] = 'inneyeWatchSeries'

        html_template = loader.get_template('home/inneye-watch-series.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard Watch Section End ####



#### Dashboard Watch Section Start ####
@login_required(login_url="/login/")
def inneyePlay(request, movieId):
    context = dict()

    try:
        playBackMovie = movieInformation.objects.filter(movieId = movieId).values()
        movieInformationDB = movieInformation.objects.filter(movieType__icontains="Action").values()
        context['segment'] = "inneyePlay"
        context['playBackMovie'] = playBackMovie
        context['movieInformationDB'] = movieInformationDB

        html_template = loader.get_template('home/inneye-player.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-500.html')
        logger.info(templateError.get('message'))
        logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard Watch Section End ####



#### Dashboard pages Section Start ####
@login_required(login_url="/login/")
def pages(request):
    context = dict()

    try:
        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except Exception as err:

        html_template = loader.get_template('home/page-404.html')
        logger.info(templateNotFound.get('message'))
        # logger.error(err)
        return HttpResponse(html_template.render(context, request))
#### Dashboard pages Section End ####



# #### Dashboard Index Section Start ####
# @login_required(login_url="/login/")
# def index(request):
#     context = dict()

#     try:
#         hotelName = serverRegister.objects.values_list('hotelName')

#         context['segment'] = 'index'
#         context['serverCount'] = serverRegister.objects.filter().count()
#         context['controllerCount'] = DVC.objects.filter().count()
#         context['unknownControllerCount'] = unknownDVC.objects.filter().count()
#         context['dvcList'] = [DVC.objects.filter(hotelName = name).count() for name in [item[0] for item in hotelName]]
#         context['serverList'] = [item[0] for item in hotelName]

#         html_template = loader.get_template('home/index.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Index Section End ####



# #### Dashboard Server Information Section Start ####
# @login_required(login_url="/login/")
# def serverInfo(request):
#     context = dict()

#     try:
#         serverDB = serverRegister.objects.filter().values()
#         context['segment'] = 'server'
#         context['serverDB'] = serverDB
#         html_template = loader.get_template('home/server.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Server Information Section End ####



# #### Dashboard Server Register Section Start ####
# @login_required(login_url="/login/")
# def serverRegistration(request):
#     context = dict()

#     try:
#         if request.user.is_superuser:

#             context['segment'] = 'addServer'

#             if request.method == 'POST':

#                 try:
#                     if serverRegister.objects.filter(Q(macAddress = request.POST.get('macAddress')) | Q(dvsURL = request.POST.get('dvsUrl')) | Q(kongURL=request.POST.get('kongUrl')) | Q(kongFqdn=request.POST.get('kongFqdn'))).exists():
                        
#                         try:
#                             serverDB = serverRegister.objects.filter(Q(macAddress = request.POST.get('macAddress')) | Q(dvsURL = request.POST.get('dvsUrl')) | Q(kongURL=request.POST.get('kongUrl')) | Q(kongFqdn=request.POST.get('kongFqdn')))
                            
#                             hotelName = request.POST.get('hotelName')
#                             dvsURL = request.POST.get('dvsUrl')
#                             dvsLocalIP = request.POST.get('dvsLocalIp')
#                             kongURL = request.POST.get('kongUrl')
#                             kongFqdn = request.POST.get('kongFqdn')
#                             kongLocalIP = request.POST.get('kongLocalIp')
#                             publicIP = request.POST.get('dvsPublicIp').replace(' ', '')
#                             macAddress = request.POST.get('dvsMacAddress')
#                             clientId = request.POST.get('dvcClientId')
#                             clientSecret = request.POST.get('dvcClientSecret')
#                             modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                            
#                             serverDB.update(hotelName=hotelName, dvsURL=dvsURL, dvsLocalIP=dvsLocalIP, kongURL=kongURL, kongFqdn=kongFqdn, kongLocalIP=kongLocalIP, publicIP=publicIP, macAddress=macAddress, clientId=clientId, clientSecret=clientSecret, modifiedOn=modifiedOn)
                            
#                             context['segment'] = 'addServer'
#                             context['status'] = True
#                             context['statusCode'] = serverUpdateStatus.get('statusCode')
#                             context['message'] = ", ".join([serverRegisterSuccess.get('message'), serverUpdateStatus.get('message')])
#                             context['data'] = None
                            
#                             logger.info(", ".join([serverRegisterSuccess.get('message'), serverUpdateStatus.get('message')]))
#                             html_template = loader.get_template('home/acknowledgement.html')
#                             return HttpResponse(html_template.render(context, request))

#                         except Exception as err:

#                             context['segment'] = 'addServer'
#                             context['status'] = False
#                             context['statusCode'] = serverDetailRequired.get('statusCode')
#                             context['message'] = ", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')])
#                             context['data'] = None

#                             logger.info(", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')]))
#                             logger.error(err)
#                             html_template = loader.get_template('home/acknowledgement.html')
#                             return HttpResponse(html_template.render(context, request))

#                     else:

#                         try:

#                             serverDB = serverRegister()
#                             serverDB.hotelName = request.POST.get('hotelName')
#                             serverDB.dvsURL = request.POST.get('dvsUrl')
#                             serverDB.dvsLocalIP = request.POST.get('dvsLocalIp')
#                             serverDB.kongURL = request.POST.get('kongUrl')
#                             serverDB.kongFqdn = request.POST.get('kongFqdn')
#                             serverDB.kongLocalIP = request.POST.get('kongLocalIp')
#                             serverDB.publicIP = request.POST.get('dvsPublicIp').replace(' ', '')
#                             serverDB.macAddress = request.POST.get('dvsMacAddress')
#                             serverDB.clientId = request.POST.get('dvcClientId')
#                             serverDB.clientSecret = request.POST.get('dvcClientSecret')
#                             serverDB.createdOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                             serverDB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                             serverDB.save()
                            
#                             context['segment'] = 'addServer'
#                             context['status'] = True
#                             context['statusCode'] = serverRegisterSuccess.get('statusCode')
#                             context['message'] = serverRegisterSuccess.get('message') 
#                             context['data'] = None
                            
#                             logger.info(serverRegisterSuccess.get('message'))
#                             html_template = loader.get_template('home/acknowledgement.html')
#                             return HttpResponse(html_template.render(context, request))

#                         except Exception as err:

#                             context['segment'] = 'addServer'
#                             context['status'] = False
#                             context['statusCode'] = serverDetailRequired.get('statusCode')
#                             context['message'] = ", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')])
#                             context['data'] = None
                            
#                             logger.info(", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')]))
#                             logger.error(err)
#                             html_template = loader.get_template('home/acknowledgement.html')
#                             return HttpResponse(html_template.render(context, request))

#                 except Exception as err:

#                     context['segment'] = 'addServer'
#                     context['status'] = False
#                     context['statusCode'] = DBError.get('statusCode')
#                     context['message'] = ", ".join([serverRegisterFailure.get('message'), DBError.get('message')])
#                     context['data'] = None
                    
#                     logger.info(", ".join([serverRegisterFailure.get('message'), DBError.get('message')]))
#                     logger.error(err)
#                     html_template = loader.get_template('home/acknowledgement.html')
#                     return HttpResponse(html_template.render(context, request))

#             else:

#                 html_template = loader.get_template('home/addServer.html')
#                 return HttpResponse(html_template.render(context, request))

#         else:
            
#             context['segment'] = 'addServer'
#             context['status'] = False
#             context['statusCode'] = unableServerRegisterStatus.get('statusCode')
#             context['message'] = unableServerRegisterStatus.get('message')
#             context['data'] = None
            
#             logger.info(unableServerRegisterStatus.get('message'))
#             html_template = loader.get_template('home/acknowledgement.html')
#             return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Server Register Section End ####



# #### Dashboard Server Detail Section Start ####
# @login_required(login_url="/login/")
# def serverDetail(request, macAddress):
#     context = dict()

#     try:
#         serverDB = serverRegister.objects.filter(macAddress = macAddress).values()

#         context['segment'] = 'server'
#         context['serverDB'] = serverDB
        
#         html_template = loader.get_template('home/serverDetail.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Server Detail Section End ####



# #### Dashboard Server Remove Section Start ####
# @login_required(login_url="/login/")
# def serverRemove(request, macAddress):
#     context = dict()

#     try:
#         if request.user.is_superuser:

#             try:
#                 serverDB = serverRegister.objects.filter(macAddress = macAddress)
#                 roomConfigDB = roomConfig.objects.filter(macAddress = macAddress)
#                 serverDB.delete()
#                 roomConfigDB.delete()
                
#                 context['segment'] = 'server'
#                 context['status'] = True
#                 context['statusCode'] = serverRemoveStatus.get('statusCode')
#                 context['message'] = serverRemoveStatus.get('message')
#                 context['data'] = None
                
#                 logger.info(serverRemoveStatus.get('message'))
#                 html_template = loader.get_template('home/acknowledgement.html')
#                 return HttpResponse(html_template.render(context, request))

#             except Exception as err:

#                 context['segment'] = 'server'
#                 context['status'] = False
#                 context['statusCode'] = DBError.get('statusCode')
#                 context['message'] = ", ".join([serverDeleteError.get('message'), DBError.get('message')])
#                 context['data'] = None
                
#                 logger.info(", ".join([serverDeleteError.get('message'), DBError.get('message')]))
#                 logger.error(err)
#                 html_template = loader.get_template('home/acknowledgement.html')
#                 return HttpResponse(html_template.render(context, request))

#         else:
    
#             context['segment'] = 'server'
#             context['status'] = False
#             context['statusCode'] = unableServerRemoveStatus.get('statusCode')
#             context['message'] = unableServerRemoveStatus.get('message')
#             context['data'] = None
            
#             logger.info(unableServerRemoveStatus.get('message'))
#             html_template = loader.get_template('home/acknowledgement.html')
#             return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Server Remove Section End ####



# #### Dashboard Server Update Section Start ####
# @login_required(login_url="/login/")
# def serverUpdate(request, macAddress):
#     context = dict()

#     try:
#         if request.user.is_superuser:

#             if request.method == 'POST':

#                     try:
#                         if serverRegister.objects.filter(macAddress = macAddress).exists():

#                             try:
#                                 serverDB = serverRegister.objects.filter(macAddress = macAddress)
                                
#                                 hotelName = request.POST.get('hotelName')
#                                 dvsURL = request.POST.get('dvsUrl')
#                                 dvsLocalIP = request.POST.get('dvsLocalIp')
#                                 kongURL = request.POST.get('kongUrl')
#                                 kongFqdn = request.POST.get('kongFqdn')
#                                 kongLocalIP = request.POST.get('kongLocalIp')
#                                 publicIP = request.POST.get('dvsPublicIp').replace(' ', '')
#                                 macAddress = request.POST.get('dvsMacAddress')
#                                 clientId = request.POST.get('dvcClientId')
#                                 clientSecret = request.POST.get('dvcClientSecret')
#                                 modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
                                
#                                 serverDB.update(hotelName=hotelName, dvsURL=dvsURL, dvsLocalIP=dvsLocalIP, kongURL=kongURL, kongFqdn=kongFqdn, kongLocalIP=kongLocalIP, publicIP=publicIP, macAddress=macAddress, clientId=clientId, clientSecret=clientSecret, modifiedOn=modifiedOn)
                                
#                                 context['segment'] = 'server'
#                                 context['status'] = True
#                                 context['statusCode'] = serverUpdateStatus.get('statusCode')
#                                 context['message'] = ", ".join([serverRegisterSuccess.get('message'), serverUpdateStatus.get('message')])
#                                 context['data'] = None
                                
#                                 logger.info(", ".join([serverRegisterSuccess.get('message'), serverUpdateStatus.get('message')]))
#                                 html_template = loader.get_template('home/acknowledgement.html')
#                                 return HttpResponse(html_template.render(context, request))

#                             except Exception as err:

#                                 context['segment'] = 'server'
#                                 context['status'] = False
#                                 context['statusCode'] = serverDetailRequired.get('statusCode')
#                                 context['message'] = ", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')])
#                                 context['data'] = None
                                
#                                 logger.info(", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')]))
#                                 logger.error(err)
#                                 html_template = loader.get_template('home/acknowledgement.html')
#                                 return HttpResponse(html_template.render(context, request))

#                     except Exception as err:
                        
#                         context['segment'] = 'server'
#                         context['status'] = False
#                         context['statusCode'] = DBError.get('statusCode')
#                         context['message'] = ", ".join([serverRegisterFailure.get('message'), DBError.get('message')])
#                         context['data'] = None
                        
#                         logger.info(", ".join([serverRegisterFailure.get('message'), DBError.get('message')]))
#                         logger.error(err)
#                         html_template = loader.get_template('home/acknowledgement.html')
#                         return HttpResponse(html_template.render(context, request))

#             serverDB = serverRegister.objects.filter(macAddress = macAddress).values()
#             context['segment'] = 'server'
#             context['serverDB'] = serverDB
#             html_template = loader.get_template('home/serverUpdate.html')
#             return HttpResponse(html_template.render(context, request))
        
#         else:
            
#             context['segment'] = 'server'
#             context['status'] = False
#             context['statusCode'] = unableServerUpdateStatus.get('statusCode')
#             context['message'] = unableServerUpdateStatus.get('message')
#             context['data'] = None
            
#             logger.info(unableServerUpdateStatus.get('message'))
#             html_template = loader.get_template('home/acknowledgement.html')
#             return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Server Update Section End ####



# #### Dashboard Room Mac Binding Information Section Start ####
# @login_required(login_url="/login/")
# def configFile(request, macAddress):
#     context = dict()

#     try:
#         roomConfigDB = roomConfig.objects.filter(macAddress = macAddress).values()

#         context['segment'] = 'server'
#         context['roomConfigDB'] = roomConfigDB

#         if roomConfig.objects.filter(macAddress = macAddress).exists():
#             context['config'] = json.loads(roomConfigDB.get()['config'].replace("'", '"'))

#         else:
#             context['log'] = "empty"

#         html_template = loader.get_template('home/configFile.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Room Mac Binding Information Section End ####



# #### Dashboard DVC Information Section Start ####
# @login_required(login_url="/login/")
# def dvcInfo(request, hotelName):
#     context = dict()

#     try:
#         DVCDB = DVC.objects.filter(hotelName = hotelName).values()

#         context['segment'] = 'server'

#         if DVC.objects.filter(hotelName = hotelName).exists():
#             context['DVCDB'] = DVCDB

#         else:
#             context['log'] = "empty"

#         html_template = loader.get_template('home/controller.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard DVC Information Section End ####



# #### Dashboard Unknown DVC Information Section Start ####
# @login_required(login_url="/login/")
# def unknownController(request):
#     context = dict()

#     try:
#         unknownDVCDB = unknownDVC.objects.values()

#         context['segment'] = 'unknownController'

#         if unknownDVC.objects.exists():
#             context['unknownDVCDB'] = unknownDVCDB

#         else:
#             context['log'] = "empty"

#         html_template = loader.get_template('home/unKnownController.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Unknown DVC Information Section End ####



# #### Dashboard Unknown Controller Remove Section Start ####
# @login_required(login_url="/login/")
# def unknownControllerRemove(request, macAddress):
#     context = dict()

#     try:
#         if request.user.is_superuser:

#             try:
#                 unknownDVCDB = unknownDVC.objects.filter(macAddress = macAddress)
#                 unknownDVCDB.delete()
                
#                 context['segment'] = 'unknownController'
#                 context['status'] = True
#                 context['statusCode'] = unknownDVCRemove.get('statusCode')
#                 context['message'] = unknownDVCRemove.get('message')
#                 context['data'] = None
                
#                 logger.info(unknownDVCRemove.get('message'))
#                 html_template = loader.get_template('home/acknowledgement.html')
#                 return HttpResponse(html_template.render(context, request))

#             except Exception as err:

#                 context['segment'] = 'unknownController'
#                 context['status'] = False
#                 context['statusCode'] = DBError.get('statusCode')
#                 context['message'] = ", ".join([unknownDVCError.get('message'), DBError.get('message')])
#                 context['data'] = None
                
#                 logger.info(", ".join([unknownDVCError.get('message'), DBError.get('message')]))
#                 logger.error(err)
#                 html_template = loader.get_template('home/acknowledgement.html')
#                 return HttpResponse(html_template.render(context, request))

#         else:
            
#             context['segment'] = 'unknownController'
#             context['status'] = False
#             context['statusCode'] = unableUnknownDVCRemove.get('statusCode')
#             context['message'] = unableUnknownDVCRemove.get('message')
#             context['data'] = None
            
#             logger.info(unableUnknownDVCRemove.get('message'))
#             html_template = loader.get_template('home/acknowledgement.html')
#             return HttpResponse(html_template.render(context, request))


#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Unknown Controller Remove Section End ####



# #### Dashboard Sys Log Section Start ####
# @login_required(login_url="/login/")
# def sysLog(request):
#     context = dict()

#     try:
#         sysLog = list()
#         with open('logs/info.log') as file:
#             for line in (file.readlines() [-20:]):
#                 sysLog.append(line)
         
#         context['segment'] = 'info'
#         context['sysLog'] = sysLog

#         html_template = loader.get_template('home/sysLog.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Sys Log Section End ####



# #### Dashboard Error Log Section Start ####
# @login_required(login_url="/login/")
# def errorLog(request):
#     context = dict()

#     try:
#         sysLog = list()
#         with open('logs/error.log') as file:
#             for line in (file.readlines() [-20:]):
#                 sysLog.append(line)
         
#         context['segment'] = 'error'
#         context['sysLog'] = sysLog

#         html_template = loader.get_template('home/sysLog.html')
#         return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Error Log Section End ####



# #### Dashboard Debug Log Section Start ####
# @login_required(login_url="/login/")
# def debugLog(request):
#     context = dict()

#     try:
#         if request.user.is_superuser:

#             sysLog = list()
#             with open('logs/debug.log') as file:
#                 for line in (file.readlines() [-20:]):
#                     sysLog.append(line)
            
#             context['segment'] = 'debug'
#             context['sysLog'] = sysLog

#             html_template = loader.get_template('home/sysLog.html')
#             return HttpResponse(html_template.render(context, request))
        
#         else:
            
#             context['segment'] = 'index'
#             context['status'] = False
#             context['statusCode'] = unableToAccessLog.get('statusCode')
#             context['message'] = unableToAccessLog.get('message')
#             context['data'] = None
            
#             logger.info(unableToAccessLog.get('message'))
#             html_template = loader.get_template('home/acknowledgement.html')
#             return HttpResponse(html_template.render(context, request))

#     except Exception as err:

#         html_template = loader.get_template('home/page-500.html')
#         logger.info(templateError.get('message'))
#         logger.error(err)
#         return HttpResponse(html_template.render(context, request))
# #### Dashboard Debug Log Section End ####



# #### GET ENVIRONMENT SECTION START ####
# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def getEnvironment(request):

#     if request.method == 'GET':

#         try:
#             if request.headers.get('deviceToken') == None:

#                 res['status'] = False
#                 res['statusCode'] = tokenNotPresent.get('statusCode')
#                 res['message'] = ", ".join([getEnvFailure.get('message'), tokenNotPresent.get('message')])
#                 res['data'] = None
                
#                 logger.info(", ".join([getEnvFailure.get('message'), tokenNotPresent.get('message')]))
#                 return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#             else:
#                 logger.debug(": ".join([requestGetEnv.get('message'), request.headers.get('deviceToken')]))

#                 if ValidationClass(request.headers.get('deviceToken')).tokenValidator():
#                     logger.debug(" : ".join([tokenSuccess.get('message'), request.headers.get('deviceToken')]))

#                     if request.GET.get("publicIp") is not None:

#                         try:
#                             if ValidationClass(request.GET.get("publicIp")).validIpAddressCheck():
#                                 logger.debug(" : ".join([ipAddressSuccess.get('message'), request.GET.get("publicIp")]))

#                                 try:
#                                     count = 0
#                                     envNames = dict()
#                                     responseData = dict()

#                                     for item in setEnvironment.objects.values_list('publicIP', 'envName'):

#                                         if [c for c in item[0].split(',') if c in request.GET.get("publicIp")]:

#                                             count = count + 1
#                                             envNames[f"NAME{count}"] = item[1]

#                                     if len(envNames) > 0:

#                                         if len(envNames) > 1:

#                                             res['status'] = False
#                                             res['statusCode'] = multipleEnvFound.get('statusCode')
#                                             res['message'] = multipleEnvFound.get('message')
#                                             res['data'] = None

#                                             logger.info(multipleEnvFound.get('message'))
#                                             return Response(res)
                                            
#                                         setEnvironmentData = setEnvironment.objects.filter(envName = envNames['NAME1']).values()

#                                         responseData['fqdn'] = setEnvironmentData.get().get('envFQDN')
#                                         responseData['url'] = f"https://{setEnvironmentData.get().get('envFQDN')}/cloud/api"
#                                         responseData['publicIp'] = request.GET.get("publicIp")
#                                         responseData['localIp'] = setEnvironmentData.get().get('localIP')

#                                         res['status'] = True
#                                         res['statusCode'] = getEnvSuccess.get('statusCode')
#                                         res['message'] = getEnvSuccess.get('message')
#                                         res['data'] = responseData

#                                         logger.info(getEnvSuccess.get('message'))
#                                         logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                         return Response(res)

#                                     responseData['fqdn'] = PROD_FQDN
#                                     responseData['url'] = f"https://{PROD_FQDN}/cloud/api"
#                                     responseData['publicIp'] = request.GET.get("publicIp")
#                                     responseData['localIp'] = None

#                                     res['status'] = True
#                                     res['statusCode'] = defaultEnv.get('statusCode')
#                                     res['message'] = defaultEnv.get('message')
#                                     res['data'] = responseData

#                                     logger.info(defaultEnv.get('message'))
#                                     logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                     return Response(res)

#                                 except Exception as err:

#                                     res['status'] = False
#                                     res['statusCode'] = DBError.get('statusCode')
#                                     res['message'] = ", ".join([getEnvFailure.get('message'), DBError.get('message')])
#                                     res['data'] = None
                                    
#                                     logger.info(", ".join([getEnvFailure.get('message'), DBError.get('message')]))
#                                     logger.error(err)
#                                     return Response(res)

#                             else:

#                                 res['status'] = False
#                                 res['statusCode'] = ipAddressInvalid.get('statusCode')
#                                 res['message'] = ", ".join([getEnvFailure.get('message'), ipAddressInvalid.get('message')])
#                                 res['data'] = None

#                                 logger.debug(": ".join([ipAddressInvalid.get('message'), request.GET.get("publicIp")]))
#                                 logger.info(", ".join([getEnvFailure.get('message'), ipAddressInvalid.get('message')]))
#                                 return Response(res, status = status.HTTP_401_UNAUTHORIZED)
                        
#                         except Exception as err:

#                             res['status'] = False
#                             res['statusCode'] = validationError.get('statusCode')
#                             res['message'] = ", ".join([getEnvFailure.get('message'), validationError.get('message')])
#                             res['data'] = None

#                             logger.info(", ".join([getEnvFailure.get('message'), validationError.get('message')]))
#                             logger.error(err)
#                             return Response(res)
                    
#                     else:

#                         res['status'] = False
#                         res['statusCode'] = requestQueryParam.get('statusCode')
#                         res['message'] = ", ".join([getEnvFailure.get('message'), requestQueryParam.get('message')])
#                         res['data'] = None
                        
#                         logger.info(", ".join([getEnvFailure.get('message'), requestQueryParam.get('message')]))
#                         return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                 else:
                    
#                     res['status'] = False
#                     res['statusCode'] = tokenFailure.get('statusCode')
#                     res['message'] = ", ".join([getEnvFailure.get('message'), tokenFailure.get('message')])
#                     res['data'] = None
                    
#                     logger.info(", ".join([getEnvFailure.get('message'), tokenFailure.get('message')]))
#                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#         except Exception as err:
            
#             res['status'] = False
#             res['statusCode'] = getEnvFailure.get('statusCode')
#             res['message'] = getEnvFailure.get('message')
#             res['data'] = None
            
#             logger.info(getEnvFailure.get('message'))
#             logger.error(err)
#             return Response(res)

#     else:

#         res['status'] = False
#         res['statusCode'] = requestInvalid.get('statusCode')
#         res['message'] = requestInvalid.get('message')
#         res['data'] = None
        
#         logger.info(requestInvalid.get('message'))
#         return Response(res)
# #### GET ENVIRONMENT SECTION END ####



# #### PUBLIC KEY SECTION START ####
# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def getPublicKey(request):

#     if request.method == 'GET':

#         try:
#             if request.headers.get('deviceToken') == None:

#                 res['status'] = False
#                 res['statusCode'] = tokenNotPresent.get('statusCode')
#                 res['message'] = ", ".join([publicKeyFailure.get('message'), tokenNotPresent.get('message')])
#                 res['data'] = None
                
#                 logger.info(", ".join([publicKeyFailure.get('message'), tokenNotPresent.get('message')]))
#                 return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#             else:
#                 logger.debug(" : ".join([requestPublicKey.get('message'), request.headers.get('deviceToken')]))

#                 if ValidationClass(request.headers.get('deviceToken')).tokenValidator():

#                     logger.debug(" : ".join([tokenSuccess.get('message'), request.headers.get('deviceToken')]))

#                     res['status'] = True
#                     res['statusCode'] = publicKeySuccess.get('statusCode')
#                     res['message'] = publicKeySuccess.get('message')
#                     res['data'] = (open('certificates/apc_publickey_rsakey.pem', 'rb').read()).decode('utf-8').replace("\n", "")

#                     logger.info(publicKeySuccess.get('message'))
#                     logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                     return Response(res)

#                 else:
                    
#                     res['status'] = False
#                     res['statusCode'] = tokenFailure.get('statusCode')
#                     res['message'] = ", ".join([publicKeyFailure.get('message'), tokenFailure.get('message')])
#                     res['data'] = None
                    
#                     logger.info(", ".join([publicKeyFailure.get('message'), tokenFailure.get('message')]))
#                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#         except Exception as err:
            
#             res['status'] = False
#             res['statusCode'] = publicKeyFailure.get('statusCode')
#             res['message'] = publicKeyFailure.get('message')
#             res['data'] = None
            
#             logger.info(publicKeyFailure.get('message'))
#             logger.error(err)
#             return Response(res)

#     else:

#         res['status'] = False
#         res['statusCode'] = requestInvalid.get('statusCode')
#         res['message'] = requestInvalid.get('message')
#         res['data'] = None
        
#         logger.info(requestInvalid.get('message'))
#         return Response(res)
# #### PUBLIC KEY SECTION END ####



# #### SESSION KEY SECTION START ####
# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def key(request):

#     if request.method == 'POST':

#         try:
#             if request.body != b'':

#                 if request.headers.get('deviceToken') == None:
                    
#                     res['status'] = False
#                     res['statusCode'] = tokenNotPresent.get('statusCode')
#                     res['message'] = ", ".join([sessionKeyFailure.get('message'), tokenNotPresent.get('message')])
#                     res['data'] = None
                    
#                     logger.info(", ".join([sessionKeyFailure.get('message'), tokenNotPresent.get('message')]))
#                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                 else:
#                     logger.debug(" : ".join([requestSessionKey.get('message'), request.headers.get('deviceToken')]))

#                     if ValidationClass(request.headers.get('deviceToken')).tokenValidator():

#                         keyInfoJson = json.loads(request.body.decode("utf-8"))

#                         logger.debug(" : ".join([tokenSuccess.get('message'), request.headers.get('deviceToken')]))
#                         logger.debug(" : ".join([requestBodyData.get('message'), str(keyInfoJson)]))

#                         if ValidationClass(keyInfoJson.get('macAddress')).validMacAddress():

#                             logger.debug(" : ".join([macAddressSuccess.get('message'), keyInfoJson.get('macAddress')]))

#                             if sessionKey.objects.filter(macAddress = (keyInfoJson.get('macAddress'))).exists():

#                                 try:
#                                     decryptSessionKey = decryptCrtRex(keyInfoJson.get('sessionKey')).strip()
#                                     logger.debug(sessionKeyDecrypt.get('message')+decryptSessionKey)

#                                     try:
#                                         sessionKeyDB = sessionKey.objects.filter(macAddress = (keyInfoJson.get('macAddress')))
#                                         token = request.headers.get('deviceToken')
#                                         sessionKeyVal = decryptSessionKey
#                                         modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                         sessionKeyDB.update(token=token, sessionKeyVal=sessionKeyVal, modifiedOn=modifiedOn)
                                        
#                                         res['status'] = True
#                                         res['statusCode'] = sessionKeyUpdated.get('statusCode')
#                                         res['message'] = ", ".join([sessionKeySuccess.get('message'), sessionKeyUpdated.get('message')])
#                                         res['data'] = None
                                        
#                                         logger.info(", ".join([sessionKeySuccess.get('message'), sessionKeyUpdated.get('message')]))
#                                         logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                         return Response(res)

#                                     except Exception as err:

#                                         res['status'] = False
#                                         res['statusCode'] = sessionKeyNotUpdated.get('statusCode')
#                                         res['message'] = ", ".join([sessionKeyFailure.get('message'), sessionKeyNotUpdated.get('message')])
#                                         res['data'] = None
                                        
#                                         logger.info(", ".join([sessionKeyFailure.get('message'), sessionKeyNotUpdated.get('message')]))
#                                         logger.error(err)
#                                         return Response(res)

#                                 except Exception as err:

#                                     res['status'] = False
#                                     res['statusCode'] = NotDecrypt.get('statusCode')
#                                     res['message'] = ", ".join([sessionKeyFailure.get('message'), NotDecrypt.get('message')])
#                                     res['data'] = None
                                    
#                                     logger.info(", ".join([sessionKeyFailure.get('message'), NotDecrypt.get('message')]))
#                                     logger.error(err)
#                                     return Response(res)
#                             else:

#                                 try:
#                                     decryptSessionKey = decryptCrtRex(keyInfoJson.get('sessionKey')).strip()
#                                     logger.debug(sessionKeyDecrypt.get('message')+decryptSessionKey)

#                                     try:
#                                         sessionKeyDB = sessionKey()

#                                         sessionKeyDB.token = request.headers.get('deviceToken')
#                                         sessionKeyDB.sessionKeyVal = decryptSessionKey
#                                         sessionKeyDB.macAddress = keyInfoJson.get('macAddress')
#                                         sessionKeyDB.createdOn=(datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                         sessionKeyDB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                         sessionKeyDB.save()
                                        
#                                         res['status'] = True
#                                         res['statusCode'] = sessionKeySuccess.get('statusCode')
#                                         res['message'] = sessionKeySuccess.get('message')
#                                         res['data'] = None
                                    
#                                         logger.info(sessionKeySuccess.get('message'))
#                                         logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                         return Response(res)

#                                     except Exception as err:

#                                         res['status'] = False
#                                         res['statusCode'] = sessionKeyNotSave.get('statusCode')
#                                         res['message'] = ", ".join([sessionKeyFailure.get('message'), sessionKeyNotSave.get('message')])
#                                         res['data'] = None
                                        
#                                         logger.info(", ".join([sessionKeyFailure.get('message'), sessionKeyNotSave.get('message')]))
#                                         logger.error(err)
#                                         return Response(res)

#                                 except Exception as err:

#                                     res['status'] = False
#                                     res['statusCode'] = NotDecrypt.get('statusCode')
#                                     res['message'] = ", ".join([sessionKeyFailure.get('message'), NotDecrypt.get('message')])
#                                     res['data'] = None
                                    
#                                     logger.info(", ".join([sessionKeyFailure.get('message'), NotDecrypt.get('message')]))
#                                     logger.error(err)
#                                     return Response(res)

#                         else:

#                             res['status'] = False
#                             res['statusCode'] = macAddressInvalid.get('statusCode')
#                             res['message'] = ", ".join([sessionKeyFailure.get('message'), macAddressInvalid.get('message')])
#                             res['data'] = None

#                             logger.info(", ".join([sessionKeyFailure.get('message'), macAddressInvalid.get('message')]))
#                             return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                     else:

#                         res['status'] = False
#                         res['statusCode'] = tokenFailure.get('statusCode')
#                         res['message'] = ", ".join([sessionKeyFailure.get('message'), tokenFailure.get('message')])
#                         res['data'] = None
                        
#                         logger.info(", ".join([sessionKeyFailure.get('message'), tokenFailure.get('message')]))
#                         return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#             else:

#                 res['status'] = False
#                 res['statusCode'] = requestBody.get('statusCode')
#                 res['message'] = ", ".join([sessionKeyFailure.get('message'), requestBody.get('message')])
#                 res['data'] = None
                
#                 logger.info(", ".join([sessionKeyFailure.get('message'), requestBody.get('message')]))
#                 return Response(res)
        
#         except Exception as err:

#             res['status'] = False
#             res['statusCode'] = sessionKeyError.get('statusCode')
#             res['message'] = sessionKeyError.get('message')
#             res['data'] = None
            
#             logger.info(sessionKeyError.get('message'))
#             logger.error(err)
#             return Response(res)

#     else:

#         res['status'] = False
#         res['statusCode'] = requestInvalid.get('statusCode')
#         res['message'] = requestInvalid.get('message')
#         res['data'] = None
        
#         logger.info(requestInvalid.get('message'))
#         return Response(res)
# #### SESSION KEY SECTION END ####



# #### SERVER REGISTER SECTION START ####
# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def server(request):

#     if request.method == 'POST':

#         try:
#             if request.body != b'':
#                 serverInfo = request.body

#                 if request.headers.get('macAddress') == None:

#                     res['status'] = False
#                     res['statusCode'] = macAddressPresent.get('statusCode')
#                     res['message'] = ", ".join([serverRegisterFailure.get('message'), macAddressPresent.get('message')])
#                     res['data'] = None
                    
#                     logger.info(", ".join([serverRegisterFailure.get('message'), macAddressPresent.get('message')]))
#                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                 else:

#                     logger.debug(" : ".join([requestServerRegister.get('message'), request.headers.get('macAddress')]))

#                     if ValidationClass(request.headers.get('macAddress')).validMacAddress():

#                         logger.debug(" : ".join([macAddressSuccess.get('message'), request.headers.get('macAddress')]))

#                         if not sessionKey.objects.filter(macAddress = (request.headers.get('macAddress'))).exists():

#                             res['status'] = False
#                             res['statusCode'] = sessionKeyNotExists.get('statusCode')
#                             res['message'] = ", ".join([serverRegisterFailure.get('message'), sessionKeyNotExists.get('message')])
#                             res['data'] = None
                            
#                             logger.info(", ".join([serverRegisterFailure.get('message'), sessionKeyNotExists.get('message')]))
#                             return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                         else:

#                             try:
#                                 key = sessionKey.objects.get(macAddress = (request.headers.get('macAddress'))).sessionKeyVal
#                                 logger.debug(sessionKeyData.get('message')+str(key))

#                                 data = json.loads(decryptionRex(key, serverInfo.decode("utf-8")))
#                                 logger.debug(serverDecrypt.get('message')+str(data))

#                                 try:
#                                     if ValidationClass(data.get('dvsPublicIp')).validIpAddressCheck() and ValidationClass(data.get('dvsPublicIp')).validIpAddressCheck():
#                                         logger.debug(" : ".join([ipAddressSuccess.get('message'), data.get('dvsPublicIp')]))
#                                         logger.debug(" : ".join([ipAddressSuccess.get('message'), data.get('dvsLocalIp')]))
                                    
#                                         if serverRegister.objects.filter(Q(macAddress = data.get('macAddress')) | Q(dvsURL = data.get('dvsUrl')) | Q(kongURL=data.get('kongUrl')) | Q(kongFqdn=data.get('kongFqdn'))).exists():
                                            
#                                             try:
#                                                 serverDB = serverRegister.objects.filter(Q(macAddress = data.get('macAddress')) | Q(dvsURL = data.get('dvsUrl')) | Q(kongURL=data.get('kongUrl')) | Q(kongFqdn=data.get('kongFqdn')))
                                                
#                                                 serverPublicIp = serverRegister.objects.get(Q(macAddress = data.get('macAddress')) | Q(dvsURL = data.get('dvsUrl')) | Q(kongURL=data.get('kongUrl')) | Q(kongFqdn=data.get('kongFqdn'))).publicIP

#                                                 publicIpSet = set(serverPublicIp.split(","))
#                                                 publicIpSet.add(data.get('dvsPublicIp'))
#                                                 updatePublicIp = ', '.join(publicIpSet).replace(" ", "")
                                                
#                                                 hotelName = data.get('hotelName')
#                                                 dvsURL = data.get('dvsUrl')
#                                                 dvsLocalIP = data.get('dvsLocalIp')
#                                                 kongURL = data.get('kongUrl')
#                                                 kongFqdn = data.get('kongFqdn')
#                                                 kongLocalIP = data.get('kongLocalIp')
#                                                 publicIP = updatePublicIp
#                                                 macAddress = data.get('dvsMacAddress')
#                                                 clientId = data.get('dvcClientId')
#                                                 clientSecret = data.get('dvcClientSecret')
#                                                 modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))

#                                                 serverDB.update(hotelName=hotelName, dvsURL=dvsURL, dvsLocalIP=dvsLocalIP, kongURL=kongURL, kongFqdn=kongFqdn, kongLocalIP=kongLocalIP, publicIP=publicIP, macAddress=macAddress, clientId=clientId, clientSecret=clientSecret, modifiedOn=modifiedOn)
                                                
#                                                 res['status'] = True
#                                                 res['statusCode'] = serverUpdateStatus.get('statusCode')
#                                                 res['message'] = ", ".join([serverRegisterSuccess.get('message'), serverUpdateStatus.get('message')])
#                                                 res['data'] = None
                                                
#                                                 logger.info(", ".join([serverRegisterSuccess.get('message'), serverUpdateStatus.get('message')]))
#                                                 logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                                 return Response(res)

#                                             except Exception as err:

#                                                 res['status'] = False
#                                                 res['statusCode'] = serverDetailRequired.get('statusCode')
#                                                 res['message'] = ", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')])
#                                                 res['data'] = None
                                                
#                                                 logger.info(", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')]))
#                                                 logger.error(err)
#                                                 return Response(res)

#                                         else:

#                                             try:
#                                                 serverDB = serverRegister()

#                                                 serverDB.hotelName = data.get('hotelName')
#                                                 serverDB.dvsURL = data.get('dvsUrl')
#                                                 serverDB.dvsLocalIP = data.get('dvsLocalIp')
#                                                 serverDB.kongURL = data.get('kongUrl')
#                                                 serverDB.kongFqdn = data.get('kongFqdn')
#                                                 serverDB.kongLocalIP = data.get('kongLocalIp')
#                                                 serverDB.publicIP = data.get('dvsPublicIp')
#                                                 serverDB.macAddress = data.get('dvsMacAddress')
#                                                 serverDB.clientId = data.get('dvcClientId')
#                                                 serverDB.clientSecret = data.get('dvcClientSecret')
#                                                 serverDB.createdOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                 serverDB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                 serverDB.save()
                                                
#                                                 res['status'] = True
#                                                 res['statusCode'] = serverRegisterSuccess.get('statusCode')
#                                                 res['message'] = serverRegisterSuccess.get('message') 
#                                                 res['data'] = None

#                                                 logger.info(serverRegisterSuccess.get('message'))
#                                                 logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                                 return Response(res)

#                                             except Exception as err:

#                                                 res['status'] = False
#                                                 res['statusCode'] = serverDetailRequired.get('statusCode')
#                                                 res['message'] = ", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')])
#                                                 res['data'] = None
                                                
#                                                 logger.info(", ".join([serverRegisterFailure.get('message'), serverDetailRequired.get('message')]))
#                                                 logger.error(err)
#                                                 return Response(res)

#                                     else:
                                        
#                                         res['status'] = False
#                                         res['statusCode'] = ipAddressInvalid.get('statusCode')
#                                         res['message'] = ", ".join([serverRegisterFailure.get('message'), ipAddressInvalid.get('message')])
#                                         res['data'] = None

#                                         logger.info(", ".join([serverRegisterFailure.get('message'), ipAddressInvalid.get('message')]))
#                                         return Response(res, status = status.HTTP_401_UNAUTHORIZED)
                               
#                                 except Exception as err:

#                                     res['status'] = False
#                                     res['statusCode'] = DBError.get('statusCode')
#                                     res['message'] = ", ".join([serverRegisterFailure.get('message'), DBError.get('message')])
#                                     res['data'] = None
                                    
#                                     logger.info(", ".join([serverRegisterFailure.get('message'), DBError.get('message')]))
#                                     logger.error(err)
#                                     return Response(res)

#                             except Exception as err:

#                                 res['status'] = False
#                                 res['statusCode'] = NotDecrypt.get('statusCode')
#                                 res['message'] = ", ".join([serverRegisterFailure.get('message'), NotDecrypt.get('message')])
#                                 res['data'] = None
                               
#                                 logger.info(", ".join([serverRegisterFailure.get('message'), NotDecrypt.get('message')]))
#                                 logger.error(err)
#                                 return Response(res)

#                     else:
                        
#                         res['status'] = False
#                         res['statusCode'] = macAddressInvalid.get('statusCode')
#                         res['message'] = ", ".join([serverRegisterFailure.get('message'), macAddressInvalid.get('message')])
#                         res['data'] = None

#                         logger.info(", ".join([serverRegisterFailure.get('message'), macAddressInvalid.get('message')]))
#                         return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#             else:

#                 res['status'] = False
#                 res['statusCode'] = requestBody.get('statusCode')
#                 res['message'] = ", ".join([serverRegisterFailure.get('message'), requestBody.get('message')])
#                 res['data'] = None
                
#                 logger.info(", ".join([serverRegisterFailure.get('message'), requestBody.get('message')]))
#                 return Response(res)

#         except Exception as err:

#             res['status'] = False
#             res['statusCode'] = serverRegisterError.get('statusCode')
#             res['message'] = serverRegisterError.get('message')
#             res['data'] = None
           
#             logger.info(serverRegisterError)
#             logger.error(err)
#             return Response(res)

#     else:

#         res['status'] = False
#         res['statusCode'] = requestInvalid.get('statusCode')
#         res['message'] = requestInvalid.get('message')
#         res['data'] = None

#         logger.info(requestInvalid.get('message'))
#         return Response(res)
# #### SERVER REGISTER SECTION END ####



# #### CONFIGURATION FILE SECTION START ####
# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def config(request):

#     if request.method == 'POST':

#         try:
#             if request.body != b'':
#                 configInfo = request.body

#                 if request.headers.get('macAddress') == None:

#                     res['status'] = False
#                     res['statusCode'] = macAddressPresent.get('statusCode')
#                     res['message'] = ", ".join([configFileFailure.get('message'), macAddressPresent.get('message')])
#                     res['data'] = None
                    
#                     logger.info(", ".join([configFileFailure.get('message'), macAddressPresent.get('message')]))
#                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                 else:

#                     try:
#                         logger.debug(requestConfigFile.get('message')+request.headers.get('macAddress'))

#                         if ValidationClass(request.headers.get('macAddress')).validMacAddress():

#                             logger.debug(" : ".join([macAddressSuccess.get('message'), request.headers.get('macAddress')]))

#                             if not sessionKey.objects.filter(macAddress = (request.headers.get('macAddress'))).exists():

#                                 res['status'] = False
#                                 res['statusCode'] = sessionKeyNotExists.get('statusCode')
#                                 res['message'] = ", ".join([configFileFailure.get('message'), sessionKeyNotExists.get('message')])
#                                 res['data'] = None
                               
#                                 logger.info(", ".join([configFileFailure.get('message'), sessionKeyNotExists.get('message')]))
#                                 return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                             else:

#                                 if not serverRegister.objects.filter(macAddress = (request.headers.get('macAddress'))).exists():

#                                     res['status'] = False
#                                     res['statusCode'] = configFileServerNotPresent.get('statusCode')
#                                     res['message'] = ", ".join([configFileFailure.get('message'), configFileServerNotPresent.get('message')])
#                                     res['data'] = None
                                    
#                                     logger.info(", ".join([configFileFailure.get('message'), configFileServerNotPresent.get('message')]))
#                                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                                 else:

#                                     try:
#                                         key = sessionKey.objects.get(macAddress = (request.headers.get('macAddress'))).sessionKeyVal
#                                         # logger.debug(sessionKeyData.get('message')+str(key))

#                                         data = json.loads(decryptionRex(key, configInfo.decode("utf-8")))
#                                         logger.debug(configFileDecrypt.get('message')+str(data))

#                                         try:
#                                             if roomConfig.objects.filter(macAddress = (request.headers.get('macAddress'))).exists():
#                                                 """UPDATE"""

#                                                 roomConfigDB = roomConfig.objects.filter(macAddress = (request.headers.get('macAddress')))
#                                                 modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                 roomConfigDB.update(config = data, modifiedOn = modifiedOn)
                                               
#                                                 res['status'] = True
#                                                 res['statusCode'] = configFileUpdate.get('statusCode')
#                                                 res['message'] = ", ".join([configFileSuccess.get('message'), configFileUpdate.get('message')])
#                                                 res['data'] = None
                                                
#                                                 logger.info(configFileSuccess.get('message'))
#                                                 logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                                 return Response(res) 

#                                             else:
#                                                 """INSERT"""

#                                                 roomConfigDB = roomConfig()
#                                                 roomConfigDB.hotelName = serverRegister.objects.get(macAddress = (request.headers.get('macAddress'))).hotelName
#                                                 roomConfigDB.macAddress = request.headers.get('macAddress')
#                                                 roomConfigDB.config = data
#                                                 roomConfigDB.createdOn=(datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                 roomConfigDB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                 roomConfigDB.save()

#                                                 res['status'] = True
#                                                 res['statusCode'] = configFileSuccess.get('statusCode')
#                                                 res['message'] = configFileSuccess.get('message')
#                                                 res['data'] = None

#                                                 logger.info(configFileSuccess.get('message')) 
#                                                 logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))      
#                                                 return Response(res)

#                                         except Exception as err:

#                                             res['status'] = False
#                                             res['statusCode'] = DBError.get('statusCode')
#                                             res['message'] = ", ".join([configFileFailure.get('message'), DBError.get('message')])
#                                             res['data'] = None

#                                             logger.info(", ".join([configFileFailure.get('message'), DBError.get('message')]))
#                                             logger.error(err)
#                                             return Response(res)

#                                     except Exception as err:

#                                         res['status'] = False
#                                         res['statusCode'] = NotDecrypt.get('statusCode')
#                                         res['message'] = ", ".join([configFileFailure.get('message'), NotDecrypt.get('message')])
#                                         res['data'] = None

#                                         logger.info(", ".join([configFileFailure.get('message'), NotDecrypt.get('message')]))
#                                         logger.error(err)
#                                         return Response(res)

#                         else:

#                             res['status'] = False
#                             res['statusCode'] = macAddressInvalid.get('statusCode')
#                             res['message'] = ", ".join([configFileFailure.get('message'), macAddressInvalid.get('message')])
#                             res['data'] = None

#                             logger.info(", ".join([configFileFailure.get('message'), macAddressInvalid.get('message')]))
#                             return Response(res)

#                     except Exception as err:

#                         res['status'] = False
#                         res['statusCode'] = validationError.get('statusCode')
#                         res['message'] = ", ".join([configFileFailure.get('message'), validationError.get('message')])
#                         res['data'] = None

#                         logger.info(", ".join([configFileFailure.get('message'), validationError.get('message')]))
#                         logger.error(err)
#                         return Response(res)

#             else:

#                 res['status'] = False
#                 res['statusCode'] = requestBody.get('statusCode')
#                 res['message'] = ", ".join([configFileFailure.get('message'), requestBody.get('message')])
#                 res['data'] = None

#                 logger.info(", ".join([configFileFailure.get('message'), requestBody.get('message')]))
#                 return Response(res)

#         except Exception as err:

#             res['status'] = False
#             res['statusCode'] = configFileError.get('statusCode')
#             res['message'] = configFileError.get('message')
#             res['data'] = None

#             logger.info(configFileError)
#             logger.error(err)
#             return Response(res)

#     else:

#         res['status'] = False
#         res['statusCode'] = requestInvalid.get('statusCode')
#         res['message'] = requestInvalid.get('message')
#         res['data'] = None

#         logger.info(requestInvalid.get('message'))
#         return Response(res)
# #### CONFIGURATION FILE SECTION END ####



# #### DVC REGISTER SECTION START ####
# @api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# def dvc(request):

#     if request.method == 'POST':

#         try:
#             resp = dict()
#             servers = dict()

#             if request.body != b'':
#                 DVCInfo = request.body

#                 if request.headers.get('macAddress') == None:

#                     res['status'] = False
#                     res['statusCode'] = macAddressPresent.get('statusCode')
#                     res['message'] = ", ".join([serverDetailFailure.get('message'), macAddressPresent.get('message')])
#                     res['data'] = None

#                     logger.info(", ".join([serverDetailFailure.get('message'), macAddressPresent.get('message')]))
#                     return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                 else:
#                     logger.debug(" : ".join([requestServerDetail.get('message'), request.headers.get('macAddress')]))

#                     if ValidationClass(request.headers.get('macAddress')).validMacAddress():

#                         logger.debug(" : ".join([macAddressSuccess.get('message'), request.headers.get('macAddress')]))

#                         try:
#                             key = sessionKey.objects.get(macAddress = (request.headers.get('macAddress'))).sessionKeyVal
#                             # logger.debug(sessionKeyData.get('message')+str(key))

#                             try:
#                                 data = json.loads(decryptionRex(key, DVCInfo.decode("utf-8")))
#                                 logger.debug(requestDecrypt.get('message')+str(data))

#                                 try:
#                                     if ValidationClass(data.get('publicIp')).validIpAddressCheck() and ValidationClass(data.get('localIp')).validIpAddressCheck():
#                                         logger.debug(" : ".join([ipAddressSuccess.get('message'), data.get('publicIp')]))
#                                         logger.debug(" : ".join([ipAddressSuccess.get('message'), data.get('localIp')]))

#                                         try:
#                                             if serverFinder(request.headers.get('macAddress')) is not None:
                                                
#                                                 if serverRegister.objects.filter(macAddress = (serverFinder(request.headers.get('macAddress')))).exists():

#                                                     serverDB = serverRegister.objects.filter(macAddress = (serverFinder(request.headers.get('macAddress')))).values()
                                                    
#                                                     dvs = dict()
#                                                     dvs['url'] = serverDB.get().get('dvsURL')
#                                                     dvs['publicIp'] = serverDB.get().get('publicIP')
#                                                     dvs['localIp'] = serverDB.get().get('dvsLocalIP')
#                                                     servers['dvs']= dvs
                                                    
#                                                     kong = dict()
#                                                     kong['fqdn'] = serverDB.get().get('kongFqdn')
#                                                     kong['url'] = serverDB.get().get('kongURL')
#                                                     kong['localIp'] = serverDB.get().get('kongLocalIP')
#                                                     kong['clientId'] = serverDB.get().get('clientId')
#                                                     kong['clientSecret'] = serverDB.get().get('clientSecret')
#                                                     servers['kong'] = kong
                                                    
#                                                     resp['servers'] = servers
#                                                     serverData = json.dumps(resp)

#                                                     logger.debug("Server Data :"+str(serverData))

#                                                     try:
#                                                         resp = encryptionRex(key, serverData)
#                                                         logger.debug(responseEncrypt.get('message')+str(resp))

#                                                         try:
#                                                             if unknownDVC.objects.filter(macAddress = request.headers.get('macAddress')).exists():

#                                                                 unknownDVCDB = unknownDVC.objects.filter(macAddress = request.headers.get('macAddress'))
#                                                                 unknownDVCDB.delete()
                                                                
#                                                             if not DVC.objects.filter(macAddress = request.headers.get('macAddress')).exists():

#                                                                 DVC_DB = DVC()
#                                                                 DVC_DB.hotelName = serverDB.get().get('hotelName')
#                                                                 DVC_DB.publicIp = data.get('publicIp')
#                                                                 DVC_DB.localIp = data.get('localIp')
#                                                                 DVC_DB.macAddress = request.headers.get('macAddress')
#                                                                 DVC_DB.createdOn=(datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                                 DVC_DB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                                 DVC_DB.save()
                                                            
#                                                             else:
                                                                
#                                                                 DVC_DB = DVC.objects.filter(macAddress = request.headers.get('macAddress'))
#                                                                 hotelName = serverDB.get().get('hotelName')
#                                                                 publicIp = data.get('publicIp')
#                                                                 localIp = data.get('localIp')
#                                                                 macAddress = request.headers.get('macAddress')
#                                                                 modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                                 DVC_DB.update(hotelName=hotelName, publicIp=publicIp, localIp=localIp, macAddress=macAddress, modifiedOn=modifiedOn)

#                                                             res['status'] = True
#                                                             res['statusCode'] = serverDetailSuccess.get('statusCode')
#                                                             res['message'] = serverDetailSuccess.get('message')
#                                                             res['data'] = resp

#                                                             logger.info(serverDetailSuccess.get('message'))
#                                                             logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                                             return Response(res)

#                                                         except Exception as err:

#                                                             res['status'] = False
#                                                             res['statusCode'] = DBError.get('statusCode')
#                                                             res['message'] = ", ".join([serverDetailFailure.get('message'), DBError.get('message')])
#                                                             res['data'] = None
                                                            
#                                                             logger.info(", ".join([serverDetailFailure.get('message'), DBError.get('message')]))
#                                                             logger.error(err)
#                                                             return Response(res)

#                                                     except Exception as err:

#                                                         res['status'] = False
#                                                         res['statusCode'] = NotEncrypt.get('statusCode')
#                                                         res['message'] = ", ".join([serverDetailFailure.get('message'), NotEncrypt.get('message')])
#                                                         res['data'] = None

#                                                         logger.info(", ".join([serverDetailFailure.get('message'), NotEncrypt.get('message')]))
#                                                         logger.error(err)
#                                                         return Response(res)

#                                                 else:

#                                                     res['status'] = False
#                                                     res['statusCode'] = serverDetailNotExists.get('statusCode')
#                                                     res['message'] = ", ".join([serverDetailFailure.get('message'), serverDetailNotExists.get('message')])
#                                                     res['data'] = None

#                                                     logger.info(", ".join([serverDetailFailure.get('message'), serverDetailNotExists.get('message')]))
#                                                     return Response(res)

#                                             else:
#                                                 count = 0
#                                                 macAddressData = dict()

#                                                 for item in serverRegister.objects.values_list('publicIP', 'macAddress'):

#                                                     if [c for c in item[0].split(',') if c in data.get('publicIp')]:

#                                                         count = count + 1
#                                                         macAddressData[f"MAC{count}"] = item[1]

#                                                 if len(macAddressData) > 0:

#                                                     if len(macAddressData) > 1:

#                                                         res['status'] = False
#                                                         res['statusCode'] = multipleServerFound.get('statusCode')
#                                                         res['message'] = multipleServerFound.get('message')
#                                                         res['data'] = None

#                                                         logger.info(multipleServerFound.get('message'))
#                                                         return Response(res)

#                                                     serverDB = serverRegister.objects.filter(macAddress = macAddressData['MAC1']).values()
                                                    
#                                                     dvs = dict()
#                                                     dvs['url'] = serverDB.get().get('dvsURL')
#                                                     dvs['publicIp'] = serverDB.get().get('publicIP')
#                                                     dvs['localIp'] = serverDB.get().get('dvsLocalIP')
#                                                     servers['dvs']= dvs
                                                    
#                                                     kong = dict()
#                                                     kong['fqdn'] = serverDB.get().get('kongFqdn')
#                                                     kong['url'] = serverDB.get().get('kongURL')
#                                                     kong['localIp'] = serverDB.get().get('kongLocalIP')
#                                                     kong['clientId'] = serverDB.get().get('clientId')
#                                                     kong['clientSecret'] = serverDB.get().get('clientSecret')
#                                                     servers['kong'] = kong
                                                    
#                                                     resp['servers'] = servers
#                                                     serverData = json.dumps(resp)

#                                                     try:
#                                                         resp = encryptionRex(key, serverData)
#                                                         logger.debug(responseEncrypt.get('message')+str(resp))

#                                                         try:
#                                                             if unknownDVC.objects.filter(macAddress = request.headers.get('macAddress')).exists():

#                                                                 unknownDVCDB = unknownDVC.objects.filter(macAddress = request.headers.get('macAddress'))
#                                                                 unknownDVCDB.delete()

#                                                             if not DVC.objects.filter(macAddress = request.headers.get('macAddress')).exists():

#                                                                 DVC_DB = DVC()
#                                                                 DVC_DB.hotelName = serverDB.get().get('hotelName')
#                                                                 DVC_DB.publicIp = data.get('publicIp')
#                                                                 DVC_DB.localIp = data.get('localIp')
#                                                                 DVC_DB.macAddress = request.headers.get('macAddress')
#                                                                 DVC_DB.createdOn=(datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                                 DVC_DB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                                 DVC_DB.save()

#                                                             else:

#                                                                 DVC_DB = DVC.objects.filter(macAddress = request.headers.get('macAddress'))
#                                                                 hotelName = serverDB.get().get('hotelName')
#                                                                 publicIp = data.get('publicIp')
#                                                                 localIp = data.get('localIp')
#                                                                 macAddress = request.headers.get('macAddress')
#                                                                 modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                                 DVC_DB.update(hotelName=hotelName, publicIp=publicIp, localIp=localIp, macAddress=macAddress, modifiedOn=modifiedOn)

#                                                             res['status'] = True
#                                                             res['statusCode'] = serverDetailSuccess.get('statusCode')
#                                                             res['message'] = serverDetailSuccess.get('message')
#                                                             res['data'] = resp

#                                                             logger.info(serverDetailSuccess.get('message'))
#                                                             logger.debug(" : ".join([responseBodyData.get('message'), str(res)]))
#                                                             return Response(res)

#                                                         except Exception as err:

#                                                             res['status'] = False
#                                                             res['statusCode'] = DBError.get('statusCode')
#                                                             res['message'] = ", ".join([serverDetailFailure.get('message'), DBError.get('message')])
#                                                             res['data'] = None
                                                            
#                                                             logger.info(", ".join([serverDetailFailure.get('message'), DBError.get('message')]))
#                                                             logger.error(err)
#                                                             return Response(res)

#                                                     except Exception as err:

#                                                         res['status'] = False
#                                                         res['statusCode'] = NotEncrypt.get('statusCode')
#                                                         res['message'] = ", ".join([serverDetailFailure.get('message'), NotEncrypt.get('message')])
#                                                         res['data'] = None

#                                                         logger.info(", ".join([serverDetailFailure.get('message'), NotEncrypt.get('message')]))
#                                                         logger.error(err)
#                                                         return Response(res)
                                                
#                                                 try:
#                                                     if not unknownDVC.objects.filter(macAddress = request.headers.get('macAddress')).exists():

#                                                         unknownDVCDB = unknownDVC()
#                                                         unknownDVCDB.publicIp = data.get('publicIp')
#                                                         unknownDVCDB.localIp = data.get('localIp')
#                                                         unknownDVCDB.macAddress = request.headers.get('macAddress')
#                                                         unknownDVCDB.createdOn=(datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                         unknownDVCDB.modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                         unknownDVCDB.save()

#                                                         res['status'] = False
#                                                         res['statusCode'] = serverDetailNotExists.get('statusCode')
#                                                         res['message'] = ", ".join([serverDetailFailure.get('message'), serverDetailNotExists.get('message')])
#                                                         res['data'] = None

#                                                         logger.info(", ".join([serverDetailFailure.get('message'), serverDetailNotExists.get('message')]))
#                                                         return Response(res)

#                                                     else:

#                                                         unknownDVCDB = unknownDVC.objects.filter(macAddress = request.headers.get('macAddress'))
#                                                         publicIp = data.get('publicIp')
#                                                         localIp = data.get('localIp')
#                                                         macAddress = request.headers.get('macAddress')
#                                                         modifiedOn = (datetime.now()).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))
#                                                         unknownDVCDB.update(publicIp=publicIp, localIp=localIp, macAddress=macAddress, modifiedOn=modifiedOn)

#                                                         res['status'] = False
#                                                         res['statusCode'] = serverDetailNotExists.get('statusCode')
#                                                         res['message'] = ", ".join([serverDetailFailure.get('message'), serverDetailNotExists.get('message')])
#                                                         res['data'] = None

#                                                         logger.info(", ".join([serverDetailFailure.get('message'), serverDetailNotExists.get('message')]))
#                                                         return Response(res)

#                                                 except Exception as err:

#                                                     res['status'] = False
#                                                     res['statusCode'] = unknownDVCError.get('statusCode')
#                                                     res['message'] = ", ".join([serverDetailFailure.get('message'), unknownDVCError.get('message')])
#                                                     res['data'] = None

#                                                     logger.info(", ".join([serverDetailFailure.get('message'), unknownDVCError.get('message')]))
#                                                     logger.error(err)
#                                                     return Response(res)

#                                         except Exception as err:

#                                             res['status'] = False
#                                             res['statusCode'] = serverFinderError.get('statusCode')
#                                             res['message'] = ", ".join([serverDetailFailure.get('message'), serverFinderError.get('message')])
#                                             res['data'] = None

#                                             logger.info(", ".join([serverDetailFailure.get('message'), serverFinderError.get('message')]))
#                                             logger.error(err)
#                                             return Response(res)

#                                     else:

#                                         res['status'] = False
#                                         res['statusCode'] = ipAddressInvalid.get('statusCode')
#                                         res['message'] = ", ".join([serverDetailFailure.get('message'), ipAddressInvalid.get('message')])
#                                         res['data'] = None

#                                         logger.info(", ".join([serverDetailFailure.get('message'), ipAddressInvalid.get('message')]))
#                                         return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#                                 except Exception as err:

#                                     res['status'] = False
#                                     res['statusCode'] = validationError.get('statusCode')
#                                     res['message'] = ", ".join([serverDetailFailure.get('message'), validationError.get('message')])
#                                     res['data'] = None

#                                     logger.info(", ".join([serverDetailFailure.get('message'), validationError.get('message')]))
#                                     logger.error(err)
#                                     return Response(res)

#                             except Exception as err:

#                                 res['status'] = False
#                                 res['statusCode'] = NotDecrypt.get('statusCode')
#                                 res['message'] = ", ".join([serverDetailFailure.get('message'), NotDecrypt.get('message')])
#                                 res['data'] = None

#                                 logger.info(", ".join([serverDetailFailure.get('message'), NotDecrypt.get('message')]))
#                                 logger.error(err)
#                                 return Response(res)

#                         except Exception as err:

#                             res['status'] = False
#                             res['statusCode'] = sessionKeyNotExists.get('statusCode')
#                             res['message'] = ", ".join([serverDetailFailure.get('message'), sessionKeyNotExists.get('message')])
#                             res['data'] = None

#                             logger.info(", ".join([serverDetailFailure.get('message'), sessionKeyNotExists.get('message')]))
#                             logger.error(err)
#                             return Response(res)

#                     else:

#                         res['status'] = False
#                         res['statusCode'] = macAddressInvalid.get('statusCode')
#                         res['message'] = ", ".join([serverDetailFailure.get('message'), macAddressInvalid.get('message')])
#                         res['data'] = None

#                         logger.info(", ".join([serverDetailFailure.get('message'), macAddressInvalid.get('message')]))
#                         return Response(res, status = status.HTTP_401_UNAUTHORIZED)

#             else:

#                 res['status'] = False
#                 res['statusCode'] = requestBody.get('statusCode')
#                 res['message'] = ", ".join([serverDetailFailure.get('message'), requestBody.get('message')])
#                 res['data'] = None

#                 logger.info(", ".join([serverDetailFailure.get('message'), requestBody.get('message')]))
#                 return Response(res)

#         except Exception as err:
            
#             res['status'] = False
#             res['statusCode'] = serverDetailError.get('statusCode')
#             res['message'] = serverDetailError.get('message')
#             res['data'] = None
            
#             logger.info(serverDetailError.get('message'))
#             logger.error(err)
#             return Response(res)

#     else:

#         res['status'] = False
#         res['statusCode'] = requestInvalid.get('statusCode')
#         res['message'] = requestInvalid.get('message')
#         res['data'] = None
        
#         logger.info(requestInvalid.get('message'))
#         return Response(res)
# #### DVC REGISTER SECTION END ####
