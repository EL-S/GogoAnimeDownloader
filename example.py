import gogoanimeapi
import converter

#if the episode range has no episodes, it will assume the anime is dead
#gogoanimeapi.download_anime("https://www04.gogoanimes.tv/category/naruto",silent=False)
#gogoanimeapi.download_anime("7363","1","1",silent=False,quality_preferred="360")
#gogoanimeapi.download_anime("https://www04.gogoanimes.tv/category/goblin-slayer","1","10",silent=False,quality_preferred="360") 
#gogoanimeapi.download_multiple_anime("188","188",silent=False,quality_preferred="1080")
gogoanimeapi.download_multiple_anime(quality_preferred="360",quality="lowest") #downloads all
