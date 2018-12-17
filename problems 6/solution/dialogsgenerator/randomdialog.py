import sys
from random import randint
import pandas as pd


class RandomDialog(object):
    
    def __init__(self, agents, max_len=5):
        """
        # Инициализация
        """
        self.agents = agents
        self.max_len = max_len
        self.eval_stor = None

    def generate(self):
        """
        Генерирует случайный диалог состоящий из 1-max_len цепочек.
        При генерации вызывает функцию turn.
        Возвращаемый объект является генератором.
        """
        def generate_generator():
            while True:
                dialog = []
                gen = self.turn()
                random_length = randint(1, self.max_len)
                for i in range(1, random_length + 1):
                    dialog.append(next(gen))
                yield dialog
        return generate_generator()

    def turn(self):
        """
        Генерирует одну случайную цепочку следующим образом: выбирается случайный агент.
        Он "говорит" случайное сообщение (msg) из своей Agent.kb (используйте next или send(None)).
        (правила того, как выбирать никак не регулируются, вы можете выбирать случайный твит из Agent.kb никак не учитывая
        переданное msg).
        Это сообщение передается с помощью send (помним, что агент - это объект-генератор).
        Далее получаем ответ от всех агентов и возвращаем (генерируем) их (включая исходное сообщение).
        Возвращаемый объект является генератором.
        """
        def turn_generator():
            while True:
                agent_initiator = self.choose_agent()
                dial = list()
                initial_msg = agent_initiator.send(None)
                dial.append('\t' + str(agent_initiator.name) + ': ' + str(initial_msg))
                for agent in self.agents:
                    if agent == agent_initiator:
                        continue
                    dial.append('\t' + str(agent.name) + ': ' + str(agent.send(initial_msg)))
                yield dial
        return turn_generator()

    def eval(self, dialog=None):
        """
        Превращает генератор случайного далога (который возвращается в self.generate())
        в список списков (пример использования далее).
        Возвращаемый объект является списком.
        """
        if dialog is None:
            dialog = self.generate()
        return next(dialog)

    def write(self, dialog=None, target=sys.stdout):
        """
        Записывает результат self.eval() в соответствующий поток.
        """
        if dialog is None:
            dialog = self.eval()
        for turn_num in range(len(dialog)):
            print("turn ", turn_num, ':', file=target)
            for phrase in dialog[turn_num]:
                print(phrase, file=target)

    def choose_agent(self):
        l = len(self.agents)
        num = randint(1, l)
        return self.agents[num - 1]
    
    pass

"""
import agent
clinton = pd.read_csv("clinton.csv", encoding="utf-8")
trump = pd.read_csv("trump.csv", encoding="utf-8")

rd = RandomDialog([agent.Agent(clinton, "clinton"), agent.Agent(trump, "trump")], max_len=3)

generated = rd.generate()
print("generated TYPE : ", generated)

evaled = rd.eval(generated)

print("evaled TYPE", type(evaled))

rd.write(evaled)
"""