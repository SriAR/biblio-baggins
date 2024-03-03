import subprocess
from .logger import logger

class Notify:
    def __init__(self, persona):
        self.persona = persona
        self.init_persona()

    def init_persona(self):
        if self.persona == 'evrart':
            self.appname = 'Evrart Claire'
            self.icon = '/home/cs/dotfiles/.assets/evrart_claire.png'

        elif self.persona == 'pandemonica':
            self.appname = 'Pandemonica'
            self.icon = '/home/cs/dotfiles/.assets/low_battery_pandemonica.png'

    def say(self, title, message, urgency='normal', timeout=5000):
        command = ['dunstify', '-a', self.appname, '-i', self.icon, '-t', str(timeout), '-u', str(urgency), title, message]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to send notification: {e}")

evrart = Notify('evrart')
pandemonica = Notify('pandemonica')
