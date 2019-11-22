import abc
import pygame

class Button:
    def __init__(self, x, y, w, h, text, click):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self._color = pygame.color.THECOLORS['brown4']
        self._rect = pygame.Rect(x, y, w, h)
        self._status = False
        self._screen = pygame.display.get_surface()
        self._text_set = pygame.font.SysFont("courier", 24).render(text, 1, (0,0,0))
        self._click = click
        print(self._click)

    def collision(self, pos):
        if (pos[0]> self.x) and (pos[0] < self.x + self.w) and (pos[1]>self.y) and (pos[1]<self.y + self.h):
            return True
        else:
            return False

    def set_clicked(self, click):
        self._click = click
    
    def clicked(self, *arg):
        print('Здарова')
        print(arg)
        if len(arg)!=0:
            self._click(arg[0])
        else:
            self._click()

    def update(self, pos):
        self._status = self.collision(pos)
        if self._status:
            self._color = pygame.color.THECOLORS['white']
            self._rect = pygame.Rect(self.x - int(self.w/50),self.y - int(self.h/50), int(52/50*self.w), int(52/50*self.h))
        else:
            self._rect = pygame.Rect(self.x, self.y, self.w, self.h)
            self._color = pygame.color.THECOLORS['brown4']

    def draw(self):
        pygame.draw.rect(self._screen, self._color, self._rect)
        text_rect = self._text_set.get_rect()
        text_rect.center = self._rect.center
        self._screen.blit(self._text_set, text_rect)

    def _get_rect(self):
        return self._rect
    
    def _set_rect(self, value: pygame.Rect):
        self._rect = value
        
    def _get_color(self):
        return self._color
    
    def _set_color(self, value):
        self._color = value
        
    def _get_text(self):
        return self._text
    
    def _set_text(self, value):
        self._text_set = pygame.font.SysFont("courier", 24).render(value, 1, (0,0,0))
        
    rect = property(_get_rect, _set_rect)
    text = property(_get_text, _set_rect)
    color = property(_get_color, _set_color)
        
class Screen:
    """
        общий интерфейс(декоратор) с которым работает ui_manager
    """

    @abc.abstractmethod
    def show(self):
        """
            вызывается при приклеплении экрана к менеджеру
        """
        pass

    @abc.abstractmethod
    def update(self, delta: float):
        """
            вызывается каждый раз, когда надо обновить экран
        :param delta: шаг по времени
        """
        pass

    @abc.abstractmethod
    def render(self):
        """
            вызывается каждый раз, когда надо отрисовать экран
        """
        pass

    @abc.abstractmethod
    def destroy(self):
        """
            вызывается при уничтожении экрана
        """
        pass

    @abc.abstractmethod
    def call(self, event):
        """
            вызывается ядром при обработке действий
        :param event:
        """
        pass
        