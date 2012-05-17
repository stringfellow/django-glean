Spine   = require('spine')
Search = require('models/search')
Manager = require('spine/lib/manager')
$       = Spine.$

Main    = require('controllers/searches.main')
Sidebar = require('controllers/searches.sidebar')

class Searches extends Spine.Controller
  className: 'searches'
  
  constructor: ->
    super
    
    @sidebar = new Sidebar
    @main    = new Main
    
    @routes
      '/searches/:id/edit': (params) -> 
        @sidebar.active(params)
        @main.edit.active(params)
      '/searches/:id': (params) ->
        @sidebar.active(params)
        @main.show.active(params)
    
    divide = $('<div />').addClass('vdivide')
    
    @append @sidebar, divide, @main
    
    Search.fetch()
    
module.exports = Searches
