from MVCEngine import Controller
from MVCEngine import RenderView

class home_controller(Controller):

	def index(self):
		return RenderView(self.context)	
