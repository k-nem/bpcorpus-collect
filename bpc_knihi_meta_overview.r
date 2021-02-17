library(tidyverse)
library(readr)
library(stringr)
library(dplyr)
library(ggplot2)
library(reshape)

setwd('.')
getwd()

m <- read_csv('bpc_knihi_metadf.csv')
View(m)

m %>%
  count(StyleGenre, sort=T) %>%
  View()

m %>%
  count(Authors,StyleGenre, sort=T) %>%
  View() 

# автор
m %>%
  filter(AvailableText == T) %>%  
  count(Authors, sort=T) %>%
  ggplot(aes(reorder(Authors, n), n, fill = n)) +
  geom_text(aes(reorder(Authors, n), n, 
                label = n),
            position = position_dodge(1),
            hjust = 0) +
  geom_col() +
  coord_flip()

# жанр/автор
m %>%
  filter(AvailableText == T) %>%  
  filter(str_detect(StyleGenre, "мастацкі")) %>%  
  count(Authors,StyleGenre, sort=T) %>%
  ggplot(aes(reorder(Authors,n), n)) +
  geom_col(aes(fill = StyleGenre)) +
  theme(legend.position = 'bottom',
        legend.direction = "vertical",
        legend.key.size = unit(0.1,"cm"),
        legend.key.width = unit(0.3,"cm")) +
  coord_flip()
 
# жанр
m %>%
 filter(AvailableText == T) %>%  
 filter(str_detect(StyleGenre, "мастацкі")) %>%
 count(StyleGenre, sort=T) %>%
 ggplot(aes(reorder(StyleGenre, n), n, fill = n)) +
 geom_text(aes(reorder(StyleGenre, n), n, 
               label = n),
           position = position_dodge(1),
           hjust = 0) +
 geom_col() +
 coord_flip()

# стихи
m %>%
  filter(AvailableText == T) %>%
  filter(str_detect(StyleGenre, c('верш'))) %>%  
  count(Authors, sort=T) %>%
  ggplot(aes(reorder(Authors, n), n, fill = n)) +
  geom_text(aes(reorder(Authors, n), n, 
                label = n),
            position = position_dodge(1),
            hjust = 0) +
  geom_col() +
  coord_flip()

# заголовки на страницах авторов
m %>%
  count(SectionAuthor, sort=T) %>%
  View()

# доступность
m %>%
  select(FileHash,FileSize,AvailableText) %>%
  count(AvailableText = F)

# язык
m %>%
  count(Lang, sort=T) %>%
  View()

m %>%
  count(LangOrig, sort=T) %>%
  View()

lang <- c('pol','rus','rus?')
m %>%
  filter(LangOrig %in% lang) %>%
  View()
