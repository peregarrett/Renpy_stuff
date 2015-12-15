init:
    # расположение участников похода в центре поля
    transform party_pos_center:
        xpos = 0.5 ypos = 0.5
    transform party_pos_leftup:
        xpos = 0.4 ypos = 0.4
    transform party_pos_rightup:
        xpos = 0.6 ypos = 0.4
    transform party_pos_leftdown:
        xpos = 0.4 ypos = 0.6
    transform party_pos_rightdown:
        xpos = 0.6 ypos = 0.6


init python:
# картинки на карте
# карта:
    renpy.image('tile l', Image('res/tiles/mine-left.png', anchor=(0.5, 0.5))) # тупик с одним выходом влево
    renpy.image('tile r', Image('res/tiles/mine-right.png', anchor=(0.5, 0.5)))
    renpy.image('tile u', Image('res/tiles/mine-up.png', anchor=(0.5, 0.5)))
    renpy.image('tile d', Image('res/tiles/mine-down.png', anchor=(0.5, 0.5)))
    renpy.image('tile lr', Image('res/tiles/mine-left-right.png', anchor=(0.5, 0.5)))
    renpy.image('tile lu', Image('res/tiles/mine-left-up.png', anchor=(0.5, 0.5)))
    renpy.image('tile ld', Image('res/tiles/mine-left-down.png', anchor=(0.5, 0.5)))
    renpy.image('tile ur', Image('res/tiles/mine-up-right.png', anchor=(0.5, 0.5)))
    renpy.image('tile ud', Image('res/tiles/mine-up-down.png', anchor=(0.5, 0.5)))
    renpy.image('tile rd', Image('res/tiles/mine-right-down.png', anchor=(0.5, 0.5)))
    renpy.image('tile lur', Image('res/tiles/mine-left-up-right.png', anchor=(0.5, 0.5)))
    renpy.image('tile urd', Image('res/tiles/mine-up-right-down.png', anchor=(0.5, 0.5)))
    renpy.image('tile lrd', Image('res/tiles/mine-right-down-left.png', anchor=(0.5, 0.5)))
    renpy.image('tile lud', Image('res/tiles/mine-down-left-up.png', anchor=(0.5, 0.5)))
    renpy.image('tile lurd', Image('res/tiles/mine-all.png', anchor=(0.5, 0.5)))
# стрелочки
    renpy.image('arrow_l', Image('res/tiles/arrow-l.png', anchor=(0.0, 0.5)))
    renpy.image('arrow_l_high', Image('res/tiles/arrow-l-highlight.png', anchor=(0.0, 0.5)))
    renpy.image('arrow_r', Image('res/tiles/arrow-r.png', anchor=(1.0, 0.5)))
    renpy.image('arrow_r_high', Image('res/tiles/arrow-r-highlight.png', anchor=(1.0, 0.5)))
    renpy.image('arrow_u', Image('res/tiles/arrow-u.png', anchor=(0.5, 0.0)))
    renpy.image('arrow_u_high', Image('res/tiles/arrow-u-highlight.png', anchor=(0.5, 0.0)))
    renpy.image('arrow_d', Image('res/tiles/arrow-d.png', anchor=(0.5, 1.0)))
    renpy.image('arrow_d_high', Image('res/tiles/arrow-d-highlight.png', anchor=(0.5, 1.0)))
# персонажи
    renpy.image('sl_px', Image('res/tiles/sl.png', anchor=(0.5, 1.0)))
    renpy.image('pi_px', Image('res/tiles/pi.png', anchor=(0.5, 1.0)))

    # квадрат на карте с координатами xpos ypos
    class Tile:
        def __init__(self, xpos, ypos, img):
            if not isinstance(xpos, int):
                raise TypeError, xpos
            if not isinstance(ypos, int):
                raise TypeError, ypos
            self.xpos = xpos # положение на карте
            self.ypos = ypos 
            self.image = img
            self.exits = dict() # выходы отсюда
        # добавляем выход. dir = 'u'p,'d'own,'l'eft,'r'ight. exit = Exit или Tile, куда выходим
        def add_exit(self, dir, exit):
            if isinstance(exit, Exit):
                self.exits[dir] = exit
            elif isinstance(exit, Tile):
                self.exits[dir] = Exit(self, exit)
            else:    
                raise TypeError, exit
        # проверяем, существует ли выход в данном направлении
        def get_exit(self, dir):
            return self.exits.get(dir)
            
    # переход между квадратами - в одну сторону. Для двустороннего перехода надо заводить два перехода - оттуда сюда и отсюда туда
    class Exit:
        def __init__(self, tilefrom, tileto, label = None):
            self.tilefrom = tilefrom # откуда переход
            self.tileto = tileto     # куда переход
            self.label = label       # label куда надо прыгнуть
        # пройти через проход
        def pass_through(self):
            return True
    # Вся карта подземелья размером width на height
    class Map:
        def __init__(self, width, height): 
            self.tiles = list()
            for x in range(width):
                for y in range(height):
                    self.tiles[x + y * width] = None
                    
        # читаем квадрат в координатах
        def get_tile(self, x, y):
            return self.tiles[x + y * width]
            
        # добавляем квадрат на карту. tile может быть объектом Tile или парой координат. Возвращаем объект Tile всегда    
        def set_tile(self, tile):
            if isinstance(tile, Tile):
                self.tiles[tile.xpos + tile.ypos * width] = tile
                return tile
            elif isinstance(tile, tuple) and len(tile) >=2:
                ret = Tile(tile[0], tile[1])
                self.tiles[tile[0] + tile[1] * width] = ret
                return ret
            else:
                raise TypeError, tile
        # добавляет проход между квадратами в обе стороны. параметры - объекты Tile или пара координат
        def set_pass(self, tile1, tile2):
            if isinstance(tile1, Tile):
                t1 = tile1.xpos, tile1.ypos
            elif isinstance(tile1, tuple) and len(tile) >=2:
                t1 = tile1[0], tile1[1]
            else:
                raise TypeError, tile1
            if isinstance(tile2, Tile):
                t2 = tile2.xpos, tile2.ypos
            elif isinstance(tile2, tuple) and len(tile) >=2:
                t2 = tile2[0], tile2[1]
            else:
                raise TypeError, tile2
            # определяем направление прохода из 1 в 2. сравниваем по x
            if t1[0] > t2[0]: dir = 'l' 
            elif t1[0] < t2[0]: dir = 'r'
            else: # сравниваем по y
                if t1[1] > t2[1]: dir = 'd'
                elif t1[1] > t2[1]: dir = 'u'
                else: dir = '' # этого никогда не должно быть! разве что захочется сделать прыжок на месте
            self.get_tile(t1[0], t1[1]).add_exit(dir, self.get_tile(t2[0], t2[1]))
            # обратный проход из 2 в 1, меняем направление на противоположное
            if dir = 'l': dir = 'r'
            elif dir = 'r': dir = 'l'
            elif dir = 'u': dir = 'd'
            elif dir = 'd': dir = 'u'
            self.get_tile(t2[0], t2[1]).add_exit(dir, self.get_tile(t1[0], t1[1]))
            
    # участник партии
    class GameCharacter:
        def __init__(self, ch, img, party_pos):
            self.ch = ch # Кто говорит
            self.inventory = list() # вещи в кармане
            self.image = img # фигурка персонажа
            self.party_pos = party_pos # где стоит в группе
            # параметры персонажа:
            self.Wet = False
            self.Scared = False
            self.KnockedOut = False
        
     # собственно, игра
    class DungeonGame(renpy.Displayable):
        Visible = False # Глобальный флаг видимости
        # инициализация карты и параметров
        def __init__(self, **kwargs):
            super(DungeonGame, self).__init__(**kwargs)
        
            self.Dungeon = Map(10, 10)
            # 9 . . . . . . . . . . 
            #                   E
            # 8 . . #-#-#-# . . # .  
            #       |   | |     |
            # 7 . . #-#>#-#-#-#D# .
            #       |     |     |
            # 6 . . # . . # . . # .
            #       |     |
            # 5 . . # . #-#-# . . .     
            #       |   | | |
            # 4 . . # . # # # . . .        
            #       |   |   |
            # 3 . . #-#-#-#-# . . .
            #       |     | |
            # 2 . . # . . # #-# . .
            #       |       | |
            # 1 . . # . . . #<#-#E.
            # 0 . . . . . . . . . .
            #   0 1 2 3 4 5 6 7 8 9    
            # сначала отметим все проходные тайлы
            self.Dungeon.set_tile(2,1, 'tile u')
            self.Dungeon.set_tile(6,1, 'tile u') # нужна картинка с пропастью
            self.Dungeon.set_tile(7,1, 'tile ur')
            self.Dungeon.set_tile(8,1, 'tile l') # нужна картинка с выходом в старый лагерь
            self.Dungeon.set_tile(2,2, 'tile ud')
            self.Dungeon.set_tile(5,2, 'tile u')
            self.Dungeon.set_tile(6,2, 'tile urd')
            self.Dungeon.set_tile(7,2, 'tile ld')
            self.Dungeon.set_tile(2,3, 'tile urd')
            self.Dungeon.set_tile(3,3, 'tile lr')
            self.Dungeon.set_tile(4,3, 'tile lur')
            self.Dungeon.set_tile(5,3, 'tile lrd')
            self.Dungeon.set_tile(6,3, 'tile lud')
            self.Dungeon.set_tile(2,4, 'tile ud')
            self.Dungeon.set_tile(4,4, 'tile ud')
            self.Dungeon.set_tile(5,4, 'tile u')
            self.Dungeon.set_tile(6,4, 'tile ud')
            self.Dungeon.set_tile(2,5, 'tile ud')
            self.Dungeon.set_tile(4,5, 'tile rd')
            self.Dungeon.set_tile(5,5, 'tile lurd')
            self.Dungeon.set_tile(6,5, 'tile ld')
            self.Dungeon.set_tile(2,6, 'tile ud')
            self.Dungeon.set_tile(5,6, 'tile ud')
            self.Dungeon.set_tile(8,6, 'tile u') # нужна картинка с котельной
            self.Dungeon.set_tile(2,7, 'tile urd')
            self.Dungeon.set_tile(3,7, 'tile l') # нужна картинка с пропастью
            self.Dungeon.set_tile(4,7, 'tile ur')
            self.Dungeon.set_tile(5,7, 'tile lurd')
            self.Dungeon.set_tile(6,7, 'tile lr')
            self.Dungeon.set_tile(7,7, 'tile lr') # нужна картинка с дверью
            self.Dungeon.set_tile(8,7, 'tile dlu')
            self.Dungeon.set_tile(2,8, 'tile rd')
            self.Dungeon.set_tile(3,8, 'tile lr')
            self.Dungeon.set_tile(4,8, 'tile rdl')
            self.Dungeon.set_tile(5,8, 'tile ld')
            self.Dungeon.set_tile(8,8, 'tile d') # нужна картинка с выходом под Генду
            
            # ломаем стены, делаем проходы, выставляем дополнительные условия и события на переходы
            self.Dungeon.set_pass((2,1), (2,2))
            self.Dungeon.set_pass((6,1), (6,2))
            self.Dungeon.get_tile(7,1).add_exit('l',self.Dungeon.get_tile(6,1))# one-way, из 7,1 в 6,1
            self.Dungeon.set_pass((7,1), (7,2))
            self.Dungeon.set_pass((7,1), (8,1))
            self.Dungeon.get_tile(8,1).add_exit('r', Exit(self.Dungeon.get_tile(8,1), None)) # выход из подземелья через старый лагерь
            
            self.Dungeon.set_pass((2,2), (2,3))
            self.Dungeon.set_pass((5,2), (5,3))
            self.Dungeon.set_pass((6,2), (7,2))
            self.Dungeon.set_pass((6,2), (6,3))
            
            self.Dungeon.set_pass((2,3), (3,3))
            self.Dungeon.set_pass((2,3), (2,4))
            self.Dungeon.set_pass((3,3), (4,3))
            self.Dungeon.set_pass((4,3), (4,4))
            self.Dungeon.set_pass((4,3), (5,3))
            self.Dungeon.set_pass((5,3), (6,3))
            self.Dungeon.set_pass((6,3), (6,4))

            self.Dungeon.set_pass((2,4), (2,5))    
            self.Dungeon.set_pass((4,4), (4,5))    
            self.Dungeon.set_pass((5,4), (5,5))     
            self.Dungeon.set_pass((6,4), (6,5)) 
            
            self.Dungeon.set_pass((2,5), (2,6))    
            self.Dungeon.set_pass((4,5), (5,5))    
            self.Dungeon.set_pass((5,5), (6,5))    
            self.Dungeon.set_pass((5,5), (5,6))

            self.Dungeon.set_pass((2,6), (2,7))    
            self.Dungeon.set_pass((5,6), (5,7))    
            self.Dungeon.set_pass((8,6), (8,7))    
            
            self.Dungeon.set_pass((2,7), (2,8))    
            self.Dungeon.set_pass((2,7), (3,7))    
            self.Dungeon.get_tile(3,7).add_exit('r', self.Dungeon.get_tile(4,7)) # one-way с 3,7 в 4,7. затяжное падение одностороннее
            self.Dungeon.get_tile(4,7).add_exit('l', self.Dungeon.get_tile(4,7)) # попытаться влево, не получается
            self.Dungeon.set_pass((4,7), (4,8))
            self.Dungeon.set_pass((4,7), (5,7))
            self.Dungeon.set_pass((5,7), (5,8))
            self.Dungeon.set_pass((5,7), (6,7))
            self.Dungeon.set_pass((6,7), (7,7))
            self.Dungeon.set_pass((7,7), (8,7)) # дверь в котельную
            self.Dungeon.set_pass((8,7), (8,8))
            
            self.Dungeon.set_pass((2,8), (3,8))# переход 8,3 в 8,2. дикий ИИ Шурика, если мокрый, долбанёт током, если напуган, нападёт (бегство)
            self.Dungeon.set_pass((2,8), (3,8))
            self.Dungeon.set_pass((3,8), (4,8))
            self.Dungeon.set_pass((4,8), (5,8))
            self.Dungeon.get_tile(8,8).add_exit('u', Exit(self.Dungeon.get_tile(8,8), None) # выход наружу под Гендой
            
            self.current_pos = None # текущее расположение партии на карте
            self.current_exit = None # текущий выход - заполняется только во время срабатывания события на переход
            self.party = list() # кто идет с нами
        
        # Рисуем карту и все происходящее на экране
        def render(self, width, height, st, at):
            return renpy.render(1,1)
        # Взаимодействия
        def event(self, ev, x, y, st):
            return
        
            # переходы
        def action_MoveUp:
            return
        def action_MoveDown:
            return
        def action_MoveLeft:
            return
        def action_MoveRight:
            return
        
        
        def Start(self, start_pos, party):
            self.current_pos = start_pos
            self.party = party()
        
       
        def DrawState(self):
            renpy.scene()
            # Draw tile
            tile = self.Dungeon.get_tile(self.current_pos)
            renpy.show(tile.img, at_list = 'truecenter')
            # создаем "кнопки" для выхода по направлениям
            
            
            # Draw party
            for person in self.party:
                renpy.show(person.img, at_list = person.party_pos)
            
            # Draw fog-of-war
            
            # Draw explored map
    
    # Объект-карта. Все как в alt_map
    renpy.store.alt_DungeonGame = DungeonGame()
    
    # функции для показа и взаимодействия с игрой из сценария
    # инициализация - стартовая позиция, набор участников
    def alt_dungeongame_setstart(pos):
        renpy.store.alt_DungeonGame.current_pos = pos
    # добавляем человека в партию
    def alt_dungeongame_addchar(ch, img, party_pos)
        renpy.store.alt_DungeonGame.party.append(GameCharacter(ch, img, party_pos))
    # убираем человека из партии
    def alt_dungeongame_removechar(ch)
        for p in renpy.store.alt_DungeonGame.party:
            if p.ch == ch:
                renpy.store.alt_DungeonGame.party.remove(p)
                return p
    # задаем событие на переход
    def alt_dungeongame_setevent(x, y, exit, label)
        renpy.store.alt_DungeonGame.Dungeon.get_tile(x, y).get_exit(exit).label = label
    # убираем все события с переходов
    def alt_dungeongame_resetevents()
        for t in renpy.store.alt_DungeonGame.Dungeon.tiles:
            if t != None:
                for e in t.exits.Values: e.label = None
    # показать карту
    def alt_dungeongame_show():
        renpy.store.alt_DungeonGame.Visible = True
    # спрятать карту
    def alt_dungeongame_hide():
        renpy.store.alt_DungeonGame.Visible = False
    # пройти или не пройти в проход. Должно вызваться при срабатывании события на переходе. если go = True - проходим через выход, если False - то остаемся на месте.
    def alt_dungeongame_travel(go)
    
label alt_cotocombs:
    menu:
        "Открыть карту?":
            jump alt_cotocombs_map
        "Воспользоваться автопилотом.":
            "Я решил прислушаться к интуиции и, прикинув направление, зашагал в нужную сторону."
            return 
label alt_cotocombs_map:
    # Инициализация 
    $ dungeongame_init
    # Определяем состав партии
    $ dungeongame_add_char(me, 'pi_px', 'party_pos_center')
    $ dungeongame_add_char(me, 'sl_px', 'party_pos_party_pos_leftup')
    # Определяем стартовую точку
    $ dungeongame_start(8,1)
    # Запуск!
    $ dungeongame_show

    #Пилим DND-карту
    #Активный тайл-сет: 8х8, номерация тайлов с левого нижнего угла, старт с тайла 8, если идём со стороны старого лагеря, либо с тайла 64, если идём от Генды.
    #Ключи участия: alt_catac_wet(попал в воду), alt_ow_77 (односторонний спуск, закрывающий выход), alt_ow_73(односторонний проход через воду(засыпает породой))
    #Ключи прохождения alt_catac2 = True (открывает тайл на карте), alt_catac_came = 0 (расчёт, куда какой поворот смотрит.)
    #Погнали ништяки - собственно тайлы и пути.
    #Доступные тайлы: #y x
    #12 -  вверх в 22 (мокрый)
    #16 - вверх в 26, вправо в 7  - доступна только с 7 (мокрый)
    #17 - влево к 6, вверх в 27, вправо в 8, 
    #18 - влево к 7, вправо к выходу (если  есть верёвка)
    #22 - вверх в 32(можно пробежаться до 72), вниз в 2
    #25 - вверх в 35 (шахта)
    #26 - вверх в 36, вправо в 27
    #27 - вниз в 7, и влево к 26
    #32 - вверх в 42, вниз в 22, вправо в 33(можно пробежаться до 36)
    #33 - влево в 32, вправо в 34  
    #34 - влево в 33, вправо в 35,  вверх в 41 (? 44 ?)
    #35 - влево в 34, вправо в 36, вниз в 25
    #36 - влево в 35, вверх в 46
    #42 - вверх в 52, вниз в 32
    #44 - вверх в 54, вниз в 34
    #45 - вверх в 55
    #46 - вверх в 56, вниз в в 36
    #52 - вверх в 62, вниз в 42
    #54 - вниз в 44, вправо в 55
    #55 - вверх в 65, влево в 54, вправо в 56, вниз в 45(для д3 ключей)
    #56 - влево в 55, вниз в 46
    #62 - вверх в 72, вниз в 52
    #65 - вверх в 75, вниз в 55
    #68 - вверх в 78(шахта)
    #72 - вверх в 82, вниз в 72, вправо в 73
    #73 - вправо в 74(затяжное падение одностороннее)
    #74 - вверх в 84, попытаться влево в 73 (мокрый)
    #75 - вниз в 65, вверх в 85, вправо в 76
    #76 - влево в 75, вправо в 77
    #77 - влево в 76, вправо в 78(дверь)
    #78 - влево в 76(если есть верёвка), вверх в 88 (? 78 - 76 ?)
    #82 - вниз в 72 (шахта)
    #83 - вправо в 82 (дикий ИИ Шурика), если мокрый, долбанёт током, если напуган, нападёт (бегство)
    #84 - влево в 83(если ходил соло), вправо в 85, вниз в 74(мокрый)
    #85 - влево в 84, вниз в 75
    #88 - вверх в лагерь (комната с лестницей)

# Раздача монстров случайная, можно сбежать, можно скормить Славе, экип представлен в виде верёвки. Изменения состояния на "мокрый", "оглушённый" и "напуганный". Всё это на уровне пре-самого-альфа-планирования толком даже ничего не продумывал. Хотя в планах темнота (керосинка в одной из бытовок или попробовать запалить подачу напряжения), возможность найти разводной ключ и от выхода пустить газ, етц.