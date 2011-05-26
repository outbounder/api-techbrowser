from MVCEngine import MVCContext

class app(object):
    def routes(self, router):
        # The application should have all of its routes defined here.
        
        api = restify(router)
        
        api.crud("entry")
        api.crud("tag")
        
        api.get("/suggest/tags", controller="suggest", action="tags")
        api.get("/suggest/tag", controller="suggest", action="tag")
        api.get("/suggest/hypertree", controller="suggest", action="hypertree")
            
        router.connect('/:entry/:id', controller="rest", action="index")
        router.connect('/:entry/create', controller="rest", action="post")
        router.connect('/:entry/update/:id', controller="rest", action="put")
        router.connect('/:entry/delete/:id', controller="rest", action="delete")
        
        router.connect('', controller="home", action="index")
        router.connect('/:controller/:action/:id')
        router.connect('/:controller/:action')

    def load(self, context):
        # Put here any code that should be run every time
        # that your application handles a request
        pass

	def missing_controller(self, context):
        # This method is run when MVCEngine can not find a controller that has been requested.
        # If it returns an ActionResult, that ActionResult will be rendered as normal.
		pass

    def missing_action(self, context):
        # This method is run when MVCEngine can not find the requested action in the
        # requested controller. If it returns an ActionResult, that result will be rendered
        # as normal.
		pass
    
