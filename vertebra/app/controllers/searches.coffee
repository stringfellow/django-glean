Spine = require('spine')

Sidebar = require('controllers/searches.sidebar')

class Searches extends Spine.Controller
  constructor: ->
    super

    @sidebar = new Sidebar
    
    @routes
      '/searches/:id/edit': (params) -> 
        @sidebar.active(params)
        @main.edit.active(params)
      '/searches/:id': (params) ->
        @sidebar.active(params)
        @main.show.active(params)

    @append @sidebar

module.exports = Searches
