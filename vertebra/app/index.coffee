require('lib/setup')

Spine    = require('spine')
Searches = require('controllers/searches')

class App extends Spine.Controller
  constructor: ->
    super
    @searches = new Searches
    @append @searches.active()
    
    Spine.Route.setup()

module.exports = App
